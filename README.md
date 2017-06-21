Good Sci-Fi
==============================

A deep learning classification model(s) of science fiction content (movies, tv shows and books) via their marketing posters and covers.

Learn more here:

Project Organization
------------
<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    |   |   └── webcrawler <- Scrapy spiders for extracting data via web crawl
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org

Source Data
------------
(TODO)

Movies & TV Shows
- The Movie Database
  - Sci-fi Movies and TV Shows ("all")
- IMDB
  - Most Voted Sci-Fi TV Shows (1000)
  - Most popular Sci-Fi TV Shows (1000)
  - Top US Grossing SCi-Fi Feature Films (1000)
  - Most Voted Sci-Fi Feature Films (1000)
  - Most Popular Sci-Fi Feature Films (1000)
- On DVD Releases
  - Overall Ratings (2009-2017, 160)
  - Theatrical Gross (2009-2017, 160)
- Ranker
  - Greatest Sci-Fi of All Time (100)
- RottenTomatoes
  - Top 100 Sci-Fi & Fantasy with 40 more critic reviews (100)
- sffjazz
  - Top 100 Sci-Fi Films (100)
  - Top 100 Sci-Fi TV Shows (100)
- IGN
  - Top 100 Sci-Fi Movies (100)
- Cult Classics lists?
- Worst ever lists?
- Most popular on TMDB?

Books
- World Without End
  - Sci-Fi Books ("all")
  - The Classics of Science Fiction (139)
  - SF Masterworks (160)
  - SF Mistressworks (90)
  - Guardian: The Best Science Fiction & Fantasy Novels (-2009, 149)
  - NPR: Top 100 Science Fiction & Fantasy Books (-2011, 100)
  - David Pringle's Science Fiction (100)
  - Science Fiction: The 101 Best Novels (1985-2010, 101)
  - Locus Best SF Novels of All Time (-1990, 53)
  - Easton Press Masterpieces of Science Fiction (139)
  - 200 Significant SF Books by Women (1984-2001, 200)
- ISFDB
  - Highest Ranked Novels of All Time, by Awards & Nominations (500)
- GoodReads
  - Best Science Fiction of the 21st Century (2000-2017, 500)
  - Best Science Fiction (500)
  - Most Popular Science Fiction on GoodReads (100)

**Labelled Data Summary:**

| | Movies | TV Shows | Books|
|---|---|---|---|
|**Classic** |0|0|0|
|**Good** |0|0|0|
|**Bad** |0|0|0|

Install
------------
