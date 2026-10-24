import re
import difflib
from collections import defaultdict

def detailed_log_comparison():
    """Perform detailed line-by-line comparison of the two dmesg logs"""

    try:
        with open('dmesg.txt', 'r', encoding='utf-8', errors='ignore') as f1:
            lines1 = f1.readlines()
        with open('dmesg2.txt', 'r', encoding='utf-8', errors='ignore') as f2:
            lines2 = f2.readlines()
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    print("DETAILED INCONSISTENCY ANALYSIS")
    print("=" * 80)

    # Basic stats
    print(f"📊 FILE STATISTICS:")
    print(f"  dmesg.txt:  {len(lines1)} lines")
    print(f"  dmesg2.txt: {len(lines2)} lines")
    print(f"  Line count difference: {abs(len(lines1) - len(lines2))}")

    # Line-by-line comparison
    differences = []
    max_lines = max(len(lines1), len(lines2))

    for i in range(max_lines):
        line1 = lines1[i].strip() if i < len(lines1) else "[FILE_END]"
        line2 = lines2[i].strip() if i < len(lines2) else "[FILE_END]"

        if line1 != line2:
            differences.append({
                'line_num': i + 1,
                'log1': line1,
                'log2': line2
            })

    print(f"\n🔍 FOUND {len(differences)} DIFFERENCES:")
    print("-" * 60)

    if differences:
        # Show first 20 differences in detail
        for i, diff in enumerate(differences[:20]):
            print(f"\nLine {diff['line_num']}:")
            print(f"  dmesg.txt:  {diff['log1'][:100]}{'...' if len(diff['log1']) > 100 else ''}")
            print(f"  dmesg2.txt: {diff['log2'][:100]}{'...' if len(diff['log2']) > 100 else ''}")

            # Analyze type of difference
            if diff['log1'] == "[FILE_END]":
                print(f"  ❌ INCONSISTENCY: dmesg2.txt has extra line")
            elif diff['log2'] == "[FILE_END]":
                print(f"  ❌ INCONSISTENCY: dmesg.txt has extra line")
            else:
                # Check for timestamp differences
                ts1 = re.search(r'\[\s*(\d+\.\d+)\]', diff['log1'])
                ts2 = re.search(r'\[\s*(\d+\.\d+)\]', diff['log2'])

                if ts1 and ts2:
                    t1, t2 = float(ts1.group(1)), float(ts2.group(1))
                    if abs(t1 - t2) > 0.001:  # More than 1ms difference
                        print(f"  ⏱️  TIMING DIFFERENCE: {t1} vs {t2} ({abs(t1-t2):.6f}s)")

                # Check for memory address differences
                mem1 = re.findall(r'0x[0-9a-f]+', diff['log1'], re.IGNORECASE)
                mem2 = re.findall(r'0x[0-9a-f]+', diff['log2'], re.IGNORECASE)

                if mem1 != mem2:
                    print(f"  🧠 MEMORY DIFFERENCE: {mem1} vs {mem2}")

                # Check for numeric value differences
                nums1 = re.findall(r'\b\d+\b', diff['log1'])
                nums2 = re.findall(r'\b\d+\b', diff['log2'])

                if nums1 != nums2:
                    unique_nums1 = set(nums1) - set(nums2)
                    unique_nums2 = set(nums2) - set(nums1)
                    if unique_nums1 or unique_nums2:
                        print(f"  🔢 NUMERIC DIFFERENCE: unique to log1: {unique_nums1}, unique to log2: {unique_nums2}")

        if len(differences) > 20:
            print(f"\n... and {len(differences) - 20} more differences")

    # Analyze patterns in differences
    print(f"\n🔍 DIFFERENCE PATTERNS ANALYSIS:")
    print("-" * 60)

    timestamp_diffs = []
    memory_diffs = []
    content_diffs = []

    for diff in differences:
        if diff['log1'] != "[FILE_END]" and diff['log2'] != "[FILE_END]":
            # Timestamp analysis
            ts1 = re.search(r'\[\s*(\d+\.\d+)\]', diff['log1'])
            ts2 = re.search(r'\[\s*(\d+\.\d+)\]', diff['log2'])

            if ts1 and ts2:
                t1, t2 = float(ts1.group(1)), float(ts2.group(1))
                if abs(t1 - t2) > 0.001:
                    timestamp_diffs.append(abs(t1 - t2))

            # Memory address analysis
            mem1 = re.findall(r'0x[0-9a-f]+', diff['log1'], re.IGNORECASE)
            mem2 = re.findall(r'0x[0-9a-f]+', diff['log2'], re.IGNORECASE)

            if mem1 != mem2:
                memory_diffs.append((mem1, mem2))

            # Content without timestamps/addresses
            clean1 = re.sub(r'\[\s*\d+\.\d+\]', '', diff['log1'])
            clean1 = re.sub(r'0x[0-9a-f]+', 'ADDR', clean1, flags=re.IGNORECASE)
            clean2 = re.sub(r'\[\s*\d+\.\d+\]', '', diff['log2'])
            clean2 = re.sub(r'0x[0-9a-f]+', 'ADDR', clean2, flags=re.IGNORECASE)

            if clean1 != clean2:
                content_diffs.append((clean1.strip(), clean2.strip()))

    if timestamp_diffs:
        print(f"⏱️  Timestamp differences: {len(timestamp_diffs)} instances")
        print(f"   Average difference: {sum(timestamp_diffs)/len(timestamp_diffs):.6f}s")
        print(f"   Max difference: {max(timestamp_diffs):.6f}s")

    if memory_diffs:
        print(f"🧠 Memory address differences: {len(memory_diffs)} instances")
        for i, (m1, m2) in enumerate(memory_diffs[:5]):
            print(f"   Example {i+1}: {m1} vs {m2}")

    if content_diffs:
        print(f"📝 Content differences: {len(content_diffs)} instances")
        unique_content = set()
        for c1, c2 in content_diffs[:10]:
            if c1 != c2:
                unique_content.add(f"{c1[:50]} vs {c2[:50]}")
        for content in list(unique_content)[:5]:
            print(f"   - {content}")

    # Generate diff report
    if differences:
        print(f"\n📄 GENERATING UNIFIED DIFF REPORT...")
        diff_output = list(difflib.unified_diff(
            [line.rstrip() for line in lines1],
            [line.rstrip() for line in lines2],
            fromfile='dmesg.txt',
            tofile='dmesg2.txt',
            lineterm=''
        ))

        with open('diff_report.txt', 'w') as f:
            for line in diff_output:
                f.write(line + '\n')

        print(f"   Detailed diff saved to: diff_report.txt")
        print(f"   Lines in diff report: {len(diff_output)}")

    # Final assessment
    print(f"\n🎯 FINAL ASSESSMENT:")
    print("-" * 60)
    if not differences:
        print("✅ The logs are identical")
    elif len(differences) < 5:
        print("⚠️  Minor differences detected - likely same system, different boot times")
    elif len(differences) < 50:
        print("⚠️  Moderate differences - possibly same system with different configurations")
    else:
        print("❌ Significant differences - likely different systems or major configuration changes")

if __name__ == "__main__":
    detailed_log_comparison()
