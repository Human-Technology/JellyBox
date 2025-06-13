import subprocess
import os
import qrcode
import logging

class Command:
    """
    Encapsulates system commands: network, USB, website, power.
    """

    def get_name_access_point(self) -> str:
        """
        Gets the name of the wireless connection on wlan0.
        """
        try:
            cmd = "nmcli -t -f NAME,DEVICE connection show | grep wlan0 | cut -d':' -f1"
            return subprocess.check_output(cmd, shell=True, text=True).strip()
        except Exception as e:
            logging.error(f"Error getting access point name: {e}", exc_info=True)
            return "No disponible"
    
    def get_SSID(self) -> str:
        """
        Reads the SSID of the access point.
        """
        try:
            arg1 = "'{print $2}'"
            ap = self.get_name_access_point()
            cmd = f"nmcli connection show {ap} | grep 802-11-wireless.ssid | awk {arg1}"
            return subprocess.check_output(cmd, shell=True, text=True).strip()
        except Exception as e:
            logging.error(f"Error getting SSID: {e}", exc_info=True)
            return "Not available"
       
    def get_password_access_point(self) -> str:
        """
        Extracts the PSK password from the NetworkManager configuration file.
        """
        try:
            ap = self.get_name_access_point()
            path = f"/etc/NetworkManager/system-connections/{ap}.nmconnection"
            content = subprocess.check_output(f"sudo grep psk= {path}", shell=True, text=True)
            return content.split('=', 1)[1].strip()
        except Exception as e:
            logging.error(f"Error getting access point password: {e}", exc_info=True)
            return "Not available"

    def get_ip_access_point(self) -> str:
        """
        Returns the IP assigned to wlan0 or an error message.
        """
        try:
            res = subprocess.run(["ip", "-o", "-4", "addr", "show", "wlan0"], 
                                    capture_output=True, text=True)
            return res.stdout.split()[3].split('/')[0]
        except Exception as e:
            logging.error(f"Error getting access point IP: {e}", exc_info=True)
            return "Not available"
    
    def get_qr_access_point(self) -> None:
        """
        Generates a QR code to share the Wi-Fi network and saves it as wifi_qr.png.
        """
        try:
            ssid = self.get_SSID()
            password = self.get_password_access_point()
            encryption = "WPA"
            wifi_qr_data = f"WIFI:S:{ssid};T:{encryption};P:{password};;"
            qr = qrcode.make(wifi_qr_data)
            qr.save("wifi_qr.png")
        except Exception as e:
            logging.error(f"Error generating Wi-Fi QR: {e}", exc_info=True)
        
    def get_device_usb(self) -> list[dict]:
        """
        Lists FAT/ExFAT formatted USB devices larger than 1GB.
        """
        try:
            cmd = ("lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT | awk '$2 ~ /(G|T)$/ "
                    "&& $2+0 > 1 && $3 ~ /fat32|exfat|vfat/'")
            out = subprocess.check_output(cmd, shell=True, text=True)
            devices = []
            for line in out.splitlines():
                parts = line.split()
                if len(parts) >= 3:
                    devices.append({
                        "NAME": parts[0].lstrip("└─"),
                        "SIZE": parts[1],
                        "FSTYPE": parts[2],
                        "MOUNTPOINT": parts[3] if len(parts) > 3 else None
                    })
            return devices
        except Exception as e:
            logging.error(f"Error getting USB devices: {e}", exc_info=True)
            return []
    
    def get_devices_len(self) -> int:
        """
        Returns the number of detected USB devices.
        """
        return len(self.get_device_usb())
    
    def mount_device(self, index: int) -> None:
        """
        Mounts the USB device at the specified index.
        """
        try:
            devices = self.get_device_usb()
            device = devices[index]
            subprocess.run(["sudo", "mkdir", "-p", f"/mnt/usb{index}"])
            subprocess.run(["sudo", "mount", f"/dev/{device['NAME']}", f"/mnt/usb{index}"])
            subprocess.run([
                "sudo", "bash", "-c",
                f"echo '/dev/{device['NAME']}\t/mnt/usb{index}\t{device['FSTYPE']}\tnofail\t0\t2' >> /etc/fstab"
            ])
        except Exception as e:
            logging.error(f"Error mounting USB device: {e}", exc_info=True)

    def umount_device(self, index: int) -> None:
        """
        Unmounts the USB device at the specified index and removes its entry from fstab.
        """
        try:
            device = self.get_device_usb()[index]
            subprocess.run(["sudo", "umount", f"{device['MOUNTPOINT']}"])
            subprocess.run(["sudo", "rm", "-r", f"{device['MOUNTPOINT']}"])
            f = f"/\\/dev\\/{device['NAME']}[[:space:]]*\\/mnt\\/usb{index}[[:space:]]*{device['FSTYPE']}[[:space:]]*nofail[[:space:]]*0[[:space:]]*2/d"
            sed_command = [
                "sudo", "sed", "-i",
                f,
                "/etc/fstab"
            ]
            subprocess.run(sed_command, check=True)
        except Exception as e:
            logging.error(f"Error unmounting USB device: {e}", exc_info=True)

    def custom_device(self, index: int) -> None:
        """
        Mounts or unmounts the USB device at the given index depending on its current state.
        """
        try:
            device = self.get_device_usb()[index]
            if device['MOUNTPOINT']:
                self.umount_device(index)
            else:
                self.mount_device(index)
        except Exception as e:
            logging.error(f"Error in custom_device: {e}", exc_info=True)

    def update_website(self, template_name: str) -> None:
        """
        Copies the selected HTML template to index.html in Apache, inserting the local IP.
        """
        try:
            base = os.path.dirname(__file__)
            src = os.path.join(base, "../web_templates", f"{template_name}.html")
            dst = "/var/www/html/index.html"
            ip_local = self.get_ip_access_point()

            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            content = content.replace("{{IP_LOCAL}}", ip_local)
            with open("/tmp/index.html", "w", encoding="utf-8") as f:
                f.write(content)
            subprocess.run(["sudo", "cp", "/tmp/index.html", dst])
        except Exception as e:
            logging.error(f"Error updating website: {e}", exc_info=True)

    def shut_down_system(self) -> None:
        """
        Safely shuts down the system.
        """
        try:
            subprocess.run(["sudo", "shutdown", "now"])
        except Exception as e:
            logging.error(f"Error shutting down the system: {e}", exc_info=True)

    def reboot_system(self) -> None:
        """
        Safely reboots the system.
        """
        try:
            subprocess.run(["sudo", "reboot"])
        except Exception as e:
            logging.error(f"Error rebooting the system: {e}", exc_info=True)