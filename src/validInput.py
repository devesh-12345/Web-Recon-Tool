import re
import socket

def is_valid_URL(full_url):
    if '/' in full_url.split("://")[1]:
        return 2
    pattern = r'^https://www\.[a-zA-Z0-9-]{1,63}(\.[a-zA-Z]{2,})+$'
    if re.match(pattern, full_url):
        return 1
    else: 
        return 0

def ip_resolve(full_url):
    domain = full_url.split("://")[1].split("/")[0]
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return 0

def isValidInput(full_url):
    if "://" not in full_url:
        return "Invalid URL format. Please check input."

    valid_url = is_valid_URL(full_url)

    if valid_url == 2:
        return "Path detected - not allowed."
    elif valid_url ==0:
        return "Invalid URL format. Please check input."
    elif valid_url == 1:
        if ip_resolve(full_url) == 0:
            return "Domain not found or unreachable."

    return 1


if __name__ == "__main__":
    pass
