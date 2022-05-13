# Lynx  
[![Coming Soon](https://img.shields.io/static/v1?label=status&message=coming-soon&color=yellow)]()

A prototype for voice based email system for the visually impaired.

## Usage

> NOTE: This project is tested only on R307 Optical fingerprint sensor. Other fingerprint sensor models/variants may require additional changes in the code.

### Setting up R307

To use the R307 sensor with a PC, you will need a USB to UART serial converter.  
Connect +5v, Ground, TXD and RXD from Fingerprint sensor to UART Bridge.  

Here's a R307 Pin diagram for your reference:  
<img src="https://i0.wp.com/circuitstate.com/wp-content/uploads/2021/05/R307-Fingerprint-Scanner-Pinout-2.png?resize=768%2C578&ssl=1" width="420">  

Once you have these connections in place, you can plug this sensor to your PC.

#### Windows Configuration
If you are using Windows (and R307 sensor), you have to install [this](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) driver. After this driver is installed, this sensor will be available at COM3 port. Check Device Manager to make sure this device is recognized.

#### Linux Configuration
If you are using linux, you do not need any additional drivers. This sensor will show up as `/dev/ttyUSB0`. But you will have to run the application as root so that it can access this port.

### Running

> **WARNING**: This software has a few security flaws that may compromise user credentials. Use with caution.  
  
Run `pip install -r requirements.txt` to install all the required packages.  
Plug in your R307 fingerprint sensor.  
Run `python main.py` to start the application.

## Links
[USB to UART Converter](https://robu.in/product/cp-2102-6-pin/?gclid=EAIaIQobChMIm8qx_Iyr9wIVZpJmAh2zTQKmEAQYAyABEgKh3_D_BwE)  
[R307 Fingerprint Sensor](https://robu.in/product/r307-optical-fingerprint-reader-module-sensor/?gclid=EAIaIQobChMIpvqjyY2r9wIVr5JmAh1iegNrEAQYASABEgIUkvD_BwE)  
[Connecting R307 to UART Bridge](https://circuitdigest.com/microcontroller-projects/raspberry-pi-fingerprint-sensor-interfacing)  
