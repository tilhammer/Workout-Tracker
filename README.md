# Workout Tracker

## Introduction

This program is a simple python tool to help me get rid of the hustle around tracking my training sessions. You can easily enter information through the CLI (Command Line Interface) and it will be saved in a TinyDB database ready for analysis.

Once you tracked your exercise, you can create a detailed analysis to understand your own habits better*.

None of your data will be shared and there is no internet connection required for usage, it is how ever neccessary during the installation process.

*Future feature, see [Roadmap](#roadmap)

## Installation and Running (Only tested on Linux)

### Prerequisites

- git installed and working

- python (only tested with 3.12 and 3.13) >= 3.12, <=4.0 installed and working ([conda](https://github.com/conda-forge/miniforge?tab=readme-ov-file#install) recommended)

- pip installed and working

### Method A: Poetry (Recommended)

Install [poetry](https://python-poetry.org/docs/#installation) via pip (recommended to do so in a conda environment for cleaner Python version management):

```bash
pip install poetry
```

Clone the project to a destination of your liking:

```bash
git clone https://github.com/tilhammer/Workout-Tracker.git
```

Now, switch into the directory and install the dependencies it with poetry:

```bash
cd Workout-Tracker
poetry install
```

To run, type:

```bash
poetry run python workout-tracker.py
```

### Method B: Without poetry

Clone the project to a destination of your liking:

```bash
git clone https://github.com/tilhammer/Workout-Tracker.git
```

Now, switch into the directory and install the requirements. It is recommended to use conda or a similar python installation manager:

```bash
cd Workout-Tracker
pip install requirements.txt
```

To run, type:

```bash
python workout-tracker.py
```

If the installation or running fails, check `python --version` and `pip --version`. You might have `python3` and `pip3` installed, especially under Linux. In that case substitute all `python` and `pip` commands with`python3` and `pip3`.

If this still doesn't work using Method B, please check if the `requirements.txt` file located at the head of the project is up to date with the `project.dependencies` in the `pyproject.toml` file. I have to manually generate the `requirements.txt` file, so there could be mistakes. Contact me in that case or open an issue please and try using Option A to ensure the poetry install works.

It is further recommended to create a simple script for running the project, especially if you use conda and have a nested home directory structure.

## Roadmap

### Definitely coming

- [x] Creating tracking functionality with the CLI
- [ ] Commenting code for easier understanding and improvement
- [ ] Adding basic analysing functionality with CLI
- [ ] Adding export functionality for statistics and diagrams
- [ ] Adding functionality to analyse specific timeframes

### Depending on my mood and the community

- [ ] Adding custom diagrams
- [ ] Adding comparison of different timeframes and exercise-categories
- [ ] Adding custom types of exercise

## Help

If you need help with the installation, feel free to reach out to me or create a GitHub issue. Check if there have been similar issues that were already closed.

You are always allowed to edit the code and make changes to the program. If you would like to contribute to the project, either create a fork or contact me.

Feature suggestions are always welcome, but there is no guarantee for implementation as I might be busy. You are always free to implement them by yourself.
