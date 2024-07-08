# Jetson Orin Nano Setup Guide

This document provides a step-by-step guide for setting up the Jetson Orin Nano. 

## Hardware Requirements

- Jetson Orin Nano Developer Kit
- Power supply (5V 4A USB-C adapter)
- MicroSD card (minimum 16GB, recommended 32GB or more)
- DisplayPort cable, DisplayPort capable monitor 
- USB keyboard and mouse
- Internet connection (Ethernet cable or USB Wi-Fi adapter)

## Software Requirements

- **JetPack SDK**: The latest version of JetPack, which includes the OS and necessary libraries. Download from [NVIDIA's official site](https://developer.nvidia.com/embedded/jetpack).
- **Balena Etcher**: For flashing the MicroSD card. Download from [here](https://www.balena.io/etcher/).

## Setup Steps

1. **Download JetPack SDK**
   - Visit the [NVIDIA JetPack SDK page](https://developer.nvidia.com/embedded/jetpack) and download the latest version.

2. **Prepare the MicroSD Card**
   - Insert the MicroSD card into your computer.
   - Use Balena Etcher to flash the JetPack SDK image onto the MicroSD card.
     - Open Balena Etcher.
     - Select the JetPack SDK image file.
     - Select the target MicroSD card.
     - Click 'Flash' to begin.

3. **Assemble the Jetson Orin Nano**
   - Insert the flashed MicroSD card into the Jetson Orin Nano slot.
   - Connect the HDMI monitor, USB keyboard, and mouse.
   - Connect the power supply.

4. **Initial Boot and Configuration**
   - Power on the Jetson Orin Nano.
   - Follow the on-screen instructions to complete the initial setup.
     - Configure language, time zone, and network settings.
     - Create a username and password.

5. **Update and Install Additional Packages**
   - Open a terminal and update the system:
     ```bash
     sudo apt-get update
     sudo apt-get upgrade
     ```
   - Install additional libraries and tools as needed for your projects:
     ```bash
     sudo apt-get install <package-name>
     ```

## Testing and Verification

To verify that the setup is successful:

1. **Check JetPack Installation**
   - Open the terminal and run:
     ```bash
     sudo apt list --installed | grep nvidia
     ```

2. **Run a Sample Program**
   - Navigate to the sample directory and run a pre-installed sample:
     ```bash
     cd /usr/src/nvidia/graphics_demos
     ./sample_graphics_app
     ```

## Troubleshooting

### Common Issues

- **Display Not Working**
  - Ensure the HDMI cable is properly connected.
  - Try using a different HDMI cable or monitor.

- **Network Connection Issues**
  - Check the Ethernet cable connection.
  - For Wi-Fi, ensure the adapter is recognized by the system:
    ```bash
    lsusb
    ```

- **Power Supply Problems**
  - Verify that the power supply meets the required specifications (5V 4A).

## Additional Resources

- [NVIDIA Jetson Orin Nano Developer Kit User Guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit)
- [JetPack SDK Documentation](https://developer.nvidia.com/embedded/jetpack)
- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/c/agx-autonomous-machines/Jetson/)

