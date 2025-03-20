# Mean Well Modbus Monitor

A Python-based Modbus RTU monitor for Mean Well power supplies, using an Ethernet-to-Modbus RTU gateway.

## Features
- Reads voltage, current, and temperature data from MeanWell power supplies
- Displays real-time data in a terminal-based UI
- Allows toggling the power state remotely

## Supported Devices
This script supports Mean Well power supplies from the **DRS** series that feature Modbus RTU communication:

- **DRS-240-12**: 240W, 12V/20A
- **DRS-240-24**: 240W, 24V/10A
- **DRS-240-36**: 240W, 36V/6.6A
- **DRS-240-48**: 240W, 48V/5A
- **DRS-480-24**: 480W, 24V/20A
- **DRS-480-36**: 480W, 36V/13.3A
- **DRS-480-48**: 480W, 48V/10A

If your device is not listed but supports Modbus RTU, it might still work—feel free to test and report any issues!

## Modbus Configuration
Since MeanWell power supplies support only **Modbus RTU**, an **Ethernet-to-Modbus RTU gateway** is required for remote communication over TCP/IP.

### Recommended Modbus RTU settings:
- **Baud Rate:** 115200
- **Data Bits:** 8 bit
- **Parity:** None
- **Stop Bits:** 1 bit
- **Inter-frame Delay:** 8 ms
- **Response Timeout:** 250 ms

### How to Get a Modbus RTU → TCP Gateway
You have two options:

1. **Buy a ready-to-use gateway**  
   A high-quality Modbus RTU → TCP gateway is available from **nippy™** at [https://nippysmart.com/](https://nippysmart.com/).

2. **Build your own using Arduino**  
   If you prefer a DIY approach, you can create your own gateway based on Arduino. A complete guide and code are available in this GitHub repository:  
   [Arduino Modbus RTU to TCP Gateway](https://github.com/budulinek/arduino-modbus-rtu-tcp-gateway).

## Requirements
- Python 3.x
- `curses` for terminal UI
- A MeanWell power supply with Modbus RTU
- An Ethernet-to-Modbus RTU gateway (ready-made or DIY)

## Installation
Clone the repository and run the script:
```sh
git clone https://github.com/twoj-user/meanwell-modbus-monitor.git
cd meanwell-modbus-monitor
python3 meanwell-modbus-monitor.py
