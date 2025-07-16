# Exploring Probabilistic Variable Dependencies

[cite_start]This project is a data science research initiative to explore the intersection of data science and probability through software development. [cite: 3] [cite_start]The core aim is to design and build a **scalable tool that identifies and visualizes probabilistic dependencies** between features in large datasets. [cite: 5] [cite_start]This work seeks to bridge the gap between probabilistic modeling and applied data engineering by implementing scalable algorithms for large-scale data analysis. [cite: 6]

***

## Features

* [cite_start]**Dependency Detection**: Implements probabilistic techniques like Bayesian networks to uncover complex, non-linear dependencies between variables. [cite: 10, 52]
* **Extensible Design**: Built with a clean, Object-Oriented structure that allows for new detection methods to be easily added.
* [cite_start]**Synthetic Data Generation**: Includes a configurable script to pragmatically generate datasets with controlled dependency structures for robust testing. [cite: 19, 20]

***

## Getting Started

Follow these instructions to set up the project environment and run the dependency detector.

### **Prerequisites**

* Python 3.8+
* `pip` and `venv`

### **Installation**

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-project-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the package and its dependencies:**
    This command installs the project in "editable" mode (`-e`), which means any changes you make to the source code will be available immediately without reinstalling.
    ```bash
    pip install -e .
    ```

***

## Usage

The workflow involves generating data based on a configuration and then analyzing it with the detector.

### **1. Generate Synthetic Data**

The project uses a `config.json` file to define variables and their relationships. [cite: 3] You can generate a dataset based on this configuration using the provided script.

```bash
python scripts/generate_data.py --config synthetic_data_generation/config.json --n_samples 10000 --out_path data/synthetic_data.parquet