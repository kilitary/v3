from compact_evolution import CompactEvolutionSystem


def run():
    s = CompactEvolutionSystem()
    # Keep hyperthreading disabled globally to rely solely on the injected Parallelism signal
    s.enable_hyperthreading(False, cores=2, threads_per_core=2)
    s.configure_time_axis(timeslice_ms=5, dataset_size=10, chunk_size=5)

    # First request: long verbs total length (e.g., Validate(8)+Transform(9)+Calculate(9)=26)
    r1 = s.process_request("Validate Transform Calculate in memory")
    print("R1 identified:", r1.get("identified_words"))
    print("R1 parallel_trigger:", r1.get("parallel_trigger"))

    # Second request: short verb total length (e.g., Parse(5)) => 26/5 = 5.2 > 2.348
    r2 = s.process_request("Parse in memory")
    print("R2 identified:", r2.get("identified_words"))
    print("R2 parallel_trigger:", r2.get("parallel_trigger"))
    print("R2 hyperthreading enabled:", r2.get("execution_plan", {}).get("hyperthreading"))


if __name__ == "__main__":
    run()

