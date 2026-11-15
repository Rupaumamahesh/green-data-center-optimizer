# decision_engine.py - detects problems and recommends actions
import pandas as pd
from model import CONGESTION_UTIL, LOSS_LIMIT

def decide(row, group):
    """row = one link at one time step, group = all links at that time step"""
    if row["status"] == "down":
        return "LINK_FAILURE", "Link is down. Rely on HSRP/redundant path and investigate the port or cable."
    if row["utilization"] > CONGESTION_UTIL:
        others = group[(group["link"] != row["link"]) & (group["status"] == "up")]
        best = others.sort_values("utilization").iloc[0]["link"]
        return "CONGESTION", f"Recommend shifting traffic from {row['link']} to {best}"
    if row["packet_loss"] > LOSS_LIMIT:
        return "HIGH_LOSS", f"Investigate {row['link']} for errors or faults"
    return "NORMAL", "No action needed"

df = pd.read_csv("traffic_data.csv")
results = []
for (scenario, step), group in df.groupby(["scenario", "step"]):
    for _, row in group.iterrows():
        state, action = decide(row, group)
        record = row.to_dict()
        record["state"] = state
        record["action"] = action
        results.append(record)

out = pd.DataFrame(results)
out.to_csv("decisions.csv", index=False)

print("Decision counts per scenario:")
print(out.groupby(["scenario", "state"]).size())
print()
print("Example decisions:")
print(out[out["state"] != "NORMAL"][["scenario", "step", "link", "state", "action"]].head(5).to_string(index=False))
