## app.py

import re
import subprocess
import platform

def get_windows_wifi_passwords():
    wifi_data = {}
    try:
        profiles_data = subprocess.check_output("netsh wlan show profile", shell=True, text=True)
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_data)
        
        for profile in profiles:
            profile_info = subprocess.check_output(
                f'netsh wlan show profile name="{profile}" key=clear', shell=True, text=True
            )
            password = re.search(r"Key Content\s*:\s*(.*)", profile_info)
            wifi_data[profile] = password.group(1) if password else "No password found"
            
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Windows Wi-Fi passwords: {e}")
    return wifi_data

def get_linux_wifi_passwords():
    wifi_data = {}
    try:
        network_profiles = subprocess.check_output(
            "grep -r '^psk=' /etc/NetworkManager/system-connections/", shell=True, text=True
        ).splitlines()
        
        for profile in network_profiles:
            profile_path, password = profile.split(":psk=", 1)
            profile_name = profile_path.split("/")[-1]
            wifi_data[profile_name] = password.strip()
            
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Linux Wi-Fi passwords: {e}")
    return wifi_data

def main():
    system = platform.system().lower()
    if system == "windows":
        wifi_passwords = get_windows_wifi_passwords()
    elif system == "linux":
        wifi_passwords = get_linux_wifi_passwords()
    else:
        print("Unsupported OS")
        return

    if wifi_passwords:
        print("Wi-Fi Passwords:")
        max_length = max(len(wifi) for wifi in wifi_passwords.keys())        
        for wifi, password in wifi_passwords.items():
            print(f"{wifi:<{max_length}} : {password}")
    else:
        print("No Wi-Fi passwords found.")

if __name__ == "__main__":
    main()