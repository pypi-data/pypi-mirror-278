import os


def sysfs_str(*path):
    file = os.path.join(*path)
    if not os.path.isfile(file):
        return None
    with open(file, 'r') as handle:
        return handle.read().strip()


def sysfs_hex(*path):
    raw = sysfs_str(*path)
    if raw is None:
        return None

    return int(raw.strip(), 16)


def sysfs_int(*path):
    raw = sysfs_str(*path)
    if raw is None:
        return None

    return int(raw.strip())


def sysfs_float(*path):
    raw = sysfs_str(*path)
    if raw is None:
        return None

    return float(raw.strip())
