import tkinter as tk
from tkinter import ttk

import subprocess
import re

def get_connected_wifi_and_password():
    def get_wifi_password(wifi_name):
        try:
            # Run netsh command to get Wi-Fi profile information
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', 'name=' + wifi_name, 'key=clear'], capture_output=True, text=True, check=True)

            # Extract the password from the output using regular expressions
            key_content = re.search(r'Key Content\s+:\s(.+)', result.stdout)
            if key_content:
                return key_content.group(1)
            else:
                return "Password not found"
        except subprocess.CalledProcessError as e:
            return "Error: " + e.stderr.strip()

    try:
        # Run netsh command to get connected Wi-Fi network
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, check=True)
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if "SSID" in line:
                ssid = line.strip().split(": ")[1]
                password = get_wifi_password(ssid)
                return ssid, password
        return None, None
    except subprocess.CalledProcessError as e:
        return "Error: " + e.stderr.strip(), None

def show_wifi_info():
    wifi_name, password = get_connected_wifi_and_password()
    if wifi_name:
        info_label.config(text=f"Connected to WiFi: {wifi_name}\nWi-Fi Password: {password}")
    else:
        info_label.config(text="Not connected to any WiFi network.")

# Create Tkinter window
root = tk.Tk()
root.title("Wi-Fi Info")
root.geometry("245x105")

# Create and pack label
info_label = tk.Label(root, text="Check wifi name and password.", font=("Helvetica", 11))
info_label.pack(pady=1)

# Create a style using ttkbootstrap
style = ttk.Style()

# Configure the style to outline the button with blue color
style.map("Outline.TButton", bordercolor=[("active", "#007bff")], relief=[("active", "solid")])

# Set the padding to adjust the button size
style.configure("Outline.TButton", padding=(10, 5))  # Adjust padding as needed

# Create and pack button with Bootstrap-like styling
button = ttk.Button(root, text="Show Wi-Fi Info", command=show_wifi_info, style="Outline.TButton")
button.pack(side="bottom", pady=15)

# Run Tkinter event loop
root.mainloop()
