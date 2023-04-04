import random

def get_random_time(duration):
    # Read the list of bad time intervals from a file
    with open('bad_times.txt') as f:
        intervals = []
        for line in f:
            start, end = line.strip().split('-')
            if start == 'end':
                final_end_time = int(end)
                break
            intervals.append((int(start), int(end)))

    # Generate a random start time and duration
    while True:
        start_time = random.uniform(0, final_end_time)
        total_duration = duration
        end_time = start_time + total_duration

        if end_time > final_end_time:
            continue

        # Check if the time falls within any of the intervals
        overlaps = False
        for interval in intervals:
            print(interval[0], interval[1])
            if interval[0] <= start_time < interval[1] or \
                    interval[0] < end_time <= interval[1] or \
                    start_time <= interval[0] and end_time + total_duration >= interval[1]:
                overlaps = True

        # If the time doesn't overlap any interval, print it and break out of the loop
        if not overlaps:
            # print(f"Start time: {start_time:.2f}, Duration: {total_duration:.2f}")
            return start_time
