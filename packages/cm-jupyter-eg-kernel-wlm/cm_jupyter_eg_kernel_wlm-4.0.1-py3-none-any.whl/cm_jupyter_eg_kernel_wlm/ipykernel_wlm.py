"""Main ipykernel_wlm  module"""

import argparse
import base64
import json
import logging
import os
import random
import socket
import tempfile
import typing
import uuid
from multiprocessing import Process
from subprocess import Popen
from time import time

from bash_kernel.kernel import BashKernel  # type: ignore
from Crypto.Cipher import AES
from ipykernel.ipkernel import IPythonKernel
from jupyter_client.connect import write_connection_file

# Minimum port range size and max retries
min_port_range_size = int(os.getenv("EG_MIN_PORT_RANGE_SIZE", "1000"))
max_port_range_retries = int(os.getenv("EG_MAX_PORT_RANGE_RETRIES", "5"))
log_level = int(os.getenv("EG_LOG_LEVEL", "10"))

logging.basicConfig(format="[%(levelname)1.1s %(asctime)s.%(msecs).03d %(name)s] %(message)s")

logger = logging.getLogger("ipykernel_wlm")
logger.setLevel(log_level)

# Block size for cipher obj can be 16, 24, or 32. 16 matches 128 bit.
BLOCK_SIZE = 16
PADDING = "%"


def prepare_gateway_socket(lower_port, upper_port):
    """Prepare control socket for EG server to connect"""
    sock = _select_socket(lower_port, upper_port)
    if not sock:
        return None
    logger.info(
        "Signal socket bound to host: '%s', port: '%s'",
        sock.getsockname()[0],
        sock.getsockname()[1],
    )
    sock.listen(1)
    sock.settimeout(5)
    return sock


def _encrypt(connection_info, conn_file):
    """Encrypt connection data"""

    def pad(data):
        """Ensure that the length of the data that will be encrypted is a
        multiple of BLOCK_SIZE by padding with '%' on the right."""
        return data.decode("utf-8") + (BLOCK_SIZE - len(data) % BLOCK_SIZE) * PADDING

    def encrypt_aes(cypher, data):
        """Encrypt connection_info whose length is a multiple
        of BLOCK_SIZE using AES cipher and then encode the
        resulting byte array using Base64."""
        return base64.b64encode(cypher.encrypt(pad(data).encode("utf-8")))

    key = os.getenv("ENCRYPT_KEY")
    if key is None:
        # Create a key using first 16 chars of the kernel-id that is burnt in
        # the name of the connection file.
        base_name = os.path.basename(conn_file)
        if base_name.find("kernel-") == -1:
            msg = f"Invalid connection file name '{conn_file}'"
            logger.error(msg)
            raise RuntimeError(msg)

        tokens = base_name.split("kernel-")
        kernel_id = tokens[1]
        key = kernel_id[0:16]

    # Creates the cipher obj using the key.
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)

    payload = encrypt_aes(cipher, connection_info)
    return payload


def return_connection_info(connection_file, response_addr, lower_port, upper_port):
    """Return connection information back to EG"""

    response_parts = response_addr.split(":")
    if len(response_parts) != 2:
        logger.error(
            "Invalid format for response address '%s'. Assuming 'pull' mode...",
            response_addr,
        )
        return None

    response_ip = response_parts[0]
    try:
        response_port = int(response_parts[1])
    except ValueError:
        logger.error(
            "Invalid port component found in response address '%s'. Assuming 'pull' mode...",
            response_addr,
        )
        return None

    with open(connection_file, encoding="utf-8") as connection_file_fp:
        cf_json = json.load(connection_file_fp)

    # add process and process group ids into connection info
    pid = os.getpid()
    cf_json["pid"] = str(pid)
    cf_json["pgid"] = str(os.getpgid(pid))

    # prepare socket address for handling signals
    gateway_sock = prepare_gateway_socket(lower_port, upper_port)
    if not gateway_sock:
        return None
    cf_json["comm_port"] = gateway_sock.getsockname()[1]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((response_ip, response_port))
        json_content = json.dumps(cf_json).encode(encoding="utf-8")
        logger.debug("JSON Payload '%s'", json_content)
        payload = _encrypt(json_content, connection_file)
        logger.debug("Encrypted Payload '%s'", payload)
        sock.send(payload)
    except ConnectionRefusedError:
        msg = f"Unable to connect to {response_ip}:{response_port}"
        logger.error(msg)
        return None
    finally:
        sock.close()

    return gateway_sock


def determine_connection_file(conn_file, kid):
    """If the directory exists, use the original file,
    else create a temporary file."""

    if conn_file is None or not os.path.exists(os.path.dirname(conn_file)):
        if kid is not None:
            basename = "kernel-" + kid
        else:
            basename = os.path.splitext(os.path.basename(conn_file))[0]
        tempfile_fd, conn_file = tempfile.mkstemp(
            suffix=".json",
            prefix=basename + "_",
        )
        os.close(tempfile_fd)
        logger.debug("Using connection file '%s'.", conn_file)

    return conn_file


def _select_ports(count, lower_port, upper_port):
    """Select and return n random ports that are available and adhere
    to the given port range, if applicable."""
    ports = []
    sockets = []
    for _ in range(count):
        sock = _select_socket(lower_port, upper_port)
        if not sock:
            return None
        ports.append(sock.getsockname()[1])
        sockets.append(sock)
    for sock in sockets:
        sock.close()
    return ports


def _select_socket(lower_port, upper_port) -> typing.Optional[socket.socket]:
    """Create and return a socket whose port is available and adheres
    to the given port range, if applicable."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    found_port = False
    retries = 0
    while not found_port:
        try:
            sock.bind(("0.0.0.0", _get_candidate_port(lower_port, upper_port)))
            found_port = True
        except OSError:
            retries = retries + 1
            if retries > max_port_range_retries:
                msg = "Failed to locate port within range "
                msg += f"{lower_port}..{upper_port} after "
                msg += f"{max_port_range_retries} retries!"
                logger.error(msg)
                return None
    return sock


def _get_candidate_port(lower_port, upper_port):
    """Return random port from the range"""
    range_size = upper_port - lower_port
    if range_size == 0:
        return 0
    return random.randint(lower_port, upper_port)


def _validate_port_range(port_range):
    """Check if we have a proper range"""
    # if no argument was provided, return a range of 0
    if not port_range:
        return 0, 0

    try:
        port_ranges = port_range.split("..")
        lower_port = int(port_ranges[0])
        upper_port = int(port_ranges[1])

        port_range_size = upper_port - lower_port
        if port_range_size != 0:
            if port_range_size < min_port_range_size:
                msg = "Port range validation failed for range: "
                msg += f"'{port_range}'.  Range size must be at least "
                msg += f"{min_port_range_size} as specified by"
                msg += " env EG_MIN_PORT_RANGE_SIZE"
                raise RuntimeError(msg)
    except (ValueError, IndexError) as exc:
        msg = "Port range validation failed for range: "
        msg += f"'{port_range}'.  Error was: {exc}"
        raise RuntimeError(msg) from None

    return lower_port, upper_port


def get_gateway_request(sock):
    """Read message from EG"""
    conn = None
    data = ""
    request_info = None
    try:
        conn, _ = sock.accept()
        while True:
            buffer = conn.recv(1024).decode("utf-8")
            if not buffer:  # send is complete
                request_info = json.loads(data)
                break
            # append what we received until we get no more...
            data = data + buffer
    except OSError as exc:
        if not isinstance(exc, socket.timeout):
            raise exc
    finally:
        if conn:
            conn.close()

    return request_info


def gateway_listener(sock, parent_pid, timeout=30):
    """Watchdog function looping over and is waiting for signals from EG"""
    shutdown = False
    last_update = time()
    while not shutdown:
        request = get_gateway_request(sock)
        if request:
            # prevent logging poll requests since that occurs every 3 seconds
            signum = -1
            if request.get("signum") is not None:
                signum = int(request.get("signum"))
                os.kill(parent_pid, signum)
            if request.get("shutdown") is not None:
                shutdown = bool(request.get("shutdown"))
            if signum != 0:
                logger.info("gateway_listener got request: '%s'", request)
            last_update = time()
        else:
            if timeout <= 0:
                # do not shutdown kernel is server is lost
                continue
            since_last_update = time() - last_update
            if since_last_update > timeout:
                os.kill(parent_pid, 9)
                shutdown = True
                continue
            logger.info(
                "No answer from server. Shutdown in %d sec",
                timeout - since_last_update,
            )
    os.kill(parent_pid, 9)


def start_ipython(namespace, kernel_lang_class, **kwargs):
    """Start kernel process"""

    # pylint: disable=import-outside-toplevel

    import sys

    from ipykernel.kernelapp import IPKernelApp

    # pylint: enable=import-outside-toplevel
    #
    # create an initial list of variables to clear
    # we do this without deleting to preserve the locals so that
    # initialize_namespace isn't affected by this mutation
    to_delete = [k for k in namespace if not k.startswith("__")]

    # delete the extraneous variables
    for k in to_delete:
        del namespace[k]

    # IPKernelApp will try to handle sys.argv too, so cleanup it
    sys.argv = [""]
    # Start the kernel
    IPKernelApp.launch_instance(kernel_class=kernel_lang_class, **kwargs)


def run_external_kernel(cmd, eg_connection_file):
    """Run external kernel as a subprocess"""

    cmd = cmd.format(eg_connection_file=eg_connection_file)
    proc = Popen(cmd, shell=True)  # pylint: disable=consider-using-with
    return proc


# pylint: disable=too-many-locals,too-many-branches,too-many-statements


def main() -> int:
    """Main call"""

    parser = argparse.ArgumentParser()
    supported_langs = {"python": IPythonKernel, "bash": BashKernel}
    parser.add_argument(
        "connection_file",
        nargs="?",
        help="Connection file to write connection info",
    )
    parser.add_argument(
        "--RemoteProcessProxy.response-address",
        dest="response_address",
        nargs="?",
        metavar="<ip>:<port>",
        help="Connection address (<ip>:<port>) for returning connection file",
    )
    parser.add_argument(
        "--RemoteProcessProxy.kernel-id",
        dest="kernel_id",
        nargs="?",
        help="Indicates the id associated with the launched kernel.",
    )
    parser.add_argument(
        "--RemoteProcessProxy.port-range",
        dest="port_range",
        nargs="?",
        metavar="<lowerPort>..<upperPort>",
        help="Port range to impose for kernel ports",
    )
    parser.add_argument(
        "--RemoteProcessProxy.shutdown-timeout",
        dest="shutdown_timeout",
        nargs="?",
        type=int,
        default=30,
        help="Number of sec kernel will be killed if server is unavailable",
    )
    parser.add_argument(
        "--RemoteProcessProxy.kernel-lang",
        dest="language",
        choices=list(supported_langs.keys()),
        default="python",
        help="Kernel language",
    )
    parser.add_argument(
        "--RemoteProcessProxy.kernel-script",
        dest="kernel_script",
        default="",
        help="Kernel command line",
    )
    arguments = vars(parser.parse_args())
    connection_file = arguments["connection_file"]
    response_addr = arguments["response_address"]
    kernel_id = arguments["kernel_id"]
    shutdown_timeout = arguments["shutdown_timeout"]
    if arguments["language"]:
        kernel_lang_class = supported_langs[arguments["language"]]
    else:
        kernel_lang_class = None
    kernel_script = arguments["kernel_script"]
    lower_port, upper_port = _validate_port_range(arguments["port_range"])
    ip = "0.0.0.0"  # pylint: disable=invalid-name

    if kernel_id is None:
        kernel_id = os.getenv("KERNEL_ID")

    if connection_file is None and kernel_id is None:
        msg = "At least one of the parameters: 'connection_file' or "
        msg += "'--RemoteProcessProxy.kernel_id' must be provided!"
        logger.error(msg)
        return 254

    # If the connection file doesn't exist, then create it.
    if (connection_file and not os.path.isfile(connection_file)) or kernel_id is not None:
        key = f"{uuid.uuid4()}".encode("utf-8")
        connection_file = determine_connection_file(connection_file, kernel_id)

        ports = _select_ports(5, lower_port, upper_port)
        if not ports:
            msg = "Unable to find free ports"
            return 254

        write_connection_file(
            fname=connection_file,
            ip=ip,
            key=key,
            shell_port=ports[0],
            iopub_port=ports[1],
            stdin_port=ports[2],
            hb_port=ports[3],
            control_port=ports[4],
        )

    if response_addr:
        gateway_socket = return_connection_info(connection_file, response_addr, lower_port, upper_port)
    else:
        gateway_socket = None

    if not gateway_socket:
        msg = "Unable to get gateway socket"
        logger.error(msg)
        return 254

    if not arguments["kernel_script"]:
        # launch the IPython kernel instance
        kernel_proc = Process(
            target=start_ipython,
            kwargs={
                "namespace": locals(),
                "kernel_lang_class": kernel_lang_class,
                "connection_file": connection_file,
                "ip": ip,
            },
        )
        kernel_proc.start()
    else:
        kernel_proc = run_external_kernel(cmd=kernel_script, eg_connection_file=connection_file)

    if not kernel_proc or not kernel_proc.pid:
        msg = "Unable to start kernel"
        logger.error(msg)
        return 254

    gateway_listener(
        gateway_socket,
        kernel_proc.pid,
        shutdown_timeout,
    )

    try:
        os.remove(connection_file)
    except OSError:
        pass

    try:
        returncode = kernel_proc.exitcode
    except AttributeError:
        returncode = kernel_proc.returncode  # type: ignore

    return returncode  # type: ignore


# pylint: enable=too-many-locals,too-many-branches,too-many-statements


if __name__ == "__main__":
    main()
