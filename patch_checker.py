#/usr/bin/env python3

import subprocess
import requests

UBUNTU_SECURITY_URL = "https://ubuntu.com/security/notices.json"

def get_upgradable_packages():
    try:
        result = subprocess.run(['apt', 'list', '--upgradable'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout.splitlines()

        # Skip the "Listing..." line
        packages = []
        for line in output [1:]:
            package_info = line.split('/')
            if package_info:
                package_name = package_info[0]
                packages.append(package_name)

        return packages
    
    except subprocess.CalledProcessError as e:
        print(f"Error running apt command: {e}")
        return []

def fetch_ubuntu_cves():
    try:
        response = requests.get(UBUNTU_SECURITY_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching CVE data: {e}")
        return []

def find_package_cves(packages, cve_data):
    affected = {}

    for notice in cve_data:
        summary = notice.get("summary", "")
        cves = notice.get("cves", [])
        affected_packages = notice.get("packages", [])

        for pkg in affected_packages:
            pkg_name = pkg.get("name")
            if pkg_name in packages:
                if pkg_name not in affected:
                    affected[pkg_name] = []
                affected[pkg_name].extend(cves)

    return affected

def main():
    print("[+] Checking for available package updates...\n")
    upgradable = get_upgradable_packages()

    if not upgradable:
        print("[-] No upgrades available. System is up to date.")
        return
    else:
        print("[!] The following packages can be upgraded:")
        for pkg in upgradable:
            print(f" - {pkg}")

    print("\n[+] Checking for known CVEs affecting upgradable packages...\n")
    cve_data = fetch_ubuntu_cves()
    affected = find_package_cves(upgradable, cve_data)

    if affected:
        print("[!] Critical CVEs found for the following packages:")
        for pkg, cves in affected.items():
            print(f" - {pkg}: {', '.join(cves)}")
    else:
        print("[+] No known CVEs affecting upgradable packages.")

if __name__ == "__main__":
    main()