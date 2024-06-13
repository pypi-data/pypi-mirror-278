import hashlib
import os
import platform
import sys
import psutil

async def get_fingerprinting_info():
    system_info = platform.uname()
    bios_info = platform.libc_ver()
    cpu_info = {
        "manufacturer": platform.processor(),
        "brand": platform.machine(),
        "speedMax": psutil.cpu_freq().max,
        "cores": psutil.cpu_count(logical=False),
        "physicalCores": psutil.cpu_count(logical=True),
    }
    mem_info = {
        "total": psutil.virtual_memory().total,
    }
    os_info_data = {
        "platform": system_info.system,
        "arch": system_info.machine,
    }
    devices = psutil.disk_partitions()
    hdds = [f"{device.device}{device.fstype}" for device in devices if not psutil.disk_usage(device.mountpoint).free == 0]

    return {
        "EOL": os.linesep,
        "endianness": "little" if sys.byteorder == "little" else "big",
        "manufacturer": system_info.node,
        "model": system_info.system,
        "serial": system_info.version,
        "uuid": system_info.machine,
        "vendor": bios_info[0],
        "biosVersion": bios_info[1],
        "releaseDate": "N/A",
        "boardManufacturer": "N/A",
        "boardModel": "N/A",
        "boardSerial": "N/A",
        "cpuManufacturer": cpu_info['manufacturer'],
        "brand": cpu_info['brand'],
        "speedMax": f"{cpu_info['speedMax']:.2f}",
        "cores": cpu_info['cores'],
        "physicalCores": cpu_info['physicalCores'],
        "socket": "N/A",
        "memTotal": mem_info['total'],
        "platform": os_info_data['platform'],
        "arch": os_info_data['arch'],
        "hdds": hdds,
    }

async def get_fingerprinting_parameters():
    info = await get_fingerprinting_info()
    return list(info.keys())

def calculate_fingerprint(parameters):
    fingerprint_string = ''.join(str(parameters[param]) for param in sorted(parameters) if param in parameters)
    fingerprint_hash = hashlib.sha512(fingerprint_string.encode())
    return fingerprint_hash.digest()

cached_fingerprints = {}

async def get_fingerprint(options=None):
    if options is None:
        options = {}
    default_parameters = await get_fingerprinting_parameters()
    only = options.get('only', default_parameters)
    except_params = options.get('except', [])
    parameters = [param for param in default_parameters if param in only and param not in except_params]
    cache_key = ''.join(parameters)
    if cache_key not in cached_fingerprints:
        info = await get_fingerprinting_info()
        selected_info = {param: info[param] for param in parameters}
        cached_fingerprints[cache_key] = calculate_fingerprint(selected_info)
    return cached_fingerprints[cache_key]
