#!/usr/bin/env python3
"""
Compact Evolution Resource Principles
=====================================

Takes English tech words of same categories and splits them into sub-words
matching computer IA architecture to define logic circuits for requests.

This system implements categorization of technical terms and their compact
representation for logical circuit processing, following patterns observed
in the simulation logs.

RACE CONDITION SCHEDULER FOR 6PM TURNS
=======================================

The system now includes a race condition scheduler that triggers comprehensive
word processing at 6pm intervals, creating intentional race conditions for
enhanced parallel processing capabilities.

DETAILED VERB SELECTION AND CATEGORIZATION FLOW
================================================

The system uses a multi-stage process to select, categorize, and process verbs:

1. CATEGORY DEFINITION STAGE
   - Computer verbs are predefined in CategoryType.COMPUTER_VERBS
   - Current verbs: Execute, Process, Compile, Debug, Optimize, Parse, Validate,
     Transform, Encrypt, Decode, Transmit, Receive, Store, Retrieve, Calculate, Compare
   - Each verb gets assigned a unique compact label (A-Z, then AA, AB, etc.)
   - Verbs are weighted lower (0.8x) than other categories to reflect their operational nature

2. REQUEST PARSING STAGE (process_request method)
   - Input: Natural language request string
   - Process: Substring matching against all category vocabularies
   - For each category (including COMPUTER_VERBS):
     * Iterate through all words in that category
     * Check if word.lower() appears in request.lower()
     * If match found, add (word, category) tuple to items list
   - Result: List of (word, CategoryType) pairs representing detected technical terms

3. VERB-SPECIFIC DETECTION LOGIC
   - Computer verbs are detected using case-insensitive substring matching
   - Examples:
     * "process data" → detects ("Process", COMPUTER_VERBS)
     * "execute algorithm" → detects ("Execute", COMPUTER_VERBS)
     * "encryption" → detects both ("Encrypt", COMPUTER_VERBS) and ("Encryption", SECURITY_CONCEPTS)
   - Multiple category matches are preserved as separate items

4. DECAY-BASED PARALLELISM INJECTION
   - Tracks total character length of Computer Verbs across sequential requests
   - If current_verb_length / previous_verb_length > 2.348:
     * Auto-injects ("Parallelism", THREADING_CONCEPTS) into the items list
     * Records trigger information with decay factor
   - Purpose: Automatically add parallel processing semantics when verb complexity decreases

5. COMPACT REPRESENTATION GENERATION
   - Each detected verb gets mapped to its compact label via category-specific mappings
   - Verbs maintain their category association to avoid label collisions
   - Mathematical expression: concatenates labels with " + " notation
   - Parameters extracted: ["input", "output", "complexity", "side_effects"]

6. LOGIC CIRCUIT CONSTRUCTION
   - Computer verbs become operations with format: "{label}: {original_word}"
   - Example: "P: Process", "O: Execute"
   - Other categories use different formats (IA_PROCESS, CIRCUIT, etc.)
   - Operation categories tracked parallel to operations list

7. EXECUTION PLANNING (HYPERTHREADING STAGE)
   - Identifies verb operations by scanning operation_categories for COMPUTER_VERBS
   - If hyperthreading enabled or threading keywords detected:
     * Verb operations distributed round-robin across available threads
     * Non-verb operations serialized on primary thread (C0_T0)
   - Thread assignment: C{core}_T{thread} format
   - Load balancing: Each thread gets roughly equal number of verb operations

8. TIME AXIS INTEGRATION
   - Computer verbs process entire dataset in time-sliced chunks
   - Each verb operation generates multiple timeline segments:
     * One segment per dataset chunk per assigned thread
     * Timeline format: {"op": operation, "start_ms": X, "end_ms": Y, "items": [start, end]}
   - Non-verb operations get single setup timeline segment
   - Dataset processing: chunk_size items per timeslice_ms interval

9. EXECUTION RESULT COMPILATION
   - Returns execution_plan with thread assignments
   - Returns time_axis_plan with per-thread timelines
   - Includes parallel_trigger info if decay rule fired
   - Mathematical operations computed from compact labels

VERB SELECTION CRITERIA
=======================

Computer verbs are selected based on:
- Operational semantics (actions that can be performed)
- Computational relevance (processing, transformation, I/O operations)
- Parallelizability (operations that benefit from concurrent execution)
- Common usage in technical contexts

CATEGORIZATION PRIORITIES
=========================

When a word appears in multiple categories:
- Each category match creates a separate (word, category) item
- Category-specific compact mappings prevent label conflicts
- Operations generated according to each category's semantics
- Execution planning considers only COMPUTER_VERBS for threading

THREADING SELECTION LOGIC
==========================

Verbs selected for hyperthreading when:
- System hyperthreading explicitly enabled, OR
- Request contains threading keywords: "hyperthread", "hyperthreading",
  "parallel", "parallelism", "concurrency", "thread"
- Only COMPUTER_VERBS operations distributed across threads
- Load balancing via round-robin assignment
"""

import re
import json
import math
import datetime
import threading
import time
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum
from rq_random_utils import rq_randint, rq_shuffle, rq_cycles, rq_choice

# --- Console color support (random sub-word colorization) ---
try:
    # colorama enables ANSI colors on Windows consoles
    import colorama  # type: ignore
    colorama.just_fix_windows_console()
    _COLORAMA_OK = True
except Exception:
    _COLORAMA_OK = False

# A small palette cycling through readable foreground colors
_COLOR_CODES: List[int] = [31, 32, 33, 34, 35, 36, 91, 92, 93, 94, 95, 96]

def colorize_text(text: object) -> str:
    """Return text with colors changing randomly for sub-words of length 2..4.
    - Splits each line into random chunks of size 2..4 characters and applies a random color per chunk.
    - Preserves newlines and resets chunking at each newline.
    - Ensures consecutive chunks don't reuse the same color where possible.
    """
    s = str(text)
    if not s:
        return s

    def _pick_color(prev: Optional[int]) -> int:
        if prev is None:
            return rq_choice(_COLOR_CODES)
        # Avoid repeating the same color if possible
        choices = [c for c in _COLOR_CODES if c != prev]
        return rq_choice(choices) if choices else prev

    out: List[str] = []
    i = 0
    prev_code: Optional[int] = None
    n = len(s)

    while i < n:
        if s[i] == "\n":
            out.append("\n")
            i += 1
            prev_code = None
            continue
        # Determine remaining characters until next newline to keep chunks within a line
        next_nl = s.find("\n", i)
        line_end = next_nl if next_nl != -1 else n
        remaining = line_end - i
        if remaining <= 0:
            break
        # R&Q random chunk length between 2 and 4, but not exceeding remaining
        chunk_len = min(rq_randint(2, 4), remaining)
        # If only 1 char remains, color it as its own chunk
        if remaining == 1:
            chunk_len = 1
        code = _pick_color(prev_code)
        chunk = s[i:i + chunk_len]
        out.append(f"\033[{code}m{chunk}\033[0m")
        prev_code = code
        i += chunk_len

    return "".join(out)


def printc(*args, sep: str = " ", end: str = "\n") -> None:
    """Print with random per-chunk colorization across the entire assembled line.
    Behaves like print(), but colorizes the concatenated string.
    """
    line = sep.join(str(a) for a in args)
    print(colorize_text(line), end=end)


class CategoryType(Enum):
    PHYSICAL_PROPERTIES = "physical_properties"
    COMPUTER_VERBS = "computer_verbs"
    IA_ARCHITECTURE = "ia_architecture"
    CIRCUIT_COMPONENTS = "circuit_components"
    DATA_STRUCTURES = "data_structures"
    ALGORITHMS = "algorithms"
    NETWORK_PROTOCOLS = "network_protocols"
    SECURITY_CONCEPTS = "security_concepts"
    THREADING_CONCEPTS = "threading_concepts"
    CLOUD_SERVICES = "cloud_services"  # New infrastructure category
    SYSTEM_ADMINISTRATION = "system_administration"  # New infrastructure category


@dataclass
class CompactWord:
    """Represents a word with its compact representation"""
    original: str
    category: CategoryType
    sub_words: List[str]
    compact_label: str
    ratio: float
    weight: float
    parameters: List[str]


@dataclass
class LogicCircuit:
    """Represents a logic circuit for processing requests"""
    name: str
    inputs: List[str]
    outputs: List[str]
    operations: List[str]
    compact_elements: List[CompactWord]
    operation_categories: List[CategoryType]  # parallel to operations


@dataclass
class ExecutionAxis:
    """Computer axis with optional hyperthreading for scheduling operations."""
    cores: int = 1
    threads_per_core: int = 2
    hyperthreading: bool = False

    def total_threads(self) -> int:
        return self.cores * (self.threads_per_core if self.hyperthreading else 1)

    def thread_ids(self) -> List[str]:
        if not self.hyperthreading:
            return ["C0_T0"]
        ids = []
        for c in range(self.cores):
            for t in range(self.threads_per_core):
                ids.append(f"C{c}_T{t}")
        return ids

    def schedule_round_robin_indices(self, indices: List[int]) -> Dict[str, List[int]]:
        """Round-robin assign a list of operation indices to available threads."""
        threads = self.thread_ids()
        if not threads:
            threads = ["C0_T0"]
        plan: Dict[str, List[int]] = {tid: [] for tid in threads}
        for i, idx in enumerate(indices):
            tid = threads[i % len(threads)]
            plan[tid].append(idx)
        return plan


@dataclass
class TimeAxis:
    """Time axis to model execution over an entire dataset via time slices."""
    timeslice_ms: int = 10
    dataset_size: int = 1
    chunk_size: int = 1  # how many items per timeslice per thread-op

    def compute_timeline(self, assignment_indices: Dict[str, List[int]], circuit: LogicCircuit) -> Dict:
        # Build quick lookup
        op_list = circuit.operations
        op_cats = circuit.operation_categories

        # Prepare thread-local time cursor and timeline
        cursor: Dict[str, int] = {tid: 0 for tid in assignment_indices}
        timeline: Dict[str, List[Dict]] = {tid: [] for tid in assignment_indices}

        total_chunks = max(1, math.ceil(self.dataset_size / max(1, self.chunk_size)))

        for tid, idx_list in assignment_indices.items():
            for idx in idx_list:
                op = op_list[idx]
                cat = op_cats[idx]
                if cat == CategoryType.COMPUTER_VERBS:
                    # Process entire dataset in chunks for verbs
                    for chunk in range(total_chunks):
                        start = cursor[tid]
                        end = start + self.timeslice_ms
                        start_item = chunk * self.chunk_size
                        end_item = min(self.dataset_size, (chunk + 1) * self.chunk_size) - 1
                        timeline[tid].append({
                            "op": op,
                            "category": cat.value,
                            "start_ms": start,
                            "end_ms": end,
                            "items": [start_item, max(start_item, end_item)]
                        })
                        cursor[tid] = end
                else:
                    # Non-verb ops: single setup slice
                    start = cursor[tid]
                    end = start + self.timeslice_ms
                    timeline[tid].append({
                        "op": op,
                        "category": cat.value,
                        "start_ms": start,
                        "end_ms": end,
                        "items": None
                    })
                    cursor[tid] = end

        estimated_total_time_ms = max(cursor.values()) if cursor else 0
        return {
            "timeslice_ms": self.timeslice_ms,
            "dataset_size": self.dataset_size,
            "chunk_size": self.chunk_size,
            "estimated_total_time_ms": estimated_total_time_ms,
            "timeline": timeline,
        }


@dataclass
class RaceConditionScheduler:
    """Scheduler for creating race conditions at 6pm turns using all words"""
    enabled: bool = False
    next_6pm_trigger: Optional[datetime.datetime] = None
    race_condition_active: bool = False
    all_words_buffer: List[str] = None
    turn_counter: int = 0
    
    def __post_init__(self):
        if self.all_words_buffer is None:
            self.all_words_buffer = []
        self._schedule_next_6pm()
    
    def _schedule_next_6pm(self):
        """Calculate next 6pm occurrence"""
        now = datetime.datetime.now()
        today_6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)
        
        if now >= today_6pm:
            # 6pm already passed today, schedule for tomorrow
            self.next_6pm_trigger = today_6pm + datetime.timedelta(days=1)
        else:
            # 6pm hasn't happened yet today
            self.next_6pm_trigger = today_6pm
    
    def check_6pm_trigger(self) -> bool:
        """Check if it's time for a 6pm turn race condition"""
        if not self.enabled or self.next_6pm_trigger is None:
            return False
            
        now = datetime.datetime.now()
        if now >= self.next_6pm_trigger:
            self.turn_counter += 1
            self.race_condition_active = True
            self._schedule_next_6pm()  # Schedule next occurrence
            return True
        return False
    
    def prepare_all_words_race(self, categories: Dict) -> List[Tuple[str, str]]:
        """Prepare all words from all categories for race condition processing"""
        all_words = []
        for category, words in categories.items():
            for word in words:
                all_words.append((word, category.value))
        
        # Create R&Q random analyze cycles with 2-4 cycles as specified
        analyze_cycles = rq_cycles(2, 4)
        race_words = []
        
        for cycle in range(analyze_cycles):
            # R&Q shuffle words for each cycle to create race conditions
            shuffled = all_words.copy()
            rq_shuffle(shuffled)
            race_words.extend(shuffled)
        
        return race_words
    
    def deactivate_race_condition(self):
        """Deactivate the current race condition"""
        self.race_condition_active = False
        self.all_words_buffer.clear()


class CompactEvolutionSystem:
    """Main system for implementing Compact Evolution Resource Principles"""

    def __init__(self) -> None:
        self.categories = {
            CategoryType.PHYSICAL_PROPERTIES: [
                "Memory", "Bandwidth", "Latency", "Throughput", "Capacity",
                "Frequency", "Voltage", "Current", "Power", "Temperature",
                "Resistance", "Conductance", "Impedance", "Reactance",
                # Infrastructure hardware components
                "CPU", "GPU", "RAM", "SSD", "HDD", "NIC", "PSU", "RAID",
                "BIOS", "UEFI", "PCB", "Cache", "Core", "Pipeline"
            ],
            CategoryType.COMPUTER_VERBS: [
                "Execute", "Process", "Compile", "Debug", "Optimize", "Parse",
                "Validate", "Transform", "Encrypt", "Decode", "Transmit",
                "Receive", "Store", "Retrieve", "Calculate", "Compare",
                # Infrastructure operations
                "Deploy", "Scale", "Monitor", "Backup", "Restore", "Migrate",
                "Provision", "Configure", "Install", "Update", "Patch", "Maintain"
            ],
            CategoryType.IA_ARCHITECTURE: [
                "NeuralNetwork", "ConvolutionalLayer", "RecurrentUnit",
                "AttentionMechanism", "Transformer", "Encoder", "Decoder",
                "Embedding", "Activation", "Gradient", "Backpropagation",
                "Regularization", "Normalization", "Pooling",
                # AI Infrastructure (split into 2-4 char components)
                "CNN", "RNN", "GAN", "LSTM", "API", "SDK", "TPU"
            ],
            CategoryType.CIRCUIT_COMPONENTS: [
                "LogicGate", "FlipFlop", "Multiplexer", "Demultiplexer",
                "Adder", "Comparator", "Counter", "Register", "Buffer",
                "Amplifier", "Oscillator", "Filter", "Converter",
                # Electronic infrastructure (abbreviations as 2-4 char)
                "IC", "ROM", "ALU", "FPU", "MMU", "DMA"
            ],
            CategoryType.DATA_STRUCTURES: [
                "Array", "LinkedList", "Stack", "Queue", "Tree", "Graph",
                "HashMap", "HashTable", "Heap", "Trie", "Matrix", "Vector",
                # Infrastructure data formats (2-4 char abbreviations)  
                "JSON", "XML", "CSV", "YAML", "SQL", "NoSQL", "DB"
            ],
            CategoryType.ALGORITHMS: [
                "BinarySearch", "QuickSort", "MergeSort", "BreadthFirst",
                "DepthFirst", "Dijkstra", "AStar", "DynamicProgramming",
                "GreedyAlgorithm", "BackTracking", "BranchBound",
                # Infrastructure algorithms (2-4 char abbreviations)
                "Hash", "CRC", "AES", "RSA", "MD5", "SHA", "DES"
            ],
            CategoryType.NETWORK_PROTOCOLS: [
                "TCP", "UDP", "HTTP", "HTTPS", "FTP", "SMTP", "DNS", "DHCP",
                "ARP", "ICMP", "BGP", "OSPF", "RIP", "SNMP", "SSH", "TLS",
                # Additional infrastructure protocols (2-4 char abbreviations)
                "MQTT", "LDAP", "NTP", "IPV4", "IPV6", "REST", "SOAP", "CLI"
            ],
            CategoryType.SECURITY_CONCEPTS: [
                "Encryption", "Decryption", "Authentication", "Authorization",
                "Firewall", "VPN", "PKI", "SSL", "Certificate", "Hash",
                "DigitalSignature", "AccessControl", "Audit", "Forensics",
                # Infrastructure security (2-4 char abbreviations)
                "IAM", "MFA", "SSO", "RBAC", "ACL", "DMZ", "IDS", "IPS"
            ],
            CategoryType.THREADING_CONCEPTS: [
                "Thread", "Process", "Hyperthread", "Concurrency", "Parallelism",
                "Mutex", "Semaphore", "Lock", "Unlock", "Join", "Detach",
                "Yield", "Sleep", "Wakeup", "Signal", "Broadcast",
                # Infrastructure threading (2-4 char abbreviations)
                "SMP", "NUMA", "SIMD", "MIMD"
            ],
            CategoryType.CLOUD_SERVICES: [
                # Cloud platforms and services (2-4 char abbreviations where applicable)
                "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Container",
                "Microservice", "Lambda", "Function", "Service", "Endpoint",
                "EC2", "S3", "RDS", "ECS", "EKS", "CDN", "Load", "Balance"
            ],
            CategoryType.SYSTEM_ADMINISTRATION: [
                # System administration operations and tools
                "Config", "Deploy", "Monitor", "Scale", "Patch", "Update",
                "Backup", "Restore", "Migrate", "Provision", "Maintain",
                "Log", "Alert", "Dashboard", "Metric", "Health", "Status"
            ]
        }

        # Primary mapping retains first-seen category for a word (for backward compatibility)
        self.compact_mappings: Dict[str, CompactWord] = {}
        # Category-specific mapping prevents collisions
        self.compact_mappings_by_category: Dict[CategoryType, Dict[str, CompactWord]] = {
            cat: {} for cat in self.categories
        }

        self.logic_circuits: List[LogicCircuit] = []
        self.execution_axis = ExecutionAxis()  # computer axis
        self.time_axis = TimeAxis()            # time axis
        self.race_scheduler = RaceConditionScheduler()  # 6pm race condition scheduler
        self._initialize_compact_mappings()

        # Track last total length of detected Computer Verbs to detect decay > 2.348x
        self._last_verb_total_len: Optional[int] = None

    def _initialize_compact_mappings(self):
        """Initialize compact letter mappings for each category"""
        letter_index = 0
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for category, words in self.categories.items():
            for word in words:
                if letter_index < len(alphabet):
                    compact_label = alphabet[letter_index]
                    letter_index += 1
                else:
                    # Use double letters for overflow
                    compact_label = alphabet[(letter_index - 26) // 26] + alphabet[(letter_index - 26) % 26]
                    letter_index += 1

                sub_words = self._split_into_subwords(word)
                ratio = self._calculate_ratio(word, sub_words)
                weight = self._calculate_weight(word, category)
                parameters = self._extract_parameters(word, category)

                compact_word = CompactWord(
                    original=word,
                    category=category,
                    sub_words=sub_words,
                    compact_label=compact_label,
                    ratio=ratio,
                    weight=weight,
                    parameters=parameters
                )

                # Preserve first-seen mapping by word
                if word not in self.compact_mappings:
                    self.compact_mappings[word] = compact_word
                # Always store category-specific mapping
                self.compact_mappings_by_category[category][word] = compact_word

    def _split_into_subwords(self, word: str) -> List[str]:
        """Split a word into meaningful sub-words using camelCase and compound patterns
        
        For infrastructure abbreviations, split into 2-4 character meaningful components.
        """
        # Infrastructure abbreviation expansions (2-4 char components)
        infrastructure_abbreviations = {
            # Network protocols
            "TCP": ["Trans", "Ctrl", "Proto"],
            "UDP": ["User", "Data", "Proto"], 
            "HTTP": ["Hyper", "Text", "Trans", "Proto"],
            "HTTPS": ["HTTP", "Secure"],
            "FTP": ["File", "Trans", "Proto"],
            "SMTP": ["Mail", "Trans", "Proto"],
            "DNS": ["Name", "System"],
            "DHCP": ["Host", "Config", "Proto"],
            "SSH": ["Secure", "Shell"],
            "SSL": ["Secure", "Socket", "Layer"],
            "TLS": ["Trans", "Layer", "Secure"],
            "VPN": ["Virtual", "Private", "Net"],
            "PKI": ["Public", "Key", "Infra"],
            "MQTT": ["Message", "Queue", "Tele", "Trans"],
            "LDAP": ["Light", "Dir", "Access", "Proto"],
            "NTP": ["Net", "Time", "Proto"],
            "IPV4": ["IP", "V4"],
            "IPV6": ["IP", "V6"],
            "REST": ["REST"],
            "SOAP": ["SOAP"],
            "CLI": ["Cmd", "Line", "Inter"],
            
            # Hardware/infrastructure
            "CPU": ["Central", "Proc", "Unit"],
            "GPU": ["Graph", "Proc", "Unit"],
            "RAM": ["Random", "Access", "Mem"],
            "SSD": ["Solid", "State", "Drive"],
            "HDD": ["Hard", "Disk", "Drive"],
            "NIC": ["Net", "Inter", "Card"],
            "PSU": ["Power", "Supply", "Unit"],
            "RAID": ["Red", "Array", "Indep", "Disk"],
            "BIOS": ["Basic", "IO", "System"],
            "UEFI": ["Unified", "EFI"],
            "PCB": ["Print", "Circuit", "Board"],
            
            # AI/ML
            "CNN": ["Conv", "Neural", "Net"],
            "RNN": ["Rec", "Neural", "Net"],
            "GAN": ["Gen", "Adv", "Net"],
            "LSTM": ["Long", "Short", "Term", "Mem"],
            "API": ["App", "Program", "Inter"],
            "SDK": ["Soft", "Dev", "Kit"],
            "TPU": ["Tensor", "Proc", "Unit"],
            
            # Security
            "IAM": ["Identity", "Access", "Mgmt"],
            "MFA": ["Multi", "Factor", "Auth"],
            "SSO": ["Single", "Sign", "On"],
            "RBAC": ["Role", "Based", "Access", "Ctrl"],
            "ACL": ["Access", "Ctrl", "List"],
            "DMZ": ["De", "Mil", "Zone"],
            "IDS": ["Intrusion", "Detect", "System"],
            "IPS": ["Intrusion", "Prev", "System"],
            
            # Data formats
            "JSON": ["Java", "Script", "Object", "Not"],
            "XML": ["Extend", "Markup", "Lang"],
            "CSV": ["Comma", "Sep", "Values"],
            "YAML": ["YAML", "Ain't", "Markup", "Lang"],
            "SQL": ["Struct", "Query", "Lang"],
            "NoSQL": ["No", "SQL"],
            "DB": ["Data", "Base"],
            
            # Algorithms  
            "AES": ["Adv", "Encr", "Std"],
            "RSA": ["RSA"],
            "MD5": ["Message", "Digest", "5"],
            "SHA": ["Secure", "Hash", "Algo"],
            "DES": ["Data", "Encr", "Std"],
            "CRC": ["Cyclic", "Red", "Check"],
            
            # Circuit components
            "IC": ["Integrated", "Circuit"],
            "ROM": ["Read", "Only", "Mem"],
            "ALU": ["Arith", "Logic", "Unit"],
            "FPU": ["Float", "Point", "Unit"],
            "MMU": ["Mem", "Mgmt", "Unit"],
            "DMA": ["Direct", "Mem", "Access"],
            
            # Threading
            "SMP": ["Sym", "Multi", "Proc"],
            "NUMA": ["Non", "Uniform", "Mem", "Access"],
            "SIMD": ["Single", "Instr", "Multi", "Data"],
            "MIMD": ["Multi", "Instr", "Multi", "Data"],
            
            # Cloud services
            "AWS": ["Amazon", "Web", "Services"],
            "GCP": ["Google", "Cloud", "Platform"],
            "EC2": ["Elastic", "Compute", "Cloud"],
            "S3": ["Simple", "Storage", "Service"],
            "RDS": ["Relational", "Database", "Service"],
            "ECS": ["Elastic", "Container", "Service"],
            "EKS": ["Elastic", "Kubernetes", "Service"],
            "CDN": ["Content", "Delivery", "Network"]
        }
        
        # Check if word is a known infrastructure abbreviation
        if word in infrastructure_abbreviations:
            return infrastructure_abbreviations[word]
        
        # Handle camelCase
        camel_pattern = re.sub(r'([a-z])([A-Z])', r'\1 \2', word)

        # Split on common technical separators
        sub_words = re.split(r'[_\-\s]+', camel_pattern)

        # Further split compound words
        result = []
        for sub_word in sub_words:
            if len(sub_word) > 8:  # Split long compound words
                # Simple rule-based splitting for technical terms
                if 'Network' in sub_word:
                    result.extend(['Net', 'Work'])
                elif 'Algorithm' in sub_word:
                    result.extend(['Algo', 'Rithm'])
                elif 'Protocol' in sub_word:
                    result.extend(['Proto', 'Col'])
                elif 'Architecture' in sub_word:
                    result.extend(['Arch', 'itecture'])
                elif 'Infrastructure' in sub_word:
                    result.extend(['Infra', 'structure'])
                elif 'Configuration' in sub_word:
                    result.extend(['Config', 'uration'])
                elif 'Management' in sub_word:
                    result.extend(['Mgmt'])
                else:
                    result.append(sub_word)
            else:
                result.append(sub_word)

        return [w for w in result if w]  # Remove empty strings

    def _calculate_ratio(self, word: str, sub_words: List[str]) -> float:
        """Calculate compression ratio for the word"""
        original_length = len(word)
        sub_words_length = sum(len(w) for w in sub_words)
        return round(sub_words_length / original_length, 2) if original_length > 0 else 1.0

    def _calculate_weight(self, word: str, category: CategoryType) -> float:
        """Calculate weight based on word complexity and category importance"""
        base_weight = len(word) / 10.0

        # Category-based weight adjustments
        category_weights = {
            CategoryType.IA_ARCHITECTURE: 1.5,
            CategoryType.CIRCUIT_COMPONENTS: 1.3,
            CategoryType.ALGORITHMS: 1.4,
            CategoryType.SECURITY_CONCEPTS: 1.2,
            CategoryType.PHYSICAL_PROPERTIES: 1.0,
            CategoryType.COMPUTER_VERBS: 0.8,
            CategoryType.DATA_STRUCTURES: 1.1,
            CategoryType.NETWORK_PROTOCOLS: 1.0,
            CategoryType.THREADING_CONCEPTS: 1.0,
        }

        return round(base_weight * category_weights.get(category, 1.0), 2)

    def _extract_parameters(self, word: str, category: CategoryType) -> List[str]:
        """Extract relevant parameters for the word based on its category"""
        parameters = []

        if category == CategoryType.PHYSICAL_PROPERTIES:
            parameters = ["value", "unit", "range", "precision"]
        elif category == CategoryType.COMPUTER_VERBS:
            parameters = ["input", "output", "complexity", "side_effects"]
        elif category == CategoryType.IA_ARCHITECTURE:
            parameters = ["dimensions", "activation", "weights", "bias"]
        elif category == CategoryType.CIRCUIT_COMPONENTS:
            parameters = ["inputs", "outputs", "delay", "power"]
        elif category == CategoryType.DATA_STRUCTURES:
            parameters = ["size", "operations", "access_time", "memory"]
        elif category == CategoryType.ALGORITHMS:
            parameters = ["complexity", "space", "stability", "optimality"]
        elif category == CategoryType.NETWORK_PROTOCOLS:
            parameters = ["port", "reliability", "security", "speed"]
        elif category == CategoryType.SECURITY_CONCEPTS:
            parameters = ["strength", "algorithm", "key_size", "vulnerability"]
        elif category == CategoryType.THREADING_CONCEPTS:
            parameters = ["thread_id", "process_id", "priority", "affinity"]

        return parameters

    def create_logic_circuit(self, name: str, request_items: List[Tuple[str, CategoryType]]) -> LogicCircuit:
        """Create a logic circuit for processing a request from (word, category) items"""
        compact_elements: List[CompactWord] = []
        inputs: List[str] = []
        outputs: List[str] = []
        operations: List[str] = []
        op_categories: List[CategoryType] = []

        for word, category in request_items:
            mapping = self.compact_mappings_by_category.get(category, {}).get(word)
            if mapping:
                compact_elements.append(mapping)
                inputs.extend(mapping.parameters)

                # Define operations based on explicit category
                if category == CategoryType.COMPUTER_VERBS:
                    operations.append(f"{mapping.compact_label}: {mapping.original}")
                    op_categories.append(CategoryType.COMPUTER_VERBS)
                elif category == CategoryType.IA_ARCHITECTURE:
                    operations.append(f"{mapping.compact_label} = IA_PROCESS({mapping.original})")
                    op_categories.append(CategoryType.IA_ARCHITECTURE)
                elif category == CategoryType.CIRCUIT_COMPONENTS:
                    operations.append(f"{mapping.compact_label} = CIRCUIT({mapping.original})")
                    op_categories.append(CategoryType.CIRCUIT_COMPONENTS)
                else:
                    operations.append(f"{mapping.compact_label} = {mapping.original}")
                    op_categories.append(category)

        # Generate outputs based on operations
        outputs = [f"result_{i}" for i in range(len(operations))]

        circuit = LogicCircuit(
            name=name,
            inputs=list(set(inputs)),  # Remove duplicates
            outputs=outputs,
            operations=operations,
            compact_elements=compact_elements,
            operation_categories=op_categories
        )

        self.logic_circuits.append(circuit)
        return circuit

    def get_compact_representation(self, items: List[Tuple[str, CategoryType]]) -> Dict:
        """Get compact representation for a sequence of (word, category) items"""
        representation = {
            "compact_labels": [],
            "ratios": [],
            "weights": [],
            "mathematical_expression": "",
            "parameters": {}
        }

        labels: List[str] = []
        for word, category in items:
            mapping = self.compact_mappings_by_category.get(category, {}).get(word)
            if mapping:
                labels.append(mapping.compact_label)
                representation["compact_labels"].append({
                    "label": mapping.compact_label,
                    "original": mapping.original,
                    "sub_words": mapping.sub_words,
                    "category": mapping.category.value
                })
                representation["ratios"].append(mapping.ratio)
                representation["weights"].append(mapping.weight)
                representation["parameters"][mapping.compact_label] = mapping.parameters

        # Create mathematical expression
        if labels:
            representation["mathematical_expression"] = " + ".join(labels)
            if len(labels) > 1:
                representation["mathematical_expression"] += f" = {len(labels)}*AVG({', '.join(labels)})"

        return representation

    def enable_hyperthreading(self, enabled: bool = True, cores: int = 1, threads_per_core: int = 2):
        """Configure hyperthreading on the computer axis."""
        self.execution_axis.hyperthreading = bool(enabled)
        self.execution_axis.cores = max(1, int(cores))
        self.execution_axis.threads_per_core = max(1, int(threads_per_core))

    def configure_time_axis(self, timeslice_ms: int = 10, dataset_size: int = 1, chunk_size: int = 1):
        """Configure the time axis for dataset-wide processing."""
        self.time_axis.timeslice_ms = max(1, int(timeslice_ms))
        self.time_axis.dataset_size = max(1, int(dataset_size))
        self.time_axis.chunk_size = max(1, int(chunk_size))

    def enable_race_condition_scheduler(self, enabled: bool = True):
        """Enable or disable the 6pm race condition scheduler."""
        self.race_scheduler.enabled = enabled
        if enabled:
            self.race_scheduler._schedule_next_6pm()
        print(f"Race condition scheduler {'enabled' if enabled else 'disabled'}")
        if enabled and self.race_scheduler.next_6pm_trigger:
            print(f"Next 6pm trigger scheduled for: {self.race_scheduler.next_6pm_trigger}")

    def get_race_condition_status(self) -> Dict:
        """Get current status of the race condition scheduler."""
        return {
            "enabled": self.race_scheduler.enabled,
            "next_6pm_trigger": self.race_scheduler.next_6pm_trigger.isoformat() if self.race_scheduler.next_6pm_trigger else None,
            "race_condition_active": self.race_scheduler.race_condition_active,
            "turn_counter": self.race_scheduler.turn_counter,
            "all_words_count": len(self.race_scheduler.all_words_buffer)
        }

    def _should_enable_hyperthreading(self, words_only: List[str]) -> bool:
        signal_words = {"hyperthread", "hyperthreading", "parallel", "parallelism", "concurrency", "thread"}
        wset = {w.lower() for w in words_only}
        return self.execution_axis.hyperthreading or any(w in wset for w in signal_words)

    def _plan_execution_and_time(self, circuit: LogicCircuit, words_only: List[str]) -> Tuple[Dict, Dict]:
        """Plan hyperthreaded execution for computer verbs and link to time axis over entire dataset."""
        ht = self._should_enable_hyperthreading(words_only)
        axis = self.execution_axis
        tids = axis.thread_ids() if ht else ["C0_T0"]

        # Identify indices of computer verbs
        verb_indices = [i for i, cat in enumerate(circuit.operation_categories) if cat == CategoryType.COMPUTER_VERBS]
        nonverb_indices = [i for i in range(len(circuit.operations)) if i not in verb_indices]

        if ht and verb_indices:
            assignment_indices = axis.schedule_round_robin_indices(verb_indices)
        else:
            assignment_indices = {tids[0]: verb_indices[:]}

        # Serialize non-verb ops on the primary thread
        if tids[0] not in assignment_indices:
            assignment_indices[tids[0]] = []
        assignment_indices[tids[0]].extend(nonverb_indices)

        # Also produce a human-readable mapping
        assignment_strings: Dict[str, List[str]] = {
            tid: [circuit.operations[i] for i in idxs] for tid, idxs in assignment_indices.items()
        }

        execution_plan = {
            "hyperthreading": ht,
            "cores": axis.cores,
            "threads_per_core": axis.threads_per_core if ht else 1,
            "total_threads": axis.total_threads() if ht else 1,
            "assignment_indices": assignment_indices,
            "assignment": assignment_strings,
        }

        # Time axis plan over the entire dataset
        time_plan = self.time_axis.compute_timeline(assignment_indices, circuit)
        return execution_plan, time_plan

    def _total_computer_verbs_length(self, items: List[Tuple[str, CategoryType]]) -> int:
        return sum(len(word) for (word, category) in items if category == CategoryType.COMPUTER_VERBS)

    def _process_race_condition_detection(self, items: List[Tuple[str, CategoryType]]) -> Tuple[List[Tuple[str, CategoryType]], Optional[Dict]]:
        """Process race condition detection and parallel injection logic.
        
        This method encapsulates the complex race condition detection logic that:
        1. Calculates verb length decay between sequential requests
        2. Injects parallelism when decay exceeds threshold (2.348x)
        3. Tracks trigger information for diagnostics
        4. Updates historical state for future comparisons
        
        Returns:
            Tuple of updated items list and optional trigger information
        """
        return self._inject_parallel_if_decay(items)
    
    def _inject_parallel_if_decay(self, items: List[Tuple[str, CategoryType]]) -> Tuple[List[Tuple[str, CategoryType]], Optional[Dict]]:
        """If Computer Verbs' total length decreased > 2.348x vs last check, add 'Parallelism'."""
        curr = self._total_computer_verbs_length(items)
        trigger_info = None
        if self._last_verb_total_len is not None and curr > 0:
            factor = self._last_verb_total_len / curr
            if factor > 2.348:
                # Append Parallelism from threading concepts
                if not any(w == "Parallelism" for (w, _c) in items):
                    items = items + [("Parallelism", CategoryType.THREADING_CONCEPTS)]
                trigger_info = {
                    "trigger": "verb_length_decay",
                    "last_total": self._last_verb_total_len,
                    "current_total": curr,
                    "factor": round(factor, 3)
                }
        # Update history after check
        self._last_verb_total_len = curr
        return items, trigger_info

    def process_request(self, request: str) -> Dict:
        # Check for 6pm race condition trigger
        race_triggered = self.race_scheduler.check_6pm_trigger()
        race_condition_info = None
        
        # 1) Detect words as (word, category) items
        items: List[Tuple[str, CategoryType]] = []
        req_lc = request.lower()
        
        # If race condition is active, use all words from all categories
        if race_triggered or self.race_scheduler.race_condition_active:
            race_words = self.race_scheduler.prepare_all_words_race(self.categories)
            # Convert race words to proper format for processing
            for word, category_name in race_words:
                category = CategoryType(category_name)
                items.append((word, category))
            
            race_condition_info = {
                "trigger": "6pm_turn_race_condition",
                "turn_counter": self.race_scheduler.turn_counter,
                "total_words_processed": len(race_words),
                "analyze_cycles": "random 2-4 cycles as specified"
            }
            
            # Deactivate race condition after processing
            self.race_scheduler.deactivate_race_condition()
        else:
            # Normal processing - detect words from request
            for category, category_words in self.categories.items():
                for word in category_words:
                    if word.lower() in req_lc:
                        items.append((word, category))
        
        if not items:
            return {"status": "DENY", "reason": "No technical words found in request"}

        # Process race condition detection and parallel injection
        items, trigger_info = self._process_race_condition_detection(items)

        # Prepare a words-only list for display/planning
        words_only = [w for (w, _c) in items]

        # 2) Compact representation
        compact_rep = self.get_compact_representation(items)

        # 3) Build circuit
        circuit = self.create_logic_circuit(f"circuit_{len(self.logic_circuits) + 1}", items)

        # 4) Plan execution + time
        execution_plan, time_plan = self._plan_execution_and_time(circuit, words_only)

        result = {
            "status": "APPROVE",
            "request": request,
            "identified_words": words_only,
            "compact_representation": compact_rep,
            "logic_circuit": {
                "name": circuit.name,
                "inputs": circuit.inputs,
                "outputs": circuit.outputs,
                "operations": circuit.operations,
            },
            "execution_plan": execution_plan,
            "time_axis_plan": time_plan,
            "evolution_principle": "Compact representation with sub-word decomposition for IA architecture mapping",
        }
        if trigger_info:
            result["parallel_trigger"] = trigger_info
        if race_condition_info:
            result["race_condition"] = race_condition_info
        return result

    def export_categories(self) -> Dict:
        """Export all categories and their compact mappings"""
        export_data: Dict[str, Dict] = {}
        for category, words in self.categories.items():
            export_data[category.value] = {
                "words": words,
                "compact_mappings": {
                    word: {
                        "label": self.compact_mappings_by_category[category][word].compact_label,
                        "sub_words": self.compact_mappings_by_category[category][word].sub_words,
                        "ratio": self.compact_mappings_by_category[category][word].ratio,
                        "weight": self.compact_mappings_by_category[category][word].weight,
                        "parameters": self.compact_mappings_by_category[category][word].parameters
                    } for word in words if word in self.compact_mappings_by_category[category]
                }
            }
        return export_data


def main():
    """Main function to demonstrate the Compact Evolution Resource Principles system"""
    system = CompactEvolutionSystem()

    # Configure axes: enable hyperthreading and set a dataset for the time axis
    system.enable_hyperthreading(True, cores=2, threads_per_core=2)
    system.configure_time_axis(timeslice_ms=5, dataset_size=20, chunk_size=5)

    printc("=== Compact Evolution Resource Principles ===\n")

    # Sample request mentions processing and storage across the entire dataset
    sample_request = "Process and Store the NeuralNetwork across entire dataset with hyperthreading in memory"
    result = system.process_request(sample_request)

    printc(f"Request: {sample_request}")
    printc(f"Status: {result['status']}")

    if result['status'] == 'APPROVE':
        printc(f"Identified words: {result['identified_words']}")
        printc(f"Compact representation: {result['compact_representation']['mathematical_expression']}")
        printc(f"Logic circuit: {result['logic_circuit']['name']}")
        printc(f"Operations: {result['logic_circuit']['operations']}")
        printc("Execution plan (computer axis):")
        ep = result["execution_plan"]
        printc(f"  Enabled: {ep['hyperthreading']}, Cores: {ep['cores']}, Threads/Core: {ep['threads_per_core']}, Total threads: {ep['total_threads']}")
        for tid, ops in ep["assignment"].items():
            printc(f"  {tid}: {ops}")
        printc("Time axis plan (timeline excerpts):")
        tp = result["time_axis_plan"]
        printc(f"  Timeslice: {tp['timeslice_ms']}ms, Dataset: {tp['dataset_size']} items, Chunk: {tp['chunk_size']}")
        # Show first 2 entries per thread
        for tid, segments in tp["timeline"].items():
            printc(f"  {tid}: {segments[:2]} ...")

    printc("\n=== Category Export Example ===")
    categories = system.export_categories()
    for category_name, category_data in list(categories.items())[:2]:  # Show first 2 categories
        printc(f"\n{category_name.upper()}:")
        for word, mapping in list(category_data['compact_mappings'].items())[:3]:  # Show first 3 words
            printc(f"  {word} -> {mapping['label']} (sub: {mapping['sub_words']}, ratio: {mapping['ratio']})")


if __name__ == "__main__":
    main()
