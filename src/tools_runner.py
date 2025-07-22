# Automate scanning using external tools through python's subprocess module
# Tools : 1. WhoIs                  : Done
#         2. Nmap                   : Done
#         3. curl                   : Done
#         4. nslookup               : Done
#         5. traceroute / tracert   : Done


import whois
import subprocess
import json
import requests
from bs4 import BeautifulSoup
import platform
from datetime import datetime, timezone
import shutil
import os


# whois functionality
def run_whois(domain):
    # Input: "google.com", Not even subdomain and any path like /index.html
    try:
        domain_name = "Null"
        registrar = "Null"
        registrar_url = "Null"
        reseller = "Null"
        whois_server = "Null"
        referral_url = "Null"
        update_date = "Null"
        creation_date = []
        expiration_date = []
        name_servers = []
        status = []
        emails = []
        dnssec = "Null"
        name = "Null"
        org = "Null"
        address = "Null"
        city = "Null"
        state = "Null"
        registrant_postal_code = "Null"
        country = "Null"
        
        result = whois.whois(domain)

        domain_name = result['domain_name']
        registrar = result['registrar']
        registrar_url = result['registrar_url']
        reseller = result['reseller']
        whois_server = result['whois_server']
        referral_url = result['referral_url']

        # sometimes may one date, return as object not list, so for that
        def to_datetime_list(maybe_date):
            if maybe_date is None:
                return []
            if isinstance(maybe_date, list):
                return maybe_date
            return [maybe_date]

        # creation date
        for item in to_datetime_list(result.get("creation_date")):
            temp = item.isoformat().replace("T", " ") if item.tzinfo else item.strftime("%Y-%m-%d %H:%M:%S")
            creation_date.append(temp)
        creation_date = json.dumps(creation_date, indent=4)

        # expiration date
        for item in to_datetime_list(result.get("expiration_date")):
            temp = item.isoformat().replace("T", " ") if item.tzinfo else item.strftime("%Y-%m-%d %H:%M:%S")
            expiration_date.append(temp)
        expiration_date = json.dumps(expiration_date, indent=4)

        # name servers
        name_servers = result['name_servers']
        name_servers = json.dumps(name_servers, indent=4)

        # status
        status = result['status']
        status = json.dumps(status, indent=4)

        # Emails
        emails = result['emails']
        emails = json.dumps(emails, indent=4)

        dnssec = result['dnssec']
        name = result['name']
        org = result['org']
        address = result['address']
        city = result['city']
        state = result['state']
        registrant_postal_code = result['registrant_postal_code']
        country = result['country']


        # writing to file
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/whois_output_{domain}.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "w") as file:
            file.write("-----------------------------WhoIs Report-----------------------------\n")
            file.write(f"Domain Name: {domain_name}\n")
            file.write(f"Registrar: {registrar}\n")
            file.write(f"Registrar URL: {registrar_url}\n")
            file.write(f"Reseller: {reseller}\n")
            file.write(f"Whois Server: {whois_server}\n")
            file.write(f"Referral URL: {referral_url}\n")
            file.write(f"Update Date: {update_date}\n")
            file.write(f"Creation Date: {creation_date}\n")
            file.write(f"Expiration Date: {expiration_date}\n")
            file.write(f"Name Servers: {name_servers}\n")
            file.write(f"Status: {status}\n")
            file.write(f"Emails: {emails}\n")
            file.write(f"Dnssec: {dnssec}\n")
            file.write(f"Name: {name}\n")
            file.write(f"Org: {org}\n")
            file.write(f"Address: {address}\n")
            file.write(f"City: {city}\n")
            file.write(f"State: {state}\n")
            file.write(f"Registrant postal code: {registrant_postal_code}\n")
            file.write(f"Country: {country}\n")
            file.write("-----------------------------End of WHOIS report-----------------------------\n")
        
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        return f"Error while fetching WHOIS data : {e}"



# Nmap functionality
def run_Nmap(target_ip, ports='1-1000'):
    # Input: "www.google.com"
    no_protocol = target_ip.split("//")[-1]
    domain = no_protocol.split(".")[1]
    try:
        nmap_cmd = ["nmap", "-sV", "-p", ports, target_ip]
        result = subprocess.run(nmap_cmd, capture_output=True, text=True)
    except:
        # Dynamic path finding 
        nmap_path = shutil.which("nmap")
        if nmap_path is None:
            return "Nmap is not found in system PATH. Please install or add to PATH."
        else:
            nmap_cmd =[nmap_path, "-sV", "-p", ports, target_ip]
            result = subprocess.run(nmap_cmd, capture_output=True, text=True)

    clean_output = []
    for line in result.stdout.splitlines():
        if line.strip().startswith("==============NEXT SERVICE FINGERPRINT"):
            break
        clean_output.append(line)

    if not any("Service detection performed" in line for line in clean_output):
        tail_lines = result.stdout.splitlines()[-5:]
        for line in tail_lines:
            if line.strip().lower().startswith("service detection performed"):
                clean_output.append("")
                clean_output.append(line)
                break

    output = "\n".join(clean_output)

    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/nmap_output_{domain}.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("-----------------------------Nmap Report-----------------------------\n")
        file.write(output)
        file.write("\n-----------------------------End of Nmap Report-----------------------------\n")

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()



# curl functionality
def run_curl(url):
    # Input: "https://www.example.com" OR "https://example.com"
    no_protocol = url.split("//")[-1]
    domain = no_protocol.split(".")[1]
    try:
        status_code = ""
        headers = ""
        headers_dict = ""
        headers_json = ""
        content_type = ""

        soup = ""
        readable_text = ""
        page_title = ""
        responded_text = ""

        # Trying request and curl for website.
        try:
            response = requests.get(url, timeout=5)

            status_code = response
            headers = response.headers
            headers_dict = dict(headers)
            headers_json = json.dumps(headers_dict, indent=4)
            content_type = response.headers.get("Content-Type", "")

            # Trying Beautifulsoup object
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                readable_text = soup.get_text(separator='\n', strip=True)
                responded_text = response.text
            except:
                soup = "BeautifulSoup Failed !!!"

            if (content_type == "text/html") and (soup.title and soup.title.string):
                page_title = soup.title.string.strip()
            else:
                page_title = "No <title> tag/title found in the response."

        except requests.exceptions.Timeout:
            return "Timeout for requests."
        except requests.exceptions.ConnectionError:
            return "Connection Error !!!\nPlease check your internet connection."
        except requests.exceptions.SSLError as e:
            return f"SLL Error: {e}."
        except requests.exceptions.MissingSchema:
            return "Missing Schema Error : Invalid URL Format."
        except requests.exceptions.InvalidURL as e:
            return f"Invalid URL Error : {e}"

        # writing in a file:
        try:
            os.makedirs("temp", exist_ok=True)
            file_path = f"temp/curl_output_{domain}.txt"
            if os.path.exists(file_path):
                os.remove(file_path)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("-----------------------------CURL Report-----------------------------\n")
                file.write(f"Status code : {status_code}\n")
                file.write(f"Headers : {headers_json}\n")

                file.write("=======================================\n")
                if content_type == "text/html":
                    file.write("Reading HTML text from BeautifulSoap: \n\n")
                    file.write(f"Page title: {page_title}\n\n")
                    file.write("Readable text: \n")
                    file.write(f"{readable_text}\n")
                    file.write("=======================================\n")
                    file.write("-----------------------------End of CURL Report-----------------------------\n")
                else:
                    file.write("response is Non-HTML format.\n")
                    file.write("=======================================\n\n")
                    file.write("-----------------------------End of CURL Report-----------------------------\n")

            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"File writing failed.\nReason: {e}"

    except Exception as e:
        return f"CURL failed.\nReason: {e}"



# nslookup
def run_nslookup(domain):
    # Input : "google.com"
    try:
        dns_server = None
        ipv4_addresses = []
        ipv6_addresses = []
        cname = None

        result = subprocess.run(["nslookup", domain], capture_output=True, text=True)
        output_lines = result.stdout.splitlines()
        
        # appending the output
        for line in output_lines:
            # Removes leading and trailing spaces from the line.
            line = line.strip()

            # DNS server
            if line.lower().startswith("server:"):
                dns_server = line.split(":", 1)[1].strip()
            
            # cname
            if "canonical name" in line.lower():
                cname = line.split("=", 1)[1].strip()
            
            # IP
            if line.count('.') == 3:
                last_part = line.split()[-1]
                parts = last_part.split('.')
                if (len(parts) == 4) and (all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)):
                    ipv4_addresses.append(last_part)
            elif ":" in line:
                clean = line.replace("Address:", "").replace("Addresses:", "").strip()
                if all(c in "0123456789abcdefABCDEF:." for c in clean.replace(" ", "")):
                    ipv6_addresses.append(clean)

        # json dump
        ipv4_addresses = json.dumps(ipv4_addresses, indent=4)
        ipv6_addresses = json.dumps(ipv6_addresses, indent=4)

        # writing to file :
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/nslookup_output_{domain}.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "w") as file:
            file.write("-----------------------------Nslookup Report-----------------------------\n")
            file.write(f"Domain: {domain}\n")
            file.write(f"dns_server: {dns_server}\n")
            file.write(f"cname: {cname}\n")
            file.write(f"ipv4: {ipv4_addresses}\n")
            file.write(f"ipv6: {ipv6_addresses}\n")
            file.write("-----------------------------End of Nslookup Report-----------------------------\n")

        with open(file_path, "r") as file:
            return file.read()

    except:
        return "nslookup failed."



# network path trace
def run_networkPath(domain):
    # Input : "google.com"
    os_name = platform.system()
    command = ""

    try:
        # command
        if os_name == "Linux":
            command = ["traceroute", domain]
        elif os_name == "Windows":
            command = ["tracert", domain]

        # running command
        result = subprocess.run(command, capture_output=True, text=True)
        result_lines = result.stdout.splitlines()

        # writing file
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/track_{domain}.txt"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "w") as file:
            file.write("-----------------------Network path tracing Report-----------------------")
            for line in result_lines:
                file.write(f"{line}\n")
            file.write("-----------------------End of Network path tracing Report-----------------------\n")
        
        with open(file_path, "r") as file:
            return file.read()

    except:
        return "Network tarcking failed !!!"



if __name__ == "__main__":
    print(whois.__file__)
    print(os.path.join(os.path.dirname(whois.__file__), "data", "public_suffix_list.exe"))
