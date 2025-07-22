import os
import datetime
import time
from fpdf import FPDF
from validInput import isValidInput
from tools_runner import run_curl, run_Nmap, run_whois, run_nslookup, run_networkPath


def scan_domain(full_url, update_status):
    update_status(f"Scanning {full_url}")
    time.sleep(1)
    # Input: "https://www.google.com" not even pathway

    # no_protocol: www.google.com
    no_protocol = full_url.split("//")[-1]

    # domain: google.com
    domain = no_protocol.split(".")[1:]
    domain = ".".join(str(part) for part in domain)

    # second_level_domain: google
    second_level_domain = no_protocol.split(".")[1]



    # getting date
    running_time = datetime.datetime.now()
    running_24hrs = running_time.strftime("%H:%M:%S")
    running_date = running_time.strftime("%Y-%m-%d")



    # 1 WhoIs: Input("google.com")
    update_status("Running Whois...")
    time.sleep(1)
    whois_output = run_whois(domain)

    # 2 Nmap: Input("google.com")
    update_status("Running Nmap...")
    nmap_ouput = run_Nmap(domain)

    # 3 curl: Input("https://www.google.com" OR "https://google.com")
    update_status("Running Curl...")
    time.sleep(1)
    curl_output = run_curl(full_url)

    # 4 nslookup: Input(google.com)
    update_status("Running nslookup...")
    time.sleep(1)
    nslookup_output = run_nslookup(domain)

    # 5 Netwrok path: Input(google.com)
    update_status("Finding Network path...")
    network_path = run_networkPath(domain)



    # writing a final report.
    update_status("Writing file...")
    time.sleep(1)
    os.makedirs("output", exist_ok=True)
    text_file_path = f"output/{second_level_domain}-scan-report-{running_date}.txt"
    pdf_file_path = f"output/{second_level_domain}-scan-report-{running_date}.pdf"
    with open(text_file_path, "w", encoding="utf-8") as file:
        file.write("="*80 +"\n")
        file.write("WEBSITE RECONNAISSANCE REPORT".center(80) + "\n")
        file.write("="*80 +"\n")

        file.write(f"Scan Time: {running_date} {running_24hrs}\n")
        file.write(f"Scan URL: {full_url}.\n")
        file.write("== Tools Used ==\n")
        file.write("1. WHOIS\n")
        file.write("2. NMAP\n")
        file.write("3. CURL\n")
        file.write("4. NSLOOKUP\n")
        file.write("5. TRACEROUTE/TRACERT\n\n\n\n")

        file.write(whois_output + "\n\n\n\n")
        file.write(nmap_ouput + "\n\n\n\n")
        file.write(curl_output + "\n\n\n\n")
        file.write(nslookup_output + "\n\n\n\n")
        file.write(network_path + "\n\n\n\n")
        file.write("END OF REPORT")

    # converting to pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)

    with open(text_file_path, "r", encoding='utf-8') as file:
        for line in file:
            pdf.multi_cell(0, 10, txt=line.strip())

    pdf.output(pdf_file_path)

    update_status(f"Scanning complete.\nReport saved to '/{pdf_file_path}' AND '/{text_file_path}' ")


def run_scan(full_url, update_status):
    Input_Check = isValidInput(full_url)

    if Input_Check != 1:
        update_status(Input_Check)
    else:
        update_status("Input is valid.")
        time.sleep(1)
        scan_domain(full_url, update_status)

if __name__ == "__main__":
    pass
