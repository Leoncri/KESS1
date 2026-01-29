# converts an IP string to an integer (IPv4 only)
def IP2Int(ip):
    b0, b1, b2, b3 = ip.split('.')
    
    ipInt = (int(b0) << 24) + (int(b1) << 16) + (int(b2) << 8) + int(b3)
    
    return ipInt

# converts an integer back to an IP string (IPv4 only)
def Int2IP(ipInt):
    b0 = str((ipInt >> 24) & 0xFF)
    b1 = str((ipInt >> 16) & 0xFF)
    b2 = str((ipInt >> 8) & 0xFF)
    b3 = str(ipInt & 0xFF)
    
    return b0 + '.' + b1 + '.' + b2 + '.' + b3