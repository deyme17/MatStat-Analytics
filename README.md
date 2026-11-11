# MatStat-Analytics

A comprehensive Python application for statistical analysis, data processing, and visualization with support for multidimensional datasets, component and factor analysis, and advanced statistical testing.

## Overview

MatStat-Analytics is a full-featured statistical analysis tool built with PyQt that provides extensive capabilities for data analysis, hypothesis testing, parameter estimation, regression, dimensionality reduction, factor analysis, and simulation. The application supports univariate, bivariate, and multivariate data analysis through an intuitive tabbed interface.

---

## Key Features

### 📂 Data Management & Processing
- **Multi-format Support**: Load data from `.txt`, `.csv`, `.xls`, `.xlsx`, `.DAT` files
- **Multidimensional Data**: Full support for datasets with multiple columns/variables
- **Column Selection**: Choose specific columns for analysis operations
- **Data Versioning**: Track changes with rollback capabilities to original data
- **Export Data**: Export transformed or simulated data as CSV
- **Missing Data Handling**: Detection, imputation (mean, median, interpolation), and removal of incomplete records

### 🔧 Data Preprocessing
- **Anomaly Detection**: Identify and handle outliers using multiple criteria (3-Sigma, Asymmetry Filter, Confidence Interval γ)
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

### 🧩 Component Analysis (PCA)

* **Principal Component Analysis**: Implements dimensionality reduction by transforming correlated variables into a set of linearly uncorrelated principal components.
* **Scree Plot**: Visualizes eigenvalues for each principal component to identify the "elbow" point where adding more components provides diminishing returns.
* **Component Loadings Matrix**: Displays loadings that quantify the relationship between original variables and principal components.
* **Feature Selection**: Flexible feature selector list to choose input variables for PCA.
* **Selection Modes**:
    * **Fixed Count**: Manually specify the exact number of components ($n$) to retain.
    * **Variance Threshold**: Automatically select the minimum number of components required to satisfy a target percentage (e.g., 90%) of explained variance.
* **Inverse Transformation**: Data reconstruction from reduced feature space back to the original coordinate space.

---

### 📉 Factor Analysis (PFM)

* **Principal Factor Method (PFM)**: Extracts underlying latent factors from correlated variables using iterative principal factor estimation.
* **Initial Communality Estimators ($h^2$)**: Supports multiple methods for initial communality estimation:
    * PCA-based Initial Estimator
    * Maximum Absolute Correlation Method
    * Triads Method
    * Centroid Method
    * Averoid Method
    * Averaging Method
* **Factor Loadings Matrix & Iteration Tracking**: Computes the final factor loading matrix, specific variances, total communalities, and tracks convergence details over iterations.
* **Interactive Clearing & Status Reports**: Real-time convergence status display and result clearing.

---

### 📊 Visualization

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
| Correlation Field 3D | Third variable scatter plot |

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
- **Strategy Pattern**: Pluggable algorithms for statistical tests, estimators, and communality methods
- **Factory Pattern**: Dynamic creation of UI tabs, controllers, connections, test objects, and estimators
- **Observer Pattern**: UI state management and real-time updates via Event Bus
- **Event Bus**: Centralized publish-subscribe system for decoupled component communication
- **Registry Pattern**: Centralized distribution register and renderers

---

## Installation

```bash
git clone [https://github.com/deyme17/MatStat-Analytics.git](https://github.com/deyme17/MatStat-Analytics.git)
cd MatStat-Analytics
pip install -r requirements.txt
python main.py
```

## Project Structure

```
MatStat-Analytics/
├── controllers/
│   ├── analysis_controllers/ # Component, correlation, estimation, factor, GoF, homogen, regression, simulation, statistics
│   ├── data_controllers/     # Data loader and dataset selection controllers
│   └── dp_controllers/       # Anomaly, data transform, missing controllers
├── factories/                # ConnectFactory, ControllersFactory, UIFactory
├── models/
│   ├── component_analysis/   # PCA model implementation
│   ├── correlation_coeffs/   # Pearson, Spearman, Kendall, Ratio, Multiple, Partial
│   ├── data_processors/      # Anomaly, missing, transformation processors
│   ├── factor_analysis/      # PFM implementation and communality estimators (MaxCorr, Triads, Centroid, etc.)
│   ├── gofs/                 # Chi-square, KS, 2D normal chi-square tests
│   ├── homogens/             # One-, two-, and N-sample homogeneity tests
│   ├── params_estimators/    # MLE, Method of Moments
│   ├── regression/           # OLS algorithm; Linear and Polynomial models
│   ├── stat_distributions/   # Normal, Exponential, Laplace, Weibull, Uniform
│   └── statistics/           # Statistics calculator
├── services/           
│   ├── data_services/        # Loader strategies, versioning, saver, exporter
│   ├── stat_services/        # Confidence assessment, simple linear regression, test performer
│   └── ui_services/          # Table renderers, graph renderers, messenger
├── views/
│   ├── tabs/                 # Main analysis tabs (Component, Factor, Correlation, Regression, Homogen, etc.)
│   │   └── graph_tabs/       # Graph visualization tabs (Univariate, Bivariate, Trivariate, Multivariate)
│   └── widgets/              # Specialized UI widgets (componentwidgets, factorwidgets, corrwidgets, etc.)
├── utils/                    # AppContext, EventBus, callbacks, decorators, helpers, ui_styles
├── factory.py                # Main Application Factory
└── main.py                   # Application Entry Point
```