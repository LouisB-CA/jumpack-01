#!/usr/bin/env bash

#
# plot the charging data in the RDB file continuously
# as the data accummulates.
#
# See the ./docs/ directory for more info.
#

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sqlite3
import functools
from collections import deque

print = functools.partial(print, flush=True)
DB_PATH = "./charging.db"
INTERVAL_MS = 2500
MAX_POINTS = 600

times    = deque(maxlen=MAX_POINTS)
voltages = deque(maxlen=MAX_POINTS)
currents = deque(maxlen=MAX_POINTS)
last_id  = 0   # use id rather than timestamp for "new rows" tracking

conn = sqlite3.connect(DB_PATH)

fig, (ax_v, ax_c) = plt.subplots(2, 1, sharex=True, figsize=(11, 6))
fig.suptitle("Battery Charging Monitor", fontsize=13)

line_v, = ax_v.plot([], [], color="steelblue", linewidth=1)
line_c, = ax_c.plot([], [], color="tomato",    linewidth=1)

ax_v.set_ylabel("Bus Voltage (V)")
ax_v.set_ylim(10, 20)
ax_v.grid(True)

ax_c.set_ylabel("Current (A)")
ax_c.set_ylim(0.3, 0.5)
ax_c.set_xlabel("Sample ID")
ax_c.grid(True)

def update(frame):
    global last_id

    try:
        cur = conn.execute(
            "SELECT id, timestamp, bus_voltage_v, current_a FROM readings WHERE id > ? ORDER BY id",
            (last_id,)
        )
        rows = cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Query error: {e}")
        return line_v, line_c

    for row_id, ts, voltage, current in rows:
        times.append(ts.split('T')[1].split('.')[0])
        ## times.append(row_id)
        voltages.append(voltage if voltage is not None else float("nan"))
        currents.append(current if current is not None else float("nan"))
        last_id = row_id

    # print(voltages)

    if times:
        xs = range(len(voltages))
        line_v.set_data(xs, list(voltages))
        line_c.set_data(xs, list(currents))
        ax_v.set_xlim(0, max(1, len(voltages) - 1))
        ax_c.set_xlim(0, max(1, len(currents) - 1))

        # sparse x-axis tick labels showing actual timestamps
        n = len(times)
        step = max(1, n // 8)
        ticks = list(range(0, n, step))
        ax_c.set_xticks(ticks)
        ax_c.set_xticklabels([times[i] for i in ticks], rotation=25, ha="right", fontsize=7)

    return line_v, line_c

ani = animation.FuncAnimation(fig, update, interval=INTERVAL_MS, cache_frame_data=False)
plt.tight_layout()
plt.show()

conn.close()


