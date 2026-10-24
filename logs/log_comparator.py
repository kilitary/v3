import re
import sys
from collections import defaultdict

def extract_log_data(filename):
    """Extract structured data from dmesg log"""
    data = {
        'memory_ranges': [],
        'device_ids': [],
        'driver_names': [],
        'hardware_info': [],
        'kernel_modules': [],
        'usb_devices': [],
        'filesystem_info': [],
        'network_config': [],
        'interrupts': [],
        'clocks': [],
        'power_domains': []
    }

    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return data

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        # Memory ranges
        mem_patterns = [
            r'mem (0x[0-9a-f]+)-(0x[0-9a-f]+)',
            r'memory pool at (0x[0-9a-f]+)',
            r'allocated \[mem (0x[0-9a-f]+)-(0x[0-9a-f]+)\]',
            r'DMA.*?(0x[0-9a-f]+)',
            r'phys_addr:(0x[0-9a-f]+)'
        ]
        for pattern in mem_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    data['memory_ranges'].append({
                        'line': line_num,
                        'range': match,
                        'context': line[:100]
                    })
                else:
                    data['memory_ranges'].append({
                        'line': line_num,
                        'address': match,
                        'context': line[:100]
                    })

        # Device IDs
        device_patterns = [
            r'idVendor=([0-9a-f]+)',
            r'idProduct=([0-9a-f]+)',
            r'CPU(\d+)',
            r'irq (\d+)',
            r'bus (\d+)',
            r'address (0x[0-9a-f]+)'
        ]
        for pattern in device_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                data['device_ids'].append({
                    'line': line_num,
                    'id': match,
                    'type': pattern.split('(')[0],
                    'context': line[:100]
                })

        # Driver names
        driver_patterns = [
            r'driver ([a-zA-Z0-9_-]+)',
            r'([a-zA-Z0-9_-]+): module',
            r'registered new.*driver ([a-zA-Z0-9_-]+)',
            r'([a-zA-Z0-9_-]+) [\d\w:.]+: ',
            r'Loading.*module ([a-zA-Z0-9_-]+)'
        ]
        for pattern in driver_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                if len(match) > 2 and not match.isdigit():  # Filter out short/numeric matches
                    data['driver_names'].append({
                        'line': line_num,
                        'driver': match,
                        'context': line[:100]
                    })

        # Hardware info
        if any(keyword in line.lower() for keyword in ['processor', 'cpu', 'machine model', 'hardware', 'board']):
            data['hardware_info'].append({
                'line': line_num,
                'info': line[:100]
            })

        # Kernel modules
        if 'module' in line.lower() and any(word in line.lower() for word in ['loaded', 'init', 'registered']):
            data['kernel_modules'].append({
                'line': line_num,
                'module': line[:100]
            })

        # USB devices
        if 'usb' in line.lower() and any(word in line.lower() for word in ['device', 'found', 'registered']):
            data['usb_devices'].append({
                'line': line_num,
                'device': line[:100]
            })

        # Filesystem info
        if any(fs in line.lower() for fs in ['ext4', 'fat', 'mounted', 'filesystem']):
            data['filesystem_info'].append({
                'line': line_num,
                'fs': line[:100]
            })

        # Network config
        if any(net in line.lower() for net in ['net:', 'tcp', 'udp', 'ip', 'protocol family']):
            data['network_config'].append({
                'line': line_num,
                'net': line[:100]
            })

        # Interrupts
        irq_match = re.search(r'irq (\d+)', line, re.IGNORECASE)
        if irq_match:
            data['interrupts'].append({
                'line': line_num,
                'irq': irq_match.group(1),
                'context': line[:100]
            })

        # Clock info
        if 'clock' in line.lower() or 'mhz' in line.lower() or 'hz' in line.lower():
            data['clocks'].append({
                'line': line_num,
                'clock': line[:100]
            })

        # Power domains
        if 'power' in line.lower() and any(word in line.lower() for word in ['domain', 'management', 'enabled']):
            data['power_domains'].append({
                'line': line_num,
                'power': line[:100]
            })

    return data

def compare_logs(data1, data2, log1_name, log2_name):
    """Compare two log datasets and find inconsistencies"""
    print(f"INCONSISTENCY ANALYSIS: {log1_name} vs {log2_name}")
    print("=" * 80)

    # Memory ranges comparison
    print("\n🔍 MEMORY RANGES ANALYSIS:")
    print("-" * 40)
    mem1_addrs = set()
    mem2_addrs = set()

    for mem in data1['memory_ranges']:
        if 'range' in mem:
            mem1_addrs.add(f"{mem['range'][0]}-{mem['range'][1]}")
        else:
            mem1_addrs.add(mem['address'])

    for mem in data2['memory_ranges']:
        if 'range' in mem:
            mem2_addrs.add(f"{mem['range'][0]}-{mem['range'][1]}")
        else:
            mem2_addrs.add(mem['address'])

    unique_to_log1 = mem1_addrs - mem2_addrs
    unique_to_log2 = mem2_addrs - mem1_addrs

    if unique_to_log1:
        print(f"Memory ranges only in {log1_name}:")
        for addr in sorted(unique_to_log1):
            print(f"  - {addr}")

    if unique_to_log2:
        print(f"Memory ranges only in {log2_name}:")
        for addr in sorted(unique_to_log2):
            print(f"  - {addr}")

    if not unique_to_log1 and not unique_to_log2:
        print("✅ Memory ranges are consistent")

    # Device IDs comparison
    print("\n🔍 DEVICE IDs ANALYSIS:")
    print("-" * 40)
    dev1_ids = {f"{d['type']}:{d['id']}" for d in data1['device_ids']}
    dev2_ids = {f"{d['type']}:{d['id']}" for d in data2['device_ids']}

    unique_dev1 = dev1_ids - dev2_ids
    unique_dev2 = dev2_ids - dev1_ids

    if unique_dev1:
        print(f"Device IDs only in {log1_name}:")
        for dev_id in sorted(unique_dev1):
            print(f"  - {dev_id}")

    if unique_dev2:
        print(f"Device IDs only in {log2_name}:")
        for dev_id in sorted(unique_dev2):
            print(f"  - {dev_id}")

    if not unique_dev1 and not unique_dev2:
        print("✅ Device IDs are consistent")

    # Driver names comparison
    print("\n🔍 DRIVER NAMES ANALYSIS:")
    print("-" * 40)
    drivers1 = {d['driver'].lower() for d in data1['driver_names'] if d['driver']}
    drivers2 = {d['driver'].lower() for d in data2['driver_names'] if d['driver']}

    unique_drivers1 = drivers1 - drivers2
    unique_drivers2 = drivers2 - drivers1

    if unique_drivers1:
        print(f"Drivers only in {log1_name}:")
        for driver in sorted(unique_drivers1):
            print(f"  - {driver}")

    if unique_drivers2:
        print(f"Drivers only in {log2_name}:")
        for driver in sorted(unique_drivers2):
            print(f"  - {driver}")

    if not unique_drivers1 and not unique_drivers2:
        print("✅ Driver names are consistent")

    # Hardware info comparison
    print("\n🔍 HARDWARE INFO ANALYSIS:")
    print("-" * 40)
    hw1_info = {h['info'].lower() for h in data1['hardware_info']}
    hw2_info = {h['info'].lower() for h in data2['hardware_info']}

    unique_hw1 = hw1_info - hw2_info
    unique_hw2 = hw2_info - hw1_info

    if unique_hw1:
        print(f"Hardware info only in {log1_name}:")
        for hw in list(unique_hw1)[:5]:  # Limit output
            print(f"  - {hw[:80]}...")

    if unique_hw2:
        print(f"Hardware info only in {log2_name}:")
        for hw in list(unique_hw2)[:5]:  # Limit output
            print(f"  - {hw[:80]}...")

    # Interrupt analysis
    print("\n🔍 INTERRUPT ANALYSIS:")
    print("-" * 40)
    irqs1 = {i['irq'] for i in data1['interrupts']}
    irqs2 = {i['irq'] for i in data2['interrupts']}

    unique_irqs1 = irqs1 - irqs2
    unique_irqs2 = irqs2 - irqs1

    if unique_irqs1:
        print(f"IRQs only in {log1_name}: {sorted(unique_irqs1)}")

    if unique_irqs2:
        print(f"IRQs only in {log2_name}: {sorted(unique_irqs2)}")

    if not unique_irqs1 and not unique_irqs2:
        print("✅ Interrupt assignments are consistent")

    # Summary statistics
    print("\n📊 SUMMARY STATISTICS:")
    print("-" * 40)
    categories = ['memory_ranges', 'device_ids', 'driver_names', 'hardware_info',
                 'kernel_modules', 'usb_devices', 'filesystem_info', 'network_config']

    print(f"{'Category':<20} {log1_name:<15} {log2_name:<15} Difference")
    print("-" * 65)
    for cat in categories:
        count1 = len(data1[cat])
        count2 = len(data2[cat])
        diff = abs(count1 - count2)
        print(f"{cat:<20} {count1:<15} {count2:<15} {diff}")

def main():
    print("Loading and analyzing log files...")

    log1_data = extract_log_data('dmesg.txt')
    log2_data = extract_log_data('dmesg2.txt')

    compare_logs(log1_data, log2_data, 'dmesg.txt', 'dmesg2.txt')

    print(f"\n🔍 Analysis complete!")

if __name__ == "__main__":
    main()
