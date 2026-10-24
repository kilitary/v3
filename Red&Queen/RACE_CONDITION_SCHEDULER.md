# Race Condition Scheduler for 6PM Turns

## Overview

The Race Condition Scheduler is a new feature that creates intentional race conditions at 6PM intervals using all available words from all categories. This system implements comprehensive word processing with random analyze cycles (2-4 range) to enhance parallel processing capabilities.

## Features

### 🕕 6PM Scheduling
- Automatically calculates next 6PM occurrence
- Works across day boundaries (schedules tomorrow's 6PM if today's has passed)
- Maintains persistent turn counter to track scheduling events

### 📚 All Words Processing
- Processes entire vocabulary during race conditions
- Includes all 11 word categories (940+ words total)
- Categories: Physical Properties, Computer Verbs, IA Architecture, Circuit Components, Data Structures, Algorithms, Threading Concepts, Security Concepts, Network Protocols, Performance Metrics, Reliability Concepts

### 🎲 Random Analyze Cycles
- Each race condition uses 2-4 random analyze cycles
- Words are shuffled and repeated across cycles
- Creates intentional processing conflicts for enhanced parallelism

### 🏃‍♂️ Race Condition Creation
- Triggers comprehensive processing of all system vocabulary
- Creates controlled chaos for testing parallel processing limits
- Deactivates automatically after processing

## Usage

### Basic Setup

```python
from compact_evolution import CompactEvolutionSystem

# Initialize system
system = CompactEvolutionSystem()

# Enable race condition scheduler
system.enable_race_condition_scheduler(True)

# Check scheduler status
status = system.get_race_condition_status()
print(f"Next 6PM trigger: {status['next_6pm_trigger']}")
```

### Processing During Race Conditions

```python
# Normal processing
result = system.process_request("Process memory with threading")

# If race condition is active, result will include:
if 'race_condition' in result:
    race_info = result['race_condition']
    print(f"Race trigger: {race_info['trigger']}")
    print(f"Words processed: {race_info['total_words_processed']}")
    print(f"Turn counter: {race_info['turn_counter']}")
```

### Manual Race Condition Testing

```python
# Simulate race condition for testing
system.race_scheduler.race_condition_active = True
system.race_scheduler.turn_counter += 1

result = system.process_request("Test request")
# Will process all 940+ words regardless of request content
```

## API Reference

### CompactEvolutionSystem Methods

#### `enable_race_condition_scheduler(enabled: bool = True)`
Enable or disable the 6PM race condition scheduler.

**Parameters:**
- `enabled`: Whether to enable the scheduler

**Returns:**
- Prints status and next scheduled trigger time

#### `get_race_condition_status() -> Dict`
Get current status of the race condition scheduler.

**Returns:**
```python
{
    "enabled": bool,
    "next_6pm_trigger": str,  # ISO format datetime
    "race_condition_active": bool,
    "turn_counter": int,
    "all_words_count": int
}
```

### RaceConditionScheduler Class

#### `check_6pm_trigger() -> bool`
Check if it's time for a 6PM turn race condition.

#### `prepare_all_words_race(categories: Dict) -> List[Tuple[str, str]]`
Prepare all words from all categories for race condition processing.

#### `deactivate_race_condition()`
Deactivate the current race condition.

## Implementation Details

### Race Condition Detection
```python
def process_request(self, request: str) -> Dict:
    # Check for 6pm race condition trigger
    race_triggered = self.race_scheduler.check_6pm_trigger()
    
    if race_triggered or self.race_scheduler.race_condition_active:
        # Process ALL words from ALL categories
        race_words = self.race_scheduler.prepare_all_words_race(self.categories)
        # ... process race words
```

### Random Analyze Cycles
```python
# Create random analyze cycles with 2-4 cycles
analyze_cycles = random.randint(2, 4)
race_words = []

for cycle in range(analyze_cycles):
    # Shuffle words for each cycle to create race conditions
    shuffled = all_words.copy()
    random.shuffle(shuffled)
    race_words.extend(shuffled)
```

## Testing

### Test Scripts

1. **`test_race_condition_6pm.py`**: Comprehensive test suite
   - Tests normal processing vs race condition processing
   - Validates random analyze cycles
   - Verifies scheduler enable/disable functionality

2. **`compact_evolution_demo.py`**: Updated demo with race condition demonstration
   - Shows full system capabilities including race conditions
   - Demonstrates word processing volume during race events

### Running Tests

```bash
# Run race condition tests
python3 Red&Queen/test_race_condition_6pm.py

# Run full demonstration
python3 Red&Queen/compact_evolution_demo.py

# Run existing tests to verify compatibility
python3 Red&Queen/test_decay_trigger.py
```

## Example Output

### Race Condition Triggered
```
🚀 Simulating 6pm race condition...
  Status: APPROVE
  Total words processed: 940
  Race trigger: 6pm_turn_race_condition
  Turn counter: 1
  Words processed: 940
  Analyze cycles: random 2-4 cycles as specified

  Sample words (first 15): ['BackTracking', 'Bandwidth', 'Cache', 'SSO', 'Config', ...]

  Random cycle examples:
    'Pipeline' processed 4 times
    'DynamicProgramming' processed 4 times
    'RAM' processed 4 times
```

### Normal Processing (No Race Condition)
```
🔍 Test 1: Normal Processing
  Status: APPROVE
  Identified words: ['Memory', 'Process', 'Thread', 'Process', 'Hyperthread']
  Race condition triggered: False
```

## Integration with Existing Systems

The race condition scheduler integrates seamlessly with existing functionality:

- ✅ Preserves all existing word detection and processing
- ✅ Maintains compatibility with decay-based parallelism injection
- ✅ Works with existing TimeAxis and ExecutionAxis systems
- ✅ Supports existing hyperthreading and execution planning
- ✅ Maintains compact representation and logic circuit generation

## Performance Considerations

- Race conditions process 940+ words (vs typical 2-5 words)
- Processing time increases proportionally during race events
- Memory usage scales with word repetition (2-4x base vocabulary)
- Automatic deactivation prevents sustained high processing

## Configuration

### Default Settings
- Scheduler: Disabled by default
- 6PM Detection: Automatic based on system time
- Analyze Cycles: Random 2-4 range
- Turn Counter: Starts from 0

### Customization
The system can be extended to support:
- Different scheduling intervals
- Custom word sets for race conditions
- Configurable analyze cycle ranges
- Custom race condition triggers

## Troubleshooting

### Common Issues

1. **Scheduler not triggering**: Ensure `enabled=True` and check system time
2. **No race words processed**: Verify categories are populated
3. **Performance issues**: Race conditions are intensive by design

### Debug Information
```python
# Check scheduler status
status = system.get_race_condition_status()
print(f"Debug info: {status}")

# Manual trigger for testing
system.race_scheduler.race_condition_active = True
```

## Future Enhancements

Potential improvements for the race condition system:
- Multiple daily trigger times
- Custom word filtering for race conditions
- Performance metrics during race events
- Integration with external scheduling systems
- Race condition intensity levels