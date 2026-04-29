# MatStat-Analytics

A comprehensive Python application for statistical analysis, data processing, and visualization with support for multidimensional datasets and advanced statistical testing.

## Overview

MatStat-Analytics is a full-featured statistical analysis tool built with PyQt that provides extensive capabilities for data analysis, hypothesis testing, parameter estimation, regression, and simulation. The application supports univariate, bivariate, and multivariate data analysis through an intuitive tabbed interface.

---

## Key Features

### 📂 Data Management & Processing
- **Multi-format Support**: Load data from `.txt`, `.csv`, `.xls`, `.xlsx` files
- **Multidimensional Data**: Full support for datasets with multiple columns/variables
- **Column Selection**: Choose specific columns for analysis operations
- **Data Versioning**: Track changes with rollback capabilities to original data
- **Export Data**: Export transformed or simulated data as CSV
- **Missing Data Handling**: Detection, imputation (mean, median, interpolation), and removal of incomplete records

### 🔧 Data Preprocessing
- **Anomaly Detection**: Identify and handle outliers using multiple criteria
- **Data Transformations**: Standardization (z-score), logarithmic transformations, custom shift operations
- **Quality Control**: Automated data validation and cleaning

---

### 📈 Statistical Analysis
- **Descriptive Statistics**: Mean, median, mode, standard deviation, variance, range, skewness, kurtosis, Pearson's variation coefficient, quantiles and percentiles
- **Confidence Intervals**: Customizable significance levels for all estimated parameters
- **Parameter Estimation**:
  - Maximum Likelihood Estimation (MLE)
  - Method of Moments
  - Supported distributions: Normal, Exponential, Laplace, Weibull, Uniform

### 🧪 Goodness-of-Fit Tests
- **Pearson's Chi-Square Test**: Univariate distribution compliance
- **Kolmogorov-Smirnov Test**: Enhanced KS implementation
- **Pearson's Chi-Square Test for 2D Normal**: Tests bivariate data for normality
- All tests report the test statistic, critical value, and a plaintext conclusion

---

### 🎲 Simulation & Modelling
- **Sample Generation**: Simulate datasets of arbitrary size using the inverse transform method for Normal, Exponential, Weibull, Uniform, and Laplace distributions; supports multivariate generation
- **T-test Experiment**: Automated experiment schema — simulate samples of sizes 20 / 50 / 100 / 400 / 1000 / 2000 / 5000, fit the model, compare estimated parameters against true values via T-test, repeat 200–500 times per sample size, and summarise mean T-statistic and its standard deviation in a consolidated table
- **Export**: Save simulation results as CSV

---

### 🔬 Homogeneity Tests

#### One-Sample
- Abbe Test (independence of observations)

#### Two-Sample (independent & dependent)
- Mann-Whitney U Test
- Normal Homogeneity Test (equal means & variances for normal samples)
- Rank Mean Difference Test
- Sign Criterion Test
- Smirnov-Kolmogorov Test
- Wilcoxon Signed-Rank Test

#### N-Sample
- ANOVA (one-way analysis of variance)
- Bartlett's Test for equal variances
- Cochran's Q Test
- Kruskal-Wallis H Test
- Multivariate Normal Homogeneity Test (equality of mean vectors and covariance matrices)

---

### 🔗 Correlation & Regression Analysis

#### Correlation
- Pearson, Spearman, Kendall correlation coefficients with significance testing and confidence intervals
- Correlation Ratio with significance testing
- Multiple and partial correlation coefficients

#### 📉 Regression
- **Models**: Simple Linear Regression, Polynomial Regression (degree 2 & 3) — all fitted via OLS
- **Summary**: Coefficients, intercept, confidence intervals for all parameters, per-coefficient and overall F-significance, R², Adjusted R², MSE, RSE, regression equation as text
- **Diagnostics**: Residuals-vs-fitted plot, tolerance bounds for residual variance
- **Prediction**: Point prediction, confidence interval for the mean response, prediction interval for an individual observation

---

### 📊 Multivariate Analysis
- **Primary Analysis**: Mean vector, standard deviation vector, matrix of significant pairwise correlation coefficients
- **Multiple & Partial Correlation**: Coefficient estimation, significance testing, confidence intervals for partial coefficients
- **Multivariate Linear Regression**: Standardised and unstandardised coefficient estimates, significance and precision analysis, R², tolerance bounds for residual variance, regression line confidence intervals, F-test for overall model significance, residuals-vs-fitted diagnostic diagram

---
### 🧩 Component Analysis

* **Principal Component Analysis**: Implements dimensionality reduction by transforming correlated variables into a set of linearly uncorrelated principal components.
* **Scree Plot**: Visualizes the eigenvalue for each principal component to help identify the "elbow" point where adding more components provides diminishing returns in explained variance.
* **Principal Components Selection**: Supports two automated modes for selection:
    * **Fixed Count**: Manually specify the exact number of components ($n$) to retain.
    * **Variance Threshold**: Automatically selects the minimum number of components required to meet a target percentage (e.g., 90%) of total explained variance.
* **Inverse Transformation**: Allows for data reconstruction from the reduced feature space back to the original coordinate system for verification and analysis.
* **Dynamic Visualization**: Integrated status reporting and real-time calculation of explained variance ratios for each component.

### 📉 Visualization

#### Univariate
| Plot | Details |
|---|---|
| Histogram | Auto & manual bin selection; frequency polygon overlay; density overlay |
| EDF | Empirical distribution function with theoretical overlay and confidence bands |
| H-H Plot | Empirical vs theoretical quantile diagnostic |
| Distribution Plot | Theoretical PDF/CDF with confidence intervals |

#### Bivariate
| Plot | Details |
|---|---|
| Correlation Field | Scatter with Pearson r displayed; optional OLS regression line |
| 3D Histogram Map | Heatmap projection of joint frequency for two variables |

#### Three-Variable
| Plot | Details |
|---|---|
| Bubble Plot | Third variable encoded as bubble size |

#### Multivariate
| Plot | Details |
|---|---|
| Scatter Matrix | Pairwise scatter plots with histogram diagonal |
| Parallel Coordinates | All variables on parallel axes; one line per observation |
| Correlation Matrix | Heatmap of pairwise correlation coefficients (Pearson / Spearman / Kendall / Ratio) |
| Heatmap | General-purpose variable heatmap |

---

## Technical Architecture

### Design Patterns
- **MVC Architecture**: Clean separation of Models, Views, and Controllers
- **Strategy Pattern**: Pluggable algorithms for statistical tests and estimators
- **Factory Pattern**: Dynamic creation of test objects and estimators
- **Observer Pattern**: UI state management and real-time updates
- **Event Bus**: Centralized publish-subscribe system for decoupled component communication
- **Registry Pattern**: Centralized registry for distributions, tests, and renderers

### Core Components
- **Models**: Statistical distributions, test implementations, regression models, data structures
- **Controllers**: Business logic for analysis, data processing, and UI coordination
- **Services**: Reusable components for data loading, transformation, and rendering
- **Views**: PyQt-based UI components organised in tabs and widgets
- **Utils**: App context, event bus, decorators, UI styles, helper functions

---

## Installation

```bash
git clone https://github.com/deyme17/MatStat-Analytics.git
cd MatStat-Analytics
pip install -r requirements.txt
python main.py
```

---

## Project Structure

```
MatStat-Analytics/
├── controllers/
│   ├── analysis_controllers/     # Correlation, estimation, GOF, homogeneity, regression, simulation, statistics
│   ├── data_controllers/         # Data loading and dataset selection
│   └── dp_controllers/           # Anomaly detection, transformation, missing data, pca
├── models/
│   ├── correlation_coeffs/       # Pearson, Spearman, Kendall, Ratio, Multiple, Partial
│   ├── data_processors/          # Anomaly, missing, transformation processors
│   ├── gofs/                     # Chi-square, KS, 2D normal chi-square tests
│   ├── homogens/                 # One-, two-, and N-sample homogeneity tests
│   ├── params_estimators/        # MLE, Method of Moments
│   ├── regression/               # OLS algorithm; Linear and Polynomial models
│   ├── stat_distributions/       # Normal, Exponential, Laplace, Weibull, Uniform
│   ├── data_model.py
│   ├── simulation_engine.py
│   └── statistics_calculator.py
├── services/           
│   ├── data_services/            # Loader strategies, versioning, export
│   ├── stat_services/            # Confidence assessment, regression service, test performer
│   └── ui_services/              # Table renderers, graph renderers, messenger
├── views/
│   ├── tabs/                     # All main application tabs
│   │   └── graph_tabs/           # Graph tabs grouped by dimensionality
│   └── widgets/                  # Specialised panels and dialogs
└── utils/                        # AppContext, EventBus, helpers, decorators, UI styles
```
