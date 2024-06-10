# lsplug

Replacement for `lsusb` that shows more useful info and less useless info.

```
usage: lsplug [-h] [--no-db] [--no-fixed] [--portinfo] [--devinfo]
              [--interfaces]
              [filter ...]

USB listing tool

positional arguments:
  filter            Filter on port numbers

options:
  -h, --help        show this help message and exit
  --no-db, -n       Don't use the hardware database for names
  --no-fixed, -r    Don't show non-removable usb devices
  --portinfo, -p    Show detailed port data
  --devinfo, -d     Show detailed kernel device info
  --interfaces, -i  Show detailed interface info
```

## Features

* Shows the usb port number instead of the bus number and device id
* The `-r / --no-fixed` option will hide usb devices that are not marked removable. This should hide all the
  built-in USB devices on laptops like card readers and webcams.
* The `-p / --portinfo` option will show the speed the USB device is connected at and the maximum current limit
  it has requested.
* The `-d / --devinfo` option will use heuristics to match up the USB device with the `/dev` device node(s).
* The `-i / --interfaces` option will show the USB class and interfaces from the device descriptor
* The `-n / --no-db` option will disable loading the `/usr/share/hwdata/usb.ids` file and show the contents of
  the descriptors itself only.

## Examples

```shell-session
Just show all the USB devices in my laptop
# lsplug
USB 2-3  [0781:cfd2] SanDisk Corp. SDDR-399 Reader [110716551151]
USB 1-7  [1770:ff00] MSI steel series rgb keyboard [MSI EPF USB]
USB 1-12 [0bda:0129] Realtek Semiconductor Corp. RTS5129 Card Reader Controller [20100201396000000]
USB 1-10 [8087:0aa7] Intel Corp. Wireless-AC 3168 Bluetooth
USB 1-8  [1050:0116] Yubico.com Yubikey NEO(-N) OTP+U2F+CCID
USB 1-11 [04f2:b521] Chicony Electronics Co., Ltd USB 2.0 Webcam Device [200901010001]
USB 1-4  [1a86:7523] QinHeng Electronics CH340 serial converter

Only show the devices that are actually in an external USB port
# lsplug -r
USB 2-3  [0781:cfd2] SanDisk Corp. SDDR-399 Reader [110716551151]
USB 1-8  [1050:0116] Yubico.com Yubikey NEO(-N) OTP+U2F+CCID
USB 1-4  [1a86:7523] QinHeng Electronics CH340 serial converter

Show the associated device nodes for the USB device
# lsplug -r -d
USB 2-3  [0781:cfd2] SanDisk Corp. SDDR-399 Reader [110716551151]
   Device /dev/sdb
USB 1-8  [1050:0116] Yubico.com Yubikey NEO(-N) OTP+U2F+CCID
   Device /dev/usb/hiddev0
USB 1-4  [1a86:7523] QinHeng Electronics CH340 serial converter
   Device /dev/ttyUSB0

Select my built-in webcam on port 1-11 and show the device nodes
# lsplug -d 1-11
USB 1-11 [04f2:b521] Chicony Electronics Co., Ltd USB 2.0 Webcam Device [200901010001]
   Device /dev/video1
   Device /dev/video0
   Device /dev/media0
   Device /dev/input/event18
   
Show the USB interface descriptors instead
# lsplug -i 1-11
USB 1-11 [04f2:b521] Chicony Electronics Co., Ltd USB 2.0 Webcam Device [200901010001]
   Class EF SubClass 02 Protocol 01
      Interface 0 0E/01/00 USB 2.0 Webcam Device
      Interface 1 0E/02/00 Unknown
   
Show the USB speed and reported max power usage of the devices connected to my laptop
# lsplug -r -p
USB 2-3  [0781:cfd2] SanDisk Corp. SDDR-399 Reader [110716551151]
   Speed: 5.0 Gbps 1x1, MaxPower: 896mA
USB 1-8  [1050:0116] Yubico.com Yubikey NEO(-N) OTP+U2F+CCID
   Speed: 12 Mbps, MaxPower: 30mA
USB 1-4  [1a86:7523] QinHeng Electronics CH340 serial converter
   Speed: 12 Mbps, MaxPower: 100mA
```

## Contributing

Send patches to via `git send-email`:

```
git config sendemail.to '~martijnbraam/public-inbox@lists.sr.ht'
git config format.subjectPrefix 'PATCH lsplug'
git send-email FIRST_COMMIT~
```
