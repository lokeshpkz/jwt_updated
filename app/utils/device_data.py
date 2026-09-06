import random
import ipaddress

# Realistic IP ranges (CIDR blocks) for Indian mobile ISPs
ISP_IP_RANGES = {
    "JIO": [
        "49.32.0.0/12",    # 49.32.0.0 - 49.47.255.255
        "157.44.0.0/15",   # 157.44.0.0 - 157.45.255.255
        "47.8.0.0/13"      # 47.8.0.0 - 47.15.255.255
    ],
    "AIRTEL": [
        "106.192.0.0/12",  # 106.192.0.0 - 106.207.255.255
        "171.76.0.0/14",   # 171.76.0.0 - 171.79.255.255
        "182.64.0.0/14"    # 182.64.0.0 - 182.67.255.255
    ],
    "VI": [
        "103.245.0.0/16",  # 103.245.0.0 - 103.245.255.255
        "223.176.0.0/12"   # 223.176.0.0 - 223.191.255.255
    ],
    "BSNL": [
        "117.192.0.0/12",  # 117.192.0.0 - 117.207.255.255
        "210.212.0.0/16"   # 210.212.0.0 - 210.212.255.255
    ]
}

# Real-world device profiles available in the market
DEVICE_PROFILES = [
    {
        "device_model": "realme RMX3085",
        "os_info": "Android OS 11 / API-30 (RKQ1.201112.002/eng.realme.20221110.193122)",
        "cpu_info": "ARM Cortex-A76/A55 | 2050 | 8",
        "total_ram": 6144,
        "gpu_name": "Mali-G76 MC4",
        "gpu_version": "OpenGL ES 3.2",
        "screen_width": 1080,
        "screen_height": 2400,
        "dpi": "409",
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 11; realme RMX3085 Build/RP1A.200720.011)"
    },
    {
        "device_model": "M2101K6I",  # Xiaomi Redmi Note 10 Pro
        "os_info": "Android OS 12 / API-31 (SP1A.210812.016/V13.0.10.0.SKFINXM)",
        "cpu_info": "ARM Cortex-A76/A55 | 2300 | 8",
        "total_ram": 8192,
        "gpu_name": "Adreno (TM) 618",
        "gpu_version": "OpenGL ES 3.2",
        "screen_width": 1080,
        "screen_height": 2400,
        "dpi": "395",
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2101K6I Build/SKQ1.210908.001)"
    },
    {
        "device_model": "SM-M325F",  # Samsung Galaxy M32
        "os_info": "Android OS 12 / API-31 (SP1A.210812.016/M325FXXU4BVI1)",
        "cpu_info": "ARM Cortex-A75/A55 | 2000 | 8",
        "total_ram": 6144,
        "gpu_name": "Mali-G52 MC2",
        "gpu_version": "OpenGL ES 3.2",
        "screen_width": 1080,
        "screen_height": 2400,
        "dpi": "411",
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 12; SM-M325F Build/SP1A.210812.016)"
    },
    {
        "device_model": "IV2201",  # OnePlus Nord CE 2 5G
        "os_info": "Android OS 11 / API-30 (RP1A.200720.011/eng.oneplus.20220311.142010)",
        "cpu_info": "ARM Cortex-A78/A55 | 2400 | 8",
        "total_ram": 8192,
        "gpu_name": "Mali-G68 MC4",
        "gpu_version": "OpenGL ES 3.2",
        "screen_width": 1080,
        "screen_height": 2400,
        "dpi": "409",
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 11; IV2201 Build/RP1A.200720.011)"
    },
    {
        "device_model": "vivo V2050",  # Vivo V21e
        "os_info": "Android OS 11 / API-30 (RP1A.200720.011/eng.vivo.20211215.183204)",
        "cpu_info": "ARM Cortex-A76/A55 | 2300 | 8",
        "total_ram": 8192,
        "gpu_name": "Adreno (TM) 618",
        "gpu_version": "OpenGL ES 3.2",
        "screen_width": 1080,
        "screen_height": 2400,
        "dpi": "409",
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 11; vivo V2050 Build/RP1A.200720.011)"
    }
]

def generate_random_ip(isp: str) -> str:
    """Generate a random valid IP within the subnet allocations of the specified ISP."""
    cidr_list = ISP_IP_RANGES.get(isp, ["182.75.115.0/24"])
    cidr = random.choice(cidr_list)
    network = ipaddress.IPv4Network(cidr)
    # Pick a random host index (excluding subnet and broadcast address)
    offset = random.randint(1, network.num_addresses - 2)
    return str(network[offset])

def get_random_profile():
    """Return a random device profile and a random Indian ISP network details."""
    isp = random.choice(list(ISP_IP_RANGES.keys()))
    ip_address = generate_random_ip(isp)
    profile = random.choice(DEVICE_PROFILES)
    return {
        "isp": isp,
        "ip_address": ip_address,
        **profile
    }
