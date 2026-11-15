# evaluate.py - baseline vs optimized comparison (SIMULATED)
import pandas as pd
import matplotlib.pyplot as plt
from model import *

df = pd.read_csv("decisions.csv")
df["throughput_mbps"] = (df["utilization"] * LINK_CAPACITY_MBPS / 100 * (1 - df["packet_loss"] / 100)).round(2)

# ---- apply the optimization: move excess traffic from congested link to least-used link ----
opt = df.copy()
for (scenario, step), group in df.groupby(["scenario", "step"]):
    for idx, row in group.iterrows():
        if row["state"] == "CONGESTION":
            excess = row["utilization"] - TARGET_UTIL
            candidates = group[(group["status"] == "up") & (group["state"] != "CONGESTION")]
            target_idx = candidates["utilization"].idxmin()
            opt.loc[idx, "utilization"] -= excess
            opt.loc[target_idx, "utilization"] += excess

# recompute metrics for links that are up
up = opt["status"] == "up"
opt.loc[up, "latency_ms"] = opt.loc[up, "utilization"].apply(latency_from_util)
opt.loc[up, "packet_loss"] = opt.loc[up, "utilization"].apply(loss_from_util)
opt.loc[up, "power_w"] = opt.loc[up, "utilization"].apply(power_from_util)
opt["throughput_mbps"] = (opt["utilization"] * LINK_CAPACITY_MBPS / 100 * (1 - opt["packet_loss"] / 100)).round(2)

# ---- summarise ----
def summarise(d):
    u = d[d["status"] == "up"]
    return {
        "avg_latency_ms": u["latency_ms"].mean(),
        "avg_packet_loss_pct": u["packet_loss"].mean(),
        "max_utilization_pct": u["utilization"].max(),
        "avg_throughput_mbps": u["throughput_mbps"].mean(),
        "avg_power_w": u["power_w"].mean(),
    }

rows = []
for sc in ["A", "B", "C"]:
    b = summarise(df[df["scenario"] == sc])
    o = summarise(opt[opt["scenario"] == sc])
    for metric in b:
        rows.append({
            "scenario": sc,
            "metric": metric,
            "baseline": round(b[metric], 2),
            "optimized": round(o[metric], 2),
            "difference": round(o[metric] - b[metric], 2)
        })

table = pd.DataFrame(rows)
table.to_csv("results_summary.csv", index=False)
print(table.to_string(index=False))

# ---- chart for Scenario B ----
bsc = table[table["scenario"] == "B"]
metrics = ["avg_latency_ms", "avg_packet_loss_pct", "max_utilization_pct"]
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, m in zip(axes, metrics):
    r = bsc[bsc["metric"] == m].iloc[0]
    ax.bar(["Baseline", "Optimized"], [r["baseline"], r["optimized"]], color=["red", "green"])
    ax.set_title(m)
fig.suptitle("Scenario B (Congested): Baseline vs Optimized (simulated)")
plt.tight_layout()
plt.savefig("comparison_chart.png", dpi=150)
print("\nSaved comparison_chart.png")
