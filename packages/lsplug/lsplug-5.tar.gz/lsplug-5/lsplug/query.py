import glob
import os
import sqlite3

from lsplug.helpers import sysfs_str, sysfs_hex, sysfs_int
from lsplug.hwdata import get_vendor, get_product

db = sqlite3.connect(':memory:')


def init():
    cur = db.cursor()
    cur.execute("CREATE TABLE usb("
                "bus INTEGER, "
                "port TEXT, "
                "portname TEXT, "
                "device INTEGER, "
                "removable INTEGER, "
                "vid INTEGER, "
                "pid INTEGER, "
                "vendor TEXT, "
                "product TEXT,"
                "version TEXT,"
                "serial TEXT,"
                "vendor_raw TEXT,"
                "product_raw TEXT,"
                "device_class INT,"
                "device_subclass INT,"
                "device_protocol INT,"
                "max_packet_size INT,"
                "max_power INT,"
                "speed INTEGER"
                ")")

    data = []
    for port in glob.glob('/sys/bus/usb/devices/*'):
        name = os.path.basename(port)
        if ':' in name:
            continue
        if 'usb' in name:
            continue

        bus, bus_port = name.split('-', maxsplit=1)
        device = sysfs_int(port, "devnum")
        removable = 1 if sysfs_str(port, "removable") == "removable" else 0
        product_raw = sysfs_str(port, "product")
        vendor_raw = sysfs_str(port, "manufacturer")
        version = sysfs_str(port, "version")
        serial = sysfs_str(port, "serial")
        pid = sysfs_hex(port, "idProduct")
        vid = sysfs_hex(port, "idVendor")
        speed = sysfs_int(port, "speed")

        vendor_db = get_vendor(vid)
        product_db = get_product(vid, pid)
        if vendor_db is not None:
            vendor = vendor_db
        else:
            vendor = vendor_raw
        if product_db is not None:
            product = product_db
        else:
            product = product_raw

        device_class = sysfs_hex(port, "bDeviceClass")
        device_subclass = sysfs_hex(port, "bDeviceSubClass")
        device_protocol = sysfs_hex(port, "bDeviceProtocol")
        max_packet_size = sysfs_int(port, "bMaxPacketSize0")
        max_power = sysfs_str(port, "bMaxPower")
        if max_power is not None:
            max_power = int(max_power.replace("mA", ""))

        data.append((bus, bus_port, name, device, removable, vid, pid, vendor, product, version, serial, vendor_raw,
                     product_raw, device_class, device_subclass, device_protocol, max_packet_size, max_power, speed))

    cur.executemany(
        "INSERT INTO usb (bus, port, portname, device, removable, vid, pid, vendor, product, version, serial, vendor_raw, product_raw, device_class, device_subclass, device_protocol, max_packet_size, max_power, speed) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        data)


def query(sql):
    cur = db.cursor()
    res = cur.execute(sql)
    fmt_bool = ['removable']
    fmt_hex2 = ['device_class', 'device_subclass', 'device_protocol']
    fmt_hex4 = ['vid', 'pid']
    columns = list(map(lambda x: x[0], res.description))
    result = []
    for row in res:
        newrow = []
        for i, field in enumerate(row):
            if columns[i] in fmt_bool:
                field = 'yes' if field > 0 else 'no'
            elif columns[i] in fmt_hex2:
                field = f'{field:02X}'
            elif columns[i] in fmt_hex4:
                field = f'{field:04x}'
            newrow.append(field)
        result.append(newrow)
    import tabulate
    print(tabulate.tabulate(result, headers=columns))


if __name__ == '__main__':
    init()
    query("SELECT * FROM usb ORDER BY bus, port")
