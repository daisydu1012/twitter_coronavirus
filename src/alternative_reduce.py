import re
from collections import defaultdict
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------- args ----------
parser = argparse.ArgumentParser()
parser.add_argument("hashtags", nargs="+")
parser.add_argument("--outputs_dir", default="outputs")
parser.add_argument("--output_png", default="task4.png")
args = parser.parse_args()


# ---------- data structure ----------
# counts[hashtag][day_of_year] = number
counts = defaultdict(lambda: defaultdict(int))


# ---------- loop over outputs ----------
files = glob.glob(os.path.join(args.outputs_dir, "*.lang"))

for path in files:
    filename = os.path.basename(path)

    # extract date: geoTwitter20-03-12
    m = re.search(r"geoTwitter(\d{2})-(\d{2})-(\d{2})", filename)
    if not m:
        continue

    yy, mm, dd = map(int, m.groups())
    date = datetime(2000 + yy, mm, dd)
    day_of_year = int(date.strftime("%j"))

    # load json
    with open(path) as f:
        data = json.load(f)

    # count hashtags
    for h in args.hashtags:
        if h in data:
            # data[h] is usually {lang: count}
            for v in data[h].values():
                counts[h][day_of_year] += v


# ---------- plotting ----------
days = sorted({d for h in counts for d in counts[h]})

plt.figure()
labels = {
    '#coronavirus': '#coronavirus (English)',
    '#코로나바이러스': '#coronavirus (Korean)',
    '#コロナウイルス': '#coronavirus (Japanese)',
    '#冠状病毒': '#coronavirus (Chinese)',
}
for h in args.hashtags:
    ys = [counts[h].get(d, 0) for d in days]
    plt.plot(days, ys, label=labels.get(h, h))

plt.xlabel("day of year")
plt.ylabel("number of tweets")
plt.legend()
plt.savefig(args.output_png)

