import socket
import psutil

def get_ip_address(ifname):
    addrs = psutil.net_if_addrs()
    if ifname in addrs:
        for addr in addrs[ifname]:
            if addr.family == socket.AF_INET:
                return addr.address
    raise ValueError(f"No IPv4 address found for interface {ifname}")

def get_hostname_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip

def get_local_ip_address():
    try:
        return get_ip_address_udp()
    finally:
        return '127.0.0.1'

def get_ip_address_udp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ret = s.getsockname()[0]
    s.close()
    return ret


def is_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        return True
    except:
        pass
    finally:
        s.close()
    return False
