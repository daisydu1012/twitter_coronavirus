#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

try:
    import matplotlib
    matplotlib.use("Agg")  # needed on servers without display
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ModuleNotFoundError:
    HAS_MPL = False

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values args.percent:
#    for k in counts[args.key]:
#       counts[args.key][k] /= counts['_all'][k]

# get the count values for this key
items = list(counts[args.key].items())

# if percent flag, normalize by the overall totals in _all
if args.percent:
    items = [(k, v / counts['_all'][k]) for k, v in items if k in counts['_all'] and counts['_all'][k] != 0]

# sort high -> low, take top 10
items = sorted(items, key=lambda item: (item[1], item[0]), reverse=True)[:10]

# then sort low -> high for plotting
items = sorted(items, key=lambda item: (item[1], item[0]))

labels = [k for k, _ in items]
values = [v for _, v in items]

if not HAS_MPL:
    print("matplotlib not available; printing top 10 instead:\n")
    for k, v in items[::-1]:  # reverse so it's high -> low when printing
        print(f"{k}\t{v}")
    raise SystemExit(0)

# --- make a bar chart and save as png ---
try:
    import matplotlib
    matplotlib.use("Agg")  # needed on servers without display
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ModuleNotFoundError:
    HAS_MPL = False

outname = f"{os.path.basename(args.input_path)}.{args.key.replace('#','')}"
if args.percent:
    outname += ".percent"
outname += ".png"

plt.figure(figsize=(10, 5))
plt.bar(labels, values)          # horizontal bars = readable labels
plt.xlabel("key")
plt.ylabel("value")
plt.xticks(rotation=45, ha="right")
plt.title(f"Top 10 for {args.key}")
plt.tight_layout()
plt.savefig(outname, dpi=200)
print("saved", outname)
