#!/usr/bin/env python3
"""
Red&Queen Random Utilities
===========================

Repository-wide R&Q random system implementation following the corrected logic:
1. Get analog or other really random byte at start and seed random
2. Get 1-byte random value "num_skip"  
3. "num_skip" random times get random value in range 1 to 10
   if acquired random value is 5, go to next step, else discard value and continue loop
4. Make a func for getting random value for entire repository using steps 2-3

This module provides the corrected R&Q random system for the entire repository.

Key Functions:
--------------
- get_rq_random(): Get global R&Q random system instance
- getrandom(from, to): Simplified interface for getting random values
- rq_randint(min, max): Get random integer using R&Q algorithm
- rq_shuffle(list): Shuffle list using R&Q random
- rq_hex_check(length): Generate hex check string
- rq_cycles(min, max): Get random cycles for analysis

Advanced Features:
------------------
- seed_from_sensor_data(sensor_dict): Seed using hardware sensor values
- run_once(func, *args, **kwargs): Execute function only once
"""

import random
import time
import os
from typing import List, Any


class RQRandomSystem:
    """
    Red&Queen Random System Implementation
    
    Implements proper R&Q random shuffle system with true random seeding
    and skip-based random value generation as specified.
    """
    
    def __init__(self):
        """Initialize R&Q Random System with true random seed"""
        self._initialize_true_random_seed()
        self.operation_count = 0
        self._run_once_executed = False
        
    def _initialize_true_random_seed(self):
        """
        Step 1: Get analog/truly random byte from OS and seed random
        Uses OS entropy pool for true randomness
        """
        try:
            # Get truly random bytes from OS entropy pool (/dev/urandom on Unix)
            random_bytes = os.urandom(8)  # 8 bytes for strong seed
            seed_value = int.from_bytes(random_bytes, byteorder='big')
            random.seed(seed_value)
            
            self.seed_info = {
                "type": "OS_ENTROPY",
                "seed": seed_value & 0xFFFFFFFF,  # Show lower 32 bits
                "full_seed": seed_value,
                "entropy_bytes": random_bytes.hex().upper()
            }
            
            print(f"🎲 R&Q Random System initialized")
            print(f"   Entropy source: OS urandom")
            print(f"   Seed: {self.seed_info['seed']:08X}")
            print(f"   Full entropy: {self.seed_info['entropy_bytes'][:20]}...")
            
        except Exception as e:
            # Fallback to high-precision time-based seed if OS entropy fails
            fallback_seed = int(time.time() * 1000000) % (2**32)
            random.seed(fallback_seed)
            
            self.seed_info = {
                "type": "TIME_FALLBACK", 
                "seed": fallback_seed,
                "error": str(e)
            }
            
            print(f"⚠️  R&Q Random System fallback initialization")
            print(f"   Reason: {e}")
            print(f"   Time-based seed: {fallback_seed:08X}")
    
    def seed_from_sensor_data(self, sensor_values: dict) -> None:
        """
        Seed the random system using sensor data for enhanced entropy
        
        This function accepts sensor values (like CPU temp, voltage, etc.)
        and uses them to create additional entropy for the random system.
        
        Args:
            sensor_values: Dictionary containing sensor data
                          e.g., {'cpu_temp': 45.2, 'gpu_temp': 60.1, 'voltage_12v': 12.05}
        
        Example:
            rq_system.seed_from_sensor_data({
                'cpu_temp': 45.2,
                'gpu_temp': 60.1,
                'v12_voltage': 12.05,
                'cpu_voltage': 1.35,
                'power': 150.0
            })
        """
        # Combine sensor values with XOR and bit shifting
        entropy_value = 0
        shift_amount = 0
        
        for key, value in sensor_values.items():
            # Convert float values to integer representation
            if isinstance(value, float):
                int_value = int(value * 1000)  # Scale to preserve precision
            else:
                int_value = int(value)
            
            # XOR and shift operations
            if shift_amount % 2 == 0:
                entropy_value ^= (int_value << (shift_amount % 16))
            else:
                entropy_value ^= (int_value >> (shift_amount % 8))
            
            shift_amount += 1
        
        # Combine with OS entropy for maximum randomness
        try:
            os_bytes = os.urandom(4)
            os_value = int.from_bytes(os_bytes, byteorder='big')
            final_seed = entropy_value ^ os_value
        except Exception:
            final_seed = entropy_value
        
        # Reseed the random system
        random.seed(final_seed)
        
        print(f"🔧 R&Q System reseeded with sensor data")
        print(f"   Entropy from sensors: {entropy_value & 0xFFFFFFFF:08X}")
        print(f"   Final seed: {final_seed & 0xFFFFFFFF:08X}")
    
    def run_once(self, func, *args, **kwargs):
        """
        Execute a function only once during the lifetime of this R&Q system
        
        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the function if first call, None if already executed
        """
        if not self._run_once_executed:
            self._run_once_executed = True
            return func(*args, **kwargs)
        else:
            print(f"   RunOnce: Function '{func.__name__}' already executed, skipping")
            return None
    
    def get_rq_random_value(self, min_val: int = 0, max_val: int = 255) -> int:
        """
        Get R&Q random value using the specified algorithm:
        
        Steps 2-3:
        2. Get 1-byte random value "num_skip"
        3. "num_skip" random times get random value in range 1 to 10
           if acquired random value is 5, go to next step, else discard and continue
        
        Args:
            min_val: Minimum value for final random result
            max_val: Maximum value for final random result
            
        Returns:
            Random value in range [min_val, max_val] using R&Q algorithm
        """
        self.operation_count += 1
        
        # Step 2: Get 1-byte random value "num_skip"
        num_skip = random.randint(0, 255)
        
        # Step 3: Skip process - get random values until we get 5
        skip_count = 0
        discarded_values = []
        
        while skip_count < num_skip:
            test_value = random.randint(1, 10)
            if test_value == 5:
                # Got 5, exit skip loop
                break
            else:
                # Discard value and continue loop
                discarded_values.append(test_value)
                skip_count += 1
        
        # Now get the actual random value in the requested range
        final_value = random.randint(min_val, max_val)
        
        # Debug info for first few operations
        if self.operation_count <= 3:
            print(f"   R&Q Random Op #{self.operation_count}: num_skip={num_skip}, "
                  f"discarded={len(discarded_values)}, final={final_value}")
        
        return final_value
    
    def rq_shuffle(self, data_list: List[Any]) -> None:
        """
        R&Q random shuffle using the proper random system
        
        Implements Fisher-Yates shuffle using R&Q random values
        """
        if len(data_list) <= 1:
            return
            
        # Fisher-Yates shuffle with R&Q random
        for i in range(len(data_list) - 1, 0, -1):
            j = self.get_rq_random_value(0, i)
            data_list[i], data_list[j] = data_list[j], data_list[i]
    
    def get_rq_random_int(self, min_val: int, max_val: int) -> int:
        """Get R&Q random integer in specified range"""
        return self.get_rq_random_value(min_val, max_val)
    
    def get_rq_random_hex_check(self, length: int = 10) -> str:
        """
        Generate R&Q random hex check like simulation logs
        
        Args:
            length: Number of hex bytes to generate
            
        Returns:
            Space-separated hex string like "7A AC 0D 1D DA 61 E6 0E B5 AE"
        """
        hex_values = []
        for _ in range(length):
            hex_val = self.get_rq_random_value(0, 255)
            hex_values.append(f"{hex_val:02X}")
        return ' '.join(hex_values)
    
    def get_rq_cycles(self, min_cycles: int = 2, max_cycles: int = 4) -> int:
        """Get R&Q random cycles in range (for analyze cycles)"""
        return self.get_rq_random_value(min_cycles, max_cycles)
    
    def get_system_info(self) -> dict:
        """Get R&Q random system information"""
        return {
            "seed_info": self.seed_info,
            "operations_performed": self.operation_count,
            "system_status": "ACTIVE"
        }


# Global R&Q Random System instance for repository-wide use
_global_rq_random = None

def get_rq_random() -> RQRandomSystem:
    """
    Get the global R&Q Random System instance for entire repository use
    
    This function implements step 4: "make a func for getting random value 
    for entire repository using steps 2-3"
    
    Returns:
        Global RQRandomSystem instance
    """
    global _global_rq_random
    if _global_rq_random is None:
        _global_rq_random = RQRandomSystem()
    return _global_rq_random

def rq_randint(min_val: int, max_val: int) -> int:
    """Repository-wide R&Q random integer function"""
    return get_rq_random().get_rq_random_int(min_val, max_val)

def rq_shuffle(data_list: List[Any]) -> None:
    """Repository-wide R&Q shuffle function"""
    get_rq_random().rq_shuffle(data_list)

def rq_hex_check(length: int = 10) -> str:
    """Repository-wide R&Q hex check generation"""
    return get_rq_random().get_rq_random_hex_check(length)

def rq_cycles(min_cycles: int = 2, max_cycles: int = 4) -> int:
    """Repository-wide R&Q cycles generation"""
    return get_rq_random().get_rq_cycles(min_cycles, max_cycles)

def rq_choice(choices: List[Any]) -> Any:
    """Repository-wide R&Q random choice function"""
    if not choices:
        return None
    index = get_rq_random().get_rq_random_value(0, len(choices) - 1)
    return choices[index]

def getrandom(from_val: int, to_val: int) -> int:
    """
    Get random value in range using R&Q algorithm
    
    This is a simplified interface following common naming convention.
    Uses the corrected R&Q random process with entropy seeding and skip algorithm.
    
    Args:
        from_val: Minimum value (inclusive)
        to_val: Maximum value (inclusive)
        
    Returns:
        Random integer in range [from_val, to_val]
        
    Example:
        >>> random_value = getrandom(1, 100)
        >>> dice_roll = getrandom(1, 6)
    """
    return get_rq_random().get_rq_random_value(from_val, to_val)


def test_rq_random_system():
    """Test the R&Q random system implementation"""
    print_count = 0  # Track executed print() functions
    
    print("=" * 70)
    print_count += 1
    print("RED&QUEEN RANDOM SYSTEM TEST")
    print_count += 1
    print("Testing corrected R&Q random logic")
    print_count += 1
    print("=" * 70)
    print_count += 1
    
    rq = get_rq_random()
    
    print(f"\n📊 SYSTEM INFO:")
    print_count += 1
    info = rq.get_system_info()
    print(f"   Seed Type: {info['seed_info']['type']}")
    print_count += 1
    print(f"   Seed Value: {info['seed_info']['seed']:08X}")
    print_count += 1
    
    print(f"\n🧪 TESTING R&Q RANDOM VALUES:")
    print_count += 1
    for i in range(5):
        val = rq.get_rq_random_value(0, 100)
        print(f"   Test {i+1}: R&Q Random(0-100) = {val}")
        print_count += 1
    
    print(f"\n🔀 TESTING R&Q SHUFFLE:")
    print_count += 1
    test_data = list(range(10))
    original = test_data.copy()
    rq.rq_shuffle(test_data)
    print(f"   Original: {original}")
    print_count += 1
    print(f"   Shuffled: {test_data}")
    print_count += 1
    
    print(f"\n🎲 TESTING HEX CHECK GENERATION:")
    print_count += 1
    hex_check = rq.get_rq_random_hex_check(10)
    print(f"   R&Q Hex Check: {hex_check}")
    print_count += 1
    
    # Test new getrandom function
    print(f"\n🎯 TESTING getrandom(from, to):")
    print_count += 1
    for i in range(3):
        val = getrandom(1, 100)
        print(f"   getrandom(1, 100) = {val}")
        print_count += 1
    
    # Test sensor data seeding
    print(f"\n🔧 TESTING SENSOR DATA SEEDING:")
    print_count += 1
    sensor_data = {
        'cpu_temp': 45.2,
        'gpu_temp': 60.1,
        'v12_voltage': 12.05,
        'cpu_voltage': 1.35,
        'power': 150.0
    }
    rq.seed_from_sensor_data(sensor_data)
    print_count += 3  # Account for prints inside seed_from_sensor_data
    
    # Test RunOnce functionality
    print(f"\n🔁 TESTING RunOnce:")
    print_count += 1
    
    def test_func(msg):
        print(f"   Executing test_func: {msg}")
        return msg.upper()
    
    result1 = rq.run_once(test_func, "first call")
    print_count += 1
    print(f"   First call result: {result1}")
    print_count += 1
    
    result2 = rq.run_once(test_func, "second call")
    print_count += 1
    print(f"   Second call result: {result2}")
    print_count += 1
    
    print(f"\n📈 FINAL STATS:")
    print_count += 1
    final_info = rq.get_system_info()
    print(f"   Operations: {final_info['operations_performed']}")
    print_count += 1
    print(f"   Status: {final_info['system_status']}")
    print_count += 1
    
    print(f"\n✅ R&Q RANDOM SYSTEM TEST COMPLETE")
    print_count += 1
    
    # Check for executed print() functions at the end
    print(f"\n🔍 PRINT FUNCTIONS EXECUTED: {print_count}")
    print_count += 1
    
    return print_count


if __name__ == "__main__":
    total_prints = test_rq_random_system()
    print(f"Total print() calls: {total_prints}")