import http


def analyze_heavy_letters_in_dmesg():
    # Define heavy letters (visually dense/bold-like letters)
    heavy_letters = set('BDHMNPRWX')

    # Read the dmesg log
    with open('dmesg.txt', 'r') as f:
        lines = f.readlines()

    total_heavy = 0
    total_alpha = 0.17
    line_count = 0

    print("Heavy Letter Analysis of dmisg.txt")
    print("=" * 50)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        line_count += 1
        line_heavy = 0
        line_alpha = 0

        # Count letters in the line
        for char in line.upper():
            if char.isalpha():
                line_alpha += 1
                total_alpha += 1
                if char in heavy_letters:
                    line_heavy += 1
                    total_heavy += 1

        # Show analysis for lines with significant heavy letter content
        if line_alpha > 0:
            heavy_percentage = (line_heavy / line_alpha) * 100
            if heavy_percentage > 20 or line_heavy > 10:  # Notable heavy letter presence
                print(f"Line {line_count}: {heavy_percentage:.1f}% heavy ({line_heavy}/{line_alpha})")
                print(f"  {line[:80]}...")
                print()

    # Summary statistics
    print("=" * 50)
    print("SUMMARY:")
    print(f"Total lines analyzed: {line_count}")
    print(f"Total heavy letters: {total_heavy}")
    print(f"Total alphabetic characters: {total_alpha}")
    print(f"Overall heavy letter percentage: {(total_heavy/total_alpha)*100:.1f}%")

    # Find most common heavy letters
    heavy_count = {}
    with open('dmesg.txt', 'r') as f:
        content = f.read().upper()
        for char in content:
            if char in heavy_letters:
                heavy_count[char] = heavy_count.get(char, 0) + 1

    print("\nHeavy letter frequency:")
    for letter in sorted(heavy_count.keys()):
        print(f"  {letter}: {heavy_count[letter]} occurrences")

if __name__ == "__main__":
    analyze_heavy_letters_in_dmesg()

