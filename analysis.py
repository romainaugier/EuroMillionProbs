import os
import re

import numpy as np

DATA_DIR = f"{os.getcwd()}/data"

FILE_NAME_RE = re.compile(r"euromillions_(\d{4})_(\d{4})\.csv")

if __name__ == "__main__":
    data = list()

    for entry in os.scandir(DATA_DIR):
        m = FILE_NAME_RE.match(entry.name)

        if m is not None:
            index = 4 if int(m.group(1)) < 2016 else 5

            with open(entry.path, "r") as file:
                text = file.read()

                nums = list()

                for line in text.splitlines()[1:]:
                    line_split = line.split(';')

                    nums.append([line_split[0], *line_split[index:12]])

                data.extend(nums)

    data = sorted(data, key=lambda x: x[0])

    ball1_count = dict()
    ball2_count = dict()
    ball3_count = dict()
    ball4_count = dict()
    ball5_count = dict()
    star1_count = dict()
    star2_count = dict()

    for d in data:
        ball1_counter = ball1_count.get(d[1], 0)
        ball1_count[d[1]] = ball1_counter + 1

        ball2_counter = ball2_count.get(d[2], 0)
        ball2_count[d[2]] = ball2_counter + 1

        ball3_counter = ball3_count.get(d[3], 0)
        ball3_count[d[3]] = ball3_counter + 1

        ball4_counter = ball4_count.get(d[4], 0)
        ball4_count[d[4]] = ball4_counter + 1

        ball5_counter = ball5_count.get(d[5], 0)
        ball5_count[d[5]] = ball5_counter + 1

        star1_counter = star1_count.get(d[6], 0)
        star1_count[d[6]] = star1_counter + 1

        star2_counter = star2_count.get(d[7], 0)
        star2_count[d[7]] = star2_counter + 1

    counters = [
        (ball1_count, "First Ball"),
        (ball2_count, "Second Ball"),
        (ball3_count, "Third Ball"),
        (ball4_count, "Fourth Ball"),
        (ball5_count, "Fifth Ball"),
        (star1_count, "First Star"),
        (star2_count, "Second Star")
    ]

    for counter, name in counters:
        nums = np.array(list(counter.keys()), dtype=np.int32)
        counts = np.array(list(counter.values()), dtype=np.int32)

        probs = counts.astype(np.float64) / float(counts.sum())

        num = np.random.choice(nums, p=probs)

        print(f"{name}: {num}")
