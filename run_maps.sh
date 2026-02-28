#!/bin/bash
set -e

OUTDIR="outputs"
mkdir -p "$OUTDIR"

for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
  base="$(basename "$file")"
  nohup python3 src/map.py --input_path "$file" --output_folder "$OUTDIR" > "nohup_${base}.log" 2>&1 &
done
