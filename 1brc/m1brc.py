import os
import multiprocessing as mp
import time
from datetime import timedelta

def get_file_chunks(filename, max_cpu = 8):
    cpu_count = min(max_cpu, mp.cpu_count())

    file_size = os.path.getsize(filename)
    chunk_size = file_size // cpu_count

    chunks = []
    with open(filename, "rb") as f:
        def is_newline(position):
            if position == 0:
                return True
            
            f.seek(position) - 1
            return f.read(1) == b"\n"
        
        def next_line(position):
            f.seek(position)
            f.readline()
            return f.tell()
    
        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = min(file_size, chunk_start + chunk_size)

            while not is_newline(chunk_end):
                chunk_end -= 1

            if chunk_start == chunk_end:
                chunk_end = next_line(chunk_end)

            chunks.append((filename, chunk_start, chunk_end))

            chunk_start = chunk_end
    
    return (cpu_count, chunks)

def process_chunk(filename, start, end, blocksize = 1024 * 1024):
    result = dict()

    with open(filename, "rb") as f:
        f.seek(start)

        tail = b""
        location = None
        byte_count = end - start

        while byte_count > 0:
            if blocksize > byte_count:
                blocksize = byte_count
            byte_count -= blocksize

            idx = 0
            data = tail + f.read(blocksize)
            while data:
                if location is None:
                    try:
                        semicolon = data.index(b";", idx)
                    except ValueError:
                        tail = data[idx:]
                        break

                    location = data[idx:semicolon]
                    idx = semicolon + 1
                
                try:
                    newline = data.index(b"\n", idx)
                except ValueError:
                    tail = data[idx:]
                    break

                value = float(data[idx:newline])
                idx = newline + 1
                
                if location not in result:
                    result[location] = [value, value, value, 1]
                else:
                    r = result[location]
                    r[0] = min(r[0], value)
                    r[1] = max(r[1], value)
                    r[2] += value
                    r[3] += 1
                    
                
                location = None
        return result


def process_file(cpu_count, chunks):
    with mp.Pool(cpu_count) as p:
        # Run chunks in parallel
        chunk_results = p.starmap(
            process_chunk,
            chunks,
        )

    # Combine all results from all chunks
    result = dict()
    for chunk_result in chunk_results:
        for location, measurements in chunk_result.items():
            if location not in result:
                result[location] = measurements
            else:
                r = result[location]
                r[0] = min(r[0], measurements[0])
                r[1] = max(r[1], measurements[1])
                r[2] += measurements[2]
                r[3] += measurements[3]

    # Print final results
    print("{", end="")
    for location, measurements in sorted(result.items()):
        print(
            f"{location.decode('utf-8')}={measurements[0]:.1f}/{(measurements[2] / measurements[3]) if measurements[3] !=0 else 0:.1f}/{measurements[1]:.1f}",
            end=", ",
        )
    print("\b\b} ")


if __name__ == "__main__":
    start_time = time.monotonic()

    cpu_count, *start_end = get_file_chunks("measurements.txt")
    
    process_file(cpu_count, start_end[0])

    time_elapsed = round(time.monotonic() - start_time, 2)


    print(f"Total application time: {timedelta(seconds=time_elapsed)}")