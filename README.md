# Understanding Video Game Reception: A Metacritic Data Analysis

A dive into the depths of video game reviews on Metacritic in an attempt to identify what makes a game successful in the eyes of the audience and what drives the divide between user reception and critic scores.

## Goals & Data

#### Goals

1. The main goal here is to try and identify how meta information about a game that is available around launch may affect user reception of that game.
2. Identify factors that may contribute to a discrepancy between critic scores and user reception
3. Has the reception of games changed over time and are there game archetypes based on their meta data and reception?
4. What determines player engagement?

**Potential Use-Cases**

- Additional information for marketing-related decisions
- ...
 
#### Data

The basis for this project is a publicly available data set that is the result of a web scrape from meta critic. You can check the kaggle data source [here](https://www.kaggle.com/datasets/zaireali/metacritic-games-scrape/data).

**Data Structure**  
The main information present in the data.

| Variable | Description |
| -------- | ----------- |
| title | Full title of the game |
| genres/0 | The first genre tag as found on metacritic |
| metascore | The aggregated critic rating of the game |
| publisherName | Name of the publisher |
| publisherUrl | web page of the publisher on metacritic |
| releaseDate | Release Date of the first system installment of the game |
| section | Console on which the game was published first |
| summary | game summary as found on the metacritic game page |
| url | link to game page on meta critic |
| userscore | aggregated user score of the game |

There are ~300 more columns in the data that are a flattened representation of positive, negative, and mixed user review counts grouped by console. This information needs to be extracted and made available for use as additional features.

**Planned methods/steps**

- Extensive EDA of original meta critic data set
- Data aggregation: Extraction and integration of console-dependent user review counts for later use
- *Feature Engineering*
    - Cyclical information of release date variable
    - Attempt at Web Scrape I: get console-dependent critic review counts
    - Attempt at Web Scrape II: get additional genre tags from game site
    - Gather number of sales or total revenue or similar business information from additional data sources or web scrape
- *ML*
    - Prediction of critic - user gap (Regression, RF, HistGradBoost, XGBoost, ...)
    - Identification of game types (PCA, k-Means, DBSCAN, ...)
- Nice visualizations

**Secondary Data Sources**

[Information about potential other data sources here]

## Installation & Use

For this project you will need Python and uv virtual environment manager installed on your machine. 

## Project Structure

```text
StackFuel_PP/
├── .venv/
├── .vscode/
├── data/
|   ├── processed/
|   └── raw/
├── docs/
├── figures/
├── models/
├── notebooks/
├── README_files/
├── src/
├── .gitignore
├── python-version
├── pyproject.toml
├── README.html
├── README.md
└── uv.lock
```

- `.venv/`: virtual environment files for the project


## Setup

Klone das Repository
```bash
# Repository klonen
git clone [DEIN-REPO-LINK]
cd [REPO-NAME]
```

Installiere [uv](https://uv.dev) (falls noch nicht installiert) und synchronisiere die Abhängigkeiten
```bash
# Dependencies installieren
uv sync
```

### Ausführung

Notebooks in dieser Reihenfolge ausführen:
1. notebooks/01_exploration.ipynb
<!--
2. notebooks/02_preprocessing.ipynb
3. notebooks/03_modeling.ipynb
4. notebooks/04_results.ipynb
-->


