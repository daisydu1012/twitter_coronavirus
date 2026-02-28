import zipfile
import datetime
import json
import argparse
import unicodedata
from collections import Counter, defaultdict


parser = argparse.ArgumentParser()
parser.add_argument("--input_path", required=True)
args = parser.parse_args()

def normalize_text(s: str) -> str:
    """Normalize unicode to NFC so multilingual hashtags match correctly."""
    return unicodedata.normalize("NFC", s)

# load keywords
hashtags = [
    '#코로나바이러스',  # Korean
    '#コロナウイルス',  # Japanese
    '#冠状病毒',        # Chinese
    '#covid2019',
    '#covid-2019',
    '#covid19',
    '#covid-19',
    '#coronavirus',
    '#corona',
    '#virus',
    '#flu',
    '#sick',
    '#cough',
    '#sneeze',
    '#hospital',
    '#nurse',
    '#doctor',
]

# normalize hashtags once
hashtags = [normalize_text(h) for h in hashtags]

# initialize counters
counter_lang = defaultdict(Counter)
counter_country = defaultdict(Counter)

with zipfile.ZipFile(args.input_path) as archive:

    for filename in archive.namelist():
        print(datetime.datetime.now(), args.input_path, filename)

        with archive.open(filename) as f:
            for line in f:
                tweet = json.loads(line)

                # language (fallback to 'und' if missing)
                lang = tweet.get("lang") or "und"

                # country (fallback to 'UNK' if missing)
                country = "UNK"
                place = tweet.get("place")
                if isinstance(place, dict):
                    cc = place.get("country_code")
                    if cc:
                        country = cc

                # get full tweet text (avoid truncated tweets)
                text = (
                    tweet.get("extended_tweet", {}).get("full_text")
                    or tweet.get("full_text")
                    or tweet.get("text")
                    or ""
                )

                # normalize and lowercase for matching
                text = normalize_text(text).lower()

                # search hashtags
                for hashtag in hashtags:
                    if hashtag.lower() in text:
                        counter_lang[hashtag][lang] += 1
                        counter_country[hashtag][country] += 1
