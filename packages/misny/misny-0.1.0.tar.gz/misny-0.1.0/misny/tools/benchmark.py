import time
import numpy as np
import os
import sqlite3
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_benchmark_multiple_times(benchmark_func, iterations=10, warmup=True):
    if warmup:
        benchmark_func()
    
    times = []
    for _ in tqdm(range(iterations), desc=benchmark_func.__name__, leave=False):
        start_time = time.time()
        benchmark_func()
        end_time = time.time()
        times.append(end_time - start_time)
    
    return times  # Return all times for visualization

def cpu_benchmark_single_core():
    result = 0
    for i in range(1, 1000000):
        result += (i ** 0.5) ** 2

def cpu_benchmark_multicore(workers=4):
    def worker_task(start, end):
        result = 0
        for i in range(start, end):
            result += (i ** 0.5) ** 2
        return result

    chunk_size = 1000000 // workers
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(worker_task, i * chunk_size, (i + 1) * chunk_size) for i in range(workers)]
        results = [future.result() for future in as_completed(futures)]
    return sum(results)

def memory_benchmark():
    array_size = 10000000
    array = np.arange(array_size, dtype=np.float64)
    array *= 2

def disk_benchmark():
    with open('disk_benchmark.tmp', 'wb') as f:
        f.write(os.urandom(500000000))  # Write 500MB
    with open('disk_benchmark.tmp', 'rb') as f:
        f.read()
    os.remove('disk_benchmark.tmp')

def io_benchmark():
    with open('io_benchmark.tmp', 'w') as f:
        for _ in range(100000):
            f.write('This is a test.\n')
    os.remove('io_benchmark.tmp')

def peak_disk_write_benchmark(file_size_mb=500):
    data = os.urandom(file_size_mb * 1024 * 1024)  # Generate large data block
    file_path = 'peak_disk_write.tmp'
    
    start_time = time.time()
    with open(file_path, 'wb') as f:
        f.write(data)
        f.flush()  # Ensure all data is written
        os.fsync(f.fileno())  # Flush OS buffer to disk
    end_time = time.time()
    
    os.remove(file_path)  # Clean up
    
    elapsed_time = end_time - start_time
    throughput = file_size_mb / elapsed_time  # MB/s
    return throughput

def run_peak_disk_write_benchmark(iterations=5, file_size_mb=500):
    throughputs = []
    for _ in tqdm(range(iterations), desc="Peak Disk Write Benchmark", leave=False):
        throughput = peak_disk_write_benchmark(file_size_mb)
        throughputs.append(throughput)
    return throughputs

def save_benchmark_results(machine_id, benchmark_name, times):
    conn = sqlite3.connect('test_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS benchmark_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT,
            benchmark_name TEXT,
            time REAL
        )
    ''')
    for time in times:
        cursor.execute('''
            INSERT INTO benchmark_samples (machine_id, benchmark_name, time)
            VALUES (?, ?, ?)
        ''', (machine_id, benchmark_name, time))
    conn.commit()
    conn.close()

# Example usage
cpu_times = run_benchmark_multiple_times(lambda: cpu_benchmark_multicore(workers=os.cpu_count()), iterations=150)
memory_times = run_benchmark_multiple_times(memory_benchmark, iterations=150)
disk_times = run_benchmark_multiple_times(disk_benchmark, iterations=150)
io_times = run_benchmark_multiple_times(io_benchmark, iterations=150)
peak_disk_write_throughputs = run_peak_disk_write_benchmark(iterations=150)

save_benchmark_results('machine_A', 'CPU', cpu_times)
save_benchmark_results('machine_A', 'Memory', memory_times)
save_benchmark_results('machine_A', 'Disk', disk_times)
save_benchmark_results('machine_A', 'IO', io_times)
save_benchmark_results('machine_A', 'PeakDiskWrite', peak_disk_write_throughputs)

print("Benchmarking complete. Results saved to the database.")
