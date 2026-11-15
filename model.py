# model.py - shared settings and simple formulas (all SIMULATED)
LINKS = ["Core1-Edge1", "Core1-Edge4", "Core2-Edge3", "Core2-Edge4"]  # rename to match your topology

CONGESTION_UTIL = 80    # % utilization above this = congestion
LOSS_LIMIT = 5          # % packet loss above this = high loss
TARGET_UTIL = 70        # utilization we try to bring a congested link down to
LINK_CAPACITY_MBPS = 1000

def latency_from_util(util):
    # latency rises sharply as a link fills up (simulated model)
    return round(2 + (util / 100) ** 3 * 80, 2)

def loss_from_util(util):
    # loss only starts when the link is above 80% (simulated model)
    return round(max(0.0, util - 80) * 0.4, 2)

def power_from_util(util):
    # estimated power in watts: 5 W idle + 0.1 W per 1% utilization (ESTIMATE)
    return round(5 + 0.1 * util, 2)
