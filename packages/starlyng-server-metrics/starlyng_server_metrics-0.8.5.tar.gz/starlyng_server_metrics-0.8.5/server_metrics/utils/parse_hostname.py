"""
parse_hostname.py
"""
def get_hostname(ip: str, port: int) -> int:
    """
    Gets the hostname based on local or public IP addresses

    Args:
        ip (str):
        port (int):

    Raises:
        ValueError:
        ValueError:

    Returns:
        int:
    """
    if ip.startswith("192.168"):
        ip_base_address = int(ip.split(".")[-1])
        if ip_base_address < 10 or ip_base_address > 255:
            raise ValueError(f"IP base address must be between 10 and 255: ip_base_address = {ip_base_address}")
        host_id_int = ip_base_address - 10
        host_id = str(host_id_int).zfill(2)
    else:
        if port < 2200 or port > 2299:
            raise ValueError(f"Port number must be between 2200 and 2299: port = {port}")
        host_id = str(port % 100).zfill(2)
    return "starlyng" + host_id
