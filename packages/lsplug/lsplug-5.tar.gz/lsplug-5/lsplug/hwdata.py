import os

_cache = None


def load_database():
    global _cache
    dbfile = '/usr/share/hwdata/usb.ids'
    if not os.path.isfile(dbfile):
        return False

    vendor = None
    product = None

    _cache = {}

    with open(dbfile, 'rb') as handle:
        for line in handle.readlines():
            if line.startswith(b'#') or line.startswith(b'\n'):
                continue
            line = line.decode('utf-8', errors="ignore")

            if line.startswith('C '):
                break

            if line[0] != '\t':
                vendor_id, name = line.split("  ", maxsplit=1)
                vendor = int(vendor_id, 16)
                _cache[vendor] = {'name': name.strip(), 'products': {}}
            elif line[1] != '\t':
                product_id, name = line.strip().split("  ", maxsplit=1)
                product = int(product_id, 16)
                _cache[vendor]['products'][product] = {'name': name}
    return True


def get_vendor(vendor_id):
    if _cache is None:
        load_database()
    if vendor_id not in _cache:
        return None
    return _cache[vendor_id]['name']


def get_product(vendor_id, product_id):
    if _cache is None:
        load_database()
    if vendor_id not in _cache:
        return None
    if product_id not in _cache[vendor_id]['products']:
        return None
    return _cache[vendor_id]['products'][product_id]['name']


if __name__ == '__main__':
    load_database()
