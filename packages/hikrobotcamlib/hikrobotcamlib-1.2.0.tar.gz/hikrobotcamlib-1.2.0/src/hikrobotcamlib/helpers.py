"""helpers"""
from typing import Tuple, Iterable, Union
import socket

IPAddressType = Union[str, Tuple[int, int, int, int]]


def get_my_ip() -> str:
    """Get this machines default route IP"""
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.settimeout(0)
    try:
        # doesn't even have to be reachable
        sck.connect(("10.254.254.254", 1))
        ipaddr = str(sck.getsockname()[0])
    except Exception:  # pylint: disable=W0718
        ipaddr = "127.0.0.1"
    finally:
        sck.close()
    return ipaddr


def ip2int(ipaddr: IPAddressType) -> int:
    """convert IP string or tuple of ints to singe int"""
    if isinstance(ipaddr, str):
        ip_parts = tuple(int(part) for part in ipaddr.split("."))
    else:
        ip_parts = ipaddr
    masked = (int(ip_parts[0]) << 24) | (int(ip_parts[1]) << 16) | (int(ip_parts[2]) << 8) | int(ip_parts[3])
    return masked


def get_octets(src: int) -> Tuple[int, int, int, int]:
    """Get the octets from an integer, useful for ips etc. returned highest first"""
    nip1 = (src & 0xFF000000) >> 24
    nip2 = (src & 0x00FF0000) >> 16
    nip3 = (src & 0x0000FF00) >> 8
    nip4 = src & 0x000000FF
    return nip1, nip2, nip3, nip4


def get_str(cstr: Iterable[int]) -> str:
    """Convert C string from the camera structs into str"""
    ret = ""
    for val in cstr:
        if val == 0x0:
            break
        ret += chr(val)
    return ret
