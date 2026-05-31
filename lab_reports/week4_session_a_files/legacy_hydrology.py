#!/usr/bin/env python3
# Legacy watershed runoff tool — DO NOT EDIT (keep for Week 4 comparison)
# Author: unknown (circa 2018 port from spreadsheet macros)

import csv
import time
import urllib.request

# global state used everywhere
STATE = {"total_q": 0.0, "rows": []}


def calc(x, y):
    # x = P mm, y = CN
    s = 25400 / y - 254
    ia = 0.2 * s
    if x <= ia:
        return 0
    return (x - ia) * (x - ia) / (x - ia + s)


def fetch_rainfall(url, cb_ok, cb_err):
    """Callback-style HTTP fetch (legacy)."""

    def _done(raw):
        try:
            val = float(raw.decode().strip())
            cb_ok(val)
        except Exception:
            cb_err("bad data")

    try:
        resp = urllib.request.urlopen(url, timeout=2)
        _done(resp.read())
    except Exception:
        cb_err("network fail")


def process(path):
    # 80-line god function: load csv, fake API per row, aggregate, print
    global STATE
    STATE = {"total_q": 0.0, "rows": []}
    f = open(path, "r")
    r = csv.reader(f)
    hdr = next(r)
    data2 = []
    for line in r:
        data2.append(line)
    f.close()

    for i in range(len(data2)):
        row = data2[i]
        eid = row[0]
        ws = row[1]
        p = float(row[2])
        lu = row[3]
        # duplicate CN lookup inline (smell: duplication)
        cn = 80
        if lu == "forest":
            cn = 70
        elif lu == "pasture":
            cn = 80
        elif lu == "cultivated":
            cn = 85
        elif lu == "residential":
            cn = 90
        elif lu == "paved":
            cn = 98

        # blocking "API" delay per row (smell: sync in loop)
        time.sleep(0.01)

        results = []

        def on_ok(v):
            results.append(v)

        def on_err(msg):
            results.append(p)  # silent fallback — smell: weak errors

        fetch_rainfall("https://httpbin.org/bytes/8", on_ok, on_err)

        p_use = results[0] if results else p
        # duplicate formula again instead of calling calc (smell)
        s2 = 25400 / cn - 254
        ia2 = 0.2 * s2
        if p_use <= ia2:
            q = 0
        else:
            q = (p_use - ia2) ** 2 / (p_use - ia2 + s2)
        if q > p_use:
            q = p_use

        STATE["rows"].append((eid, ws, p_use, lu, cn, q))
        STATE["total_q"] = STATE["total_q"] + q

    print("=== LEGACY RUNOFF REPORT ===")
    print("event  watershed  P_mm  land_use  CN  Q_mm")
    for item in STATE["rows"]:
        print(
            "%5s  %9s  %5.1f  %10s  %2d  %8.4f"
            % (item[0], item[1], item[2], item[3], item[4], item[5])
        )
    print("TOTAL Q =", STATE["total_q"])


if __name__ == "__main__":
    import sys

    pth = "data/events.csv"
    if len(sys.argv) > 1:
        pth = sys.argv[1]
    try:
        process(pth)
    except:
        print("failed")
