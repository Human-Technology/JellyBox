# JellyBox

**JellyBox** is a portable media server based on a Raspberry Pi that allows you to carry your movies, shows, and music anywhere, without the need for an internet connection. It creates its own Wi-Fi hotspot, plays content from a USB drive or external disk, and optionally includes a TFT-ST7789 display for a local interface.

## Project Structure

```
📂 JellyBox
 ├── 📂 Connection Diagram/        # Hardware connection diagram
 ├── 📂 input/                     # Button logic
 ├── 📂 interface/                 # Interface logic
 ├── 📂 web_templates/             # HTML web templates
 ├── main.py                   # Main script
 ├── modules.txt               # Dependencies
 ├── README.md                 # Documentation
 └── LICENSE                   # Project license
```

## Features

- **Portable**: Powered by a USB-C battery.
- **Own Wi-Fi**: Creates a hotspot to connect devices.
- **Jellyfin**: Open-source media server.
- **Local Interface** (optional): Use a TFT-ST7789 display and buttons to navigate.
- **Código abierto**: Modify and customize to fit your needs.

## Required Hardware

- Raspberry Pi (4B with 2GB RAM or 3B+)
- MicroSD (at least 32GB, preferably high-speed)
- TFT-ST7789 Display (optional)
- 3 Buttons (optional, for menu)
- Breadboard and jumper wires
- Internet connection (for initial setup only)
- USB-C portable battery

## 1. Install the Operating System

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
2. Select **Raspberry Pi OS Lite** (64 bits recommended).
3. Configure SSH, username (`human`), password and timezone in advanced settings (`Ctrl + Shift + X`).
4. Flash the image to the MicroSD.

## 2. Connect and Update

1. Insert the MicroSD into the Pi and power it on.
2. Connect via SSH:

```sh
ssh human@raspberrypi
```

3. Update the system:

```sh
sudo apt update && sudo apt upgrade -y
```

## 3. Set Up Wi-Fi Access Point

1. Set the region for proper Wi-Fi functionality:

```sh
sudo raspi-config
```

Go to option 5. "Localisation Options" > "WLAN Country", select your country, and reboot:

```sh
sudo reboot
```

2. Create the Wi-Fi network:

```sh
sudo nmcli connection add type wifi ifname wlan0 con-name jellyfin_ap autoconnect yes ssid JellyBox
```

3. Set up security:

```sh
sudo nmcli connection modify jellyfin_ap wifi-sec.key-mgmt wpa-psk
sudo nmcli connection modify jellyfin_ap wifi-sec.psk "password"
```

4. Assign a static IP:

```sh
sudo nmcli connection modify jellyfin_ap ipv4.method shared
sudo nmcli connection modify jellyfin_ap ipv4.addresses 192.168.1.1/24
```

5. Configure as access point:

```sh
sudo nmcli connection modify jellyfin_ap 802-11-wireless.mode ap
sudo nmcli connection modify jellyfin_ap connection.interface-name wlan0
```

6. Activate the network:

```sh
sudo nmcli connection up jellyfin_ap
```

If the network doesn't appear, change the channel:

```sh
sudo nmcli connection modify jellyfin_ap 802-11-wireless.band bg 802-11-wireless.channel 6
sudo nmcli connection up jellyfin_ap
```

## 4. Install Jellyfin

```sh
curl -s https://repo.jellyfin.org/install-debuntu.sh | sudo bash
```

## 5. Set Up Local Web Server (optional)

```sh
sudo apt install lighttpd
sudo systemctl enable --now lighttpd
```

## 6. Set Up TFT-ST7789 Display (optional)

1. Enable SPI:

```sh
sudo raspi-config nonint do_spi 0
```

2. Connect the display:

| Nombre LCD | Nombre PI | Pin GPIO PI |
| ---------- | --------- | ----------- |
| GND        | GND       | 6           |
| VCC        | 3.3V      | 1           |
| SCL        | SCLK      | 23          |
| SDA        | MOSI      | 19          |
| RES        | GPIO 25   | 22          |
| DC         | GPIO 24   | 18          |
| CS         | CE0       | 24          |
| BLK        | GPIO 18   | 12          |

Raspberry Pi GPIO Pins

![pines GPIO raspberry pi](https://github.com/user-attachments/assets/284f4cba-bc72-45ba-8055-d51c39fdab08)

LCD Display Pins

![display](https://github.com/user-attachments/assets/1b0daac0-9910-4627-94f6-acf1d3b0b0e3)

Overall Connection

![JellyBox_Connection_diagram](https://github.com/user-attachments/assets/f44c2290-ce1e-4a3b-accb-e240ae4cfa84)


## 7. Prepare Python Environment

1. Install dependencies:

```sh
sudo apt install python3-dev python3-pip python3-setuptools
```

2. Clone the repository:

```sh
git clone https://github.com/Human-Technology/JellyBox.git
cd JellyBox
```

3. Create virtual environment:

```sh
python -m venv .env
source .env/bin/activate
```

4. Upgrade pip and install dependencies:

```sh
pip install --upgrade pip
pip install -r modules.txt
```

## 8. Create Systemd Service

1. Create the file:

```sh
sudo nano /etc/systemd/system/jellybox.service
```

2. Add the following:

```ini
[Unit]
Description=Servicio JellyBox
After=network.target

[Service]
ExecStart=/home/human/JellyBox/.env/bin/python /home/human/JellyBox/main.py
WorkingDirectory=/home/human/JellyBox
User=human
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

*Adjust paths and username according to your setup.*

3. Enable and start the service:

```sh
sudo systemctl daemon-reload
sudo systemctl enable jellybox.service
sudo systemctl start jellybox.service
```

4. Reboot to test:

```sh
sudo reboot
```

## Usage

- Plug in a USB drive with media content.
- Access Jellyfin from any device connected to the hotspot: `http://192.168.1.1:8096`
- Use the display and buttons to navigate options: mount/unmount USB, change interface, view IP, shutdown/reboot.

## Contribute

Feel free to open issues or pull requests! Give the project a star if you liked it.

## Contact

- Blog: [link to your blog]
- YouTube: [link to your video]
- X/Twitter: [link to your profile]

Enjoy your JellyBox and bring your entertainment anywhere!
