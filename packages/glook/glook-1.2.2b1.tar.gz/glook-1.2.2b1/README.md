
![G-Look](https://github.com/gaurang157/glook/blob/main/assets/G-Look-Auto-EDA-Ml%20(10).png?raw=true)
---

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/pypi/l/glook?style=flat-square"/></a>
  <a href="https://pypi.org/project/glook/"><img src="https://img.shields.io/pypi/pyversions/glook?style=flat-square"/></a>
  <a href="https://pypistats.org/packages/glook"><img src="https://img.shields.io/pypi/dm/glook?style=flat-square" alt="downloads"/></a>
</p>

## Releases

<div align="center">
  <table>
    <tr>
      <th>Repo</th>
      <th>Version</th>
      <th>Downloads</th>
    </tr>
    <tr>
      <td>PyPI</td>
      <td><a href="https://pypi.org/project/glook/"><img src="https://img.shields.io/pypi/v/glook?style=flat-square"/></a></td>
      <td><a href="https://pepy.tech/project/glook"><img src="https://pepy.tech/badge/glook"/></a></td>
    </tr>
  </table>
</div>

# G-Look: Auto EDA

Glook is an automated Python library that provides a graphical user interface (GUI) for supervised and unsupervised learning. It encompasses everything from data collection to Auto-EDA, preprocessing, data splitting, multiple model training for comparison, custom model training, and deployment demonstrations. With Glook, you can easily manage and streamline your entire machine learning workflow in one comprehensive library.

## ⚠️ **BEFORE INSTALLATION** ⚠️

**Before installing glook, it's strongly recommended to create a new Python environment to avoid potential conflicts with your current environment.**


## Creating a New Conda Environment

To create a new conda environment, follow these steps:

1. **Install Conda**:
   If you don't have conda installed, you can download and install it from the [Anaconda website](https://www.anaconda.com/products/distribution).

2. **Open a Anaconda Prompt**:
   Open a Anaconda Prompt (or Anaconda Terminal) on your system.

3. **Create a New Environment**:
   To create a new conda environment, use the following command. Replace `my_env_name` with your desired environment name.
- Support Python versions are > 3.8
```bash
conda create --name my_env_name python=3.8
```

4. **Activate the Environment**:
    After creating the environment, activate it with the following command:
```bash
conda activate my_env_name
```

## OR
## Create a New Virtual Environment with `venv`
If you prefer using Python's built-in `venv` module, here's how to create a virtual environment:

1. **Check Your Python Installation**:
   Ensure you have Python installed on your system. You can check by running:
   - Support Python versions are > 3.8
```bash
python --version
```

2. **Create a Virtual Environment**:
Use the following command to create a new virtual environment. Replace `my_env_name` with your desired environment name.
```bash
python -m venv my_env_name
```

3. **Activate the Environment**:
After creating the virtual environment, activate it using the appropriate command for your operating system:
```bash
my_env_name\Scripts\activate
```

## Installation

You can install glook using pip:

```bash
pip install glook
```

## Usage

Once installed, you can open Glook Auto-EDA for analysis with the global CLI command `glook`:

```bash
glook
```

The G-Look Auto EDA application GUI will launch, allowing you to perform Auto EDA on your dataset interactively.

<img width="960" alt="image" src="https://github.com/gaurang157/glook/assets/148379526/668aaa96-5883-49eb-aa85-4852df92233a">

You can also open Glook Auto-ML using the global CLI command  `glookml`:

```bash
glookml
```

The G-Look Auto ML application GUI will launch, allowing you to perform Auto ML on your dataset interactively.


<img width="960" alt="image" src="https://github.com/gaurang157/glook/blob/main/assets/Screenshot%20(5124).png?raw=true">


## Features

- General Data Insights
<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/general_data_insights.png?raw=true" alt="General Data Insights">
  <figcaption>General Data Insights (in <code>glook</code> & <code>glookml</code>)</figcaption>
</figure>
      

### Univariate Analysis
- Visualize distributions of individual columns using:
  - Histograms
  - Box plots
  - Q-Q plot
- Statistical Calculations:

<figure>
  <img src="https://github.com/gaurang157/glook/assets/148379526/4d9bb69b-c0f5-4e57-8a42-6de58af9a5e0" alt="Statistical Calculations">
  <figcaption>Statistical Calculations (in <code>glook</code> & <code>glookml</code>)</figcaption>
</figure>

### Bivariate Analysis
<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/bivariate_analysis.png?raw=true" alt="Trivariate Analysis">
  <figcaption>Trivariate Analysis (in <code>glook</code> & <code>glookml</code>)</figcaption>
</figure>

- Explore relationships between two columns using:
  - Scatter plots
  - Line plots
  - Bar plots
  - Histograms
  - Box plots
  - Violin plots
  - Strip charts
  - Density contours
  - Density heatmaps
  - **Polar plots**
    - **Polar Scatter Plot:** Visualize the relationship between two columns in polar coordinates.
    - **Polar Line Plot:** Show the relationship between two columns as lines in polar coordinates.
    - **Polar Bar Plot:** Display the relationship between two columns as bars in polar coordinates.
- Select x-axis and y-axis columns to visualize their relationship.

#### Trivariate Analysis

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/Screenshot%20(5125).png?raw=true" alt="Bivariate Analysis">
  <figcaption>Bivariate Analysis (in <code>glook</code> & <code>glookml</code>)</figcaption>
</figure>

- Analyze relationships between three columns using:
  - 3D Scatter plots
  - Ternary Scatter plots
  - Contour plots
  - Surface plots
  - Parallel coordinate plots
- Select three columns to visualize their trivariate relationship.

#### Pre-Processing

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/pre_processing(5126).png?raw=true" alt="Pre-Processing">
  <figcaption>Pre-Processing (in <code>glookml</code>)</figcaption>
</figure>

#### Data Split

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/data_split.png?raw=true" alt="Data Split">
  <figcaption>Data Split (in <code>glookml</code>)</figcaption>
</figure>

#### Supervised Multi Model Building for Comparison

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/MB_SL.png?raw=true" alt="Supervised Model Building">
  <figcaption>Supervised Multi Model Building for Comparison (in <code>glookml</code>)</figcaption>
</figure>

#### Supervised Multi Model Comparison Charts

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/MB_SL_Metrics.png?raw=true" alt="Supervised Model Building">
  <figcaption>Supervised Multi Model Comparison Charts (in <code>glookml</code>)</figcaption>
</figure>

#### Un-supervised Multi Model Building for Comparison

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/UL_MD_.png?raw=true">
  <figcaption>Un-supervised Multi Model Building for Comparison (in <code>glookml</code>)</figcaption>
</figure>

#### Un-supervised Multi Model Comparison Charts

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/UL_MD_Metrics_Charts.png?raw=true" alt="Supervised Model Building">
  <figcaption>Un-supervised Multi Model Comparison Charts (in <code>glookml</code>)</figcaption>
</figure>

#### Custom Model Building

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/Custom_Model_Training.png?raw=true" alt="Custom Model Building">
  <figcaption>Custom Model Building (in <code>glookml</code>)</figcaption>
</figure>

#### Deployment Demo 

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/Deployment_Demo.png?raw=true" alt="Deployment Demo">
  <figcaption>Deployment Demo (in <code>glookml</code>)</figcaption>
</figure>

#### Supervised Model Building Predictions

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/Predictions.png?raw=true" alt="Predictions">
  <figcaption>Supervised Model Building Predictions (in <code>glookml</code>)</figcaption>
</figure>

#### Un-supervised Model Building Predictions

<figure>
  <img src="https://github.com/gaurang157/glook/blob/main/assets/UL_Predictions.png?raw=true" alt=" Un-supervised Model Building Predictions">
  <figcaption> Un-supervised Model Building Predictions (in <code>glookml</code>)</figcaption>
</figure>



### Supported Formats

glook supports various data formats, including CSV & Excel.

## Getting Help

If you encounter any issues or have questions about using glook, please feel free to open an issue on the [GitHub repository](https://github.com/gaurang157/glook/). We'll be happy to assist you.

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit) file for details.
