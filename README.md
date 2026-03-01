# Twitter Hashtag Analysis with MapReduce (2020 Geotagged Dataset)

## Overview
This project analyzes 1.1 billion geotagged tweets from 2020 using a custom MapReduce pipeline written in Python and executed in parallel on a Linux compute server.
The goal is to measure how selected hashtags (e.g., `#coronavirus`, `#코로나바이러스`) vary across countries, languages, and time.
Each day of tweets is processed independently in the map phase and then aggregated into global results in the reduce phase, enabling scalable large-scale data analysis.

---

## Tech Stack
- Python  
- Bash (nohup, background jobs, process control)  
- MapReduce workflow  
- Matplotlib  
- Linux server environment  

---

## Dataset
Location:

/data/Twitter dataset/


- ~1.1 billion geotagged tweets  
- One compressed file per day  
- Each file contains 24 hourly JSON streams  

The dataset is too large to process locally, so all computation was executed in parallel on the lambda server.

---

## MapReduce Pipeline

### Map Phase
For each day:

```
python src/map.py --input_path <zip_file> --output_folder outputs/
```

This step extracts hashtag counts by:

language → .lang files

country → .country files

All jobs were launched in parallel using:

```
nohup ./run_maps.sh &
```

### Reduce Phase

All daily outputs are combined into global totals:
```
python src/reduce.py --input_path outputs/ --output_file reduce.lang
python src/reduce.py --input_path outputs/ --output_file reduce.country
Visualization
```

Bar charts of the top 10 countries and languages for each hashtag are generated with:

```
python src/visualize.py --input_path <file> --key <hashtag>
```

### Alternative Reduce (Time Series)
A second reduce pipeline generates time-series plots showing daily hashtag usage over the year.
x-axis: day of the year
y-axis: number of tweets
one line per hashtag


### Key Features

Parallel processing over hundreds of daily files
Streaming JSON directly from compressed archives
Fault-tolerant execution using nohup and background jobs
Global aggregation via a custom reduce step
Automated visualization of large-scale results


### Outputs

The project produces:

Language distribution plots

Country distribution plots

Time-series hashtag trends

### Results:
## Top Hashtag Usage by Language and Country

<table>
  <tr>
    <td align="center"><b>Languages – #coronavirus</b></td>
    <td align="center"><b>Countries – #coronavirus</b></td>
  </tr>
  <tr>
    <td><img src="img/all.lang.coronavirus.png" width="400"></td>
    <td><img src="img/all.country.coronavirus.png" width="400"></td>
  </tr>
  <tr>
    <td align="center"><b>Languages – Korean term</b></td>
    <td align="center"><b>Countries – Korean term</b></td>
  </tr>
  <tr>
    <td><img src="img/all.lang.korean.png" width="400"></td>
    <td><img src="img/all.country.korean.png" width="400"></td>
  </tr>
</table>

## Hashtag Usage Over Time (Task 4)

![Hashtag trends over time](img/task4_languages.png)
