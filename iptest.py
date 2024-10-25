import requests
import json


def query_ip_location(ip_address):
    url = f"https://ip.useragentinfo.com/json?ip={ip_address}"
    payload = {}
    headers = {}
    response = requests.get(url, headers=headers, data=payload)
    if response.status_code == 200:
        try:
            data = response.json()
            country = data.get("country", "Unknown")
            province = data.get("province", "Unknown")
            city = data.get("city", "Unknown")
            isp = data.get("isp", "Unknown")
            net = data.get("net", "Unknown")
            return country, province, city, isp, net
        except json.JSONDecodeError:
            return "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"
    else:
        return "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"


# Example usage:
ip_address = "8.218.192.192"  # Replace this with the IP address you want to query
country, province, city, isp, net = query_ip_location(ip_address)
print(f"The IP address {ip_address} is located in {city}, {province}, {country}.")
print(f"The ISP of this IP address is {isp}, and it's using {net} network.")