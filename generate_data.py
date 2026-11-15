# generate_data.py - creates simulated traffic metrics
import csv
import random
from model import *

random.seed(42)  # same numbers every time you run it
STEPS = 20

def make_row(scenario, step, link):
    status = "up"
    if scenario == "A":  # normal traffic
        util = random.uniform(20, 50)
    elif scenario == "B":  # congested traffic
        if link == "Core1-Edge1":
            util = random.uniform(85, 98)
        else:
            util = random.uniform(20, 45)
    else:  # C: link failure
        if link == "Core1-Edge1":
            util, status = 0, "down"
        elif link == "Core1-Edge4":
            util = random.uniform(60, 75)  # takes extra traffic
        else:
            util = random.uniform(20, 45)

    if status == "down":
        latency, loss, power = 0, 100, 0
    else:
        latency = latency_from_util(util)
        loss = loss_from_util(util)
        power = power_from_util(util)

    return [scenario, step, link, status, round(util, 2), latency, loss, power]

rows = []
for scenario in ["A", "B", "C"]:
    for step in range(1, STEPS + 1):
        for link in LINKS:
            rows.append(make_row(scenario, step, link))

with open("traffic_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["scenario", "step", "link", "status", "utilization", "latency_ms", "packet_loss", "power_w"])
    writer.writerows(rows)

print("traffic_data.csv created with", len(rows), "rows")
