# MatStat-Analytics

A comprehensive Python application for statistical analysis, data processing, and visualization with support for multidimensional datasets and advanced statistical testing.

## Overview

MatStat-Analytics is a full-featured statistical analysis tool built with PyQt that provides extensive capabilities for data analysis, hypothesis testing, parameter estimation, and simulation. The application supports both univariate and multivariate data analysis with an intuitive tabbed interface.

## Key Features

### 📊 **Data Management & Processing**
- **Multi-format Support**: Load data from `.txt`, `.csv`, `.xls`, `.xlsx` files
- **Multidimensional Data**: Full support for datasets with multiple columns/variables
- **Column Selection**: Choose specific columns for analysis operations
- **Data Versioning**: Track changes with rollback capabilities to original
- **Export Data**: Possibility to export transformed data
- **Missing Data Handling**: 
  - Detection of missing values
  - Imputation methods (mean, median, interpolation)
  - Option to remove incomplete records

### 🔧 **Data Preprocessing**
- **Anomaly Detection**: Identify and handle outliers using multiple criteria
- **Data Transformations**: 
  - Standardization (z-score normalization)
  - Logarithmic transformations
  - Custom shift operations
- **Quality Control**: Automated data validation and cleaning

### 📈 **Statistical Analysis**
- **Descriptive Statistics**: Complete statistical summaries including:
  - Central tendencies (mean, median, mode)
  - Variability measures (standard deviation, variance, range)
  - Distribution shape (skewness, kurtosis)
  - Quantiles and percentiles
- **Confidence Intervals**: Customizable precision levels for parameter estimation
- **Parameter Estimation**: 
  - Maximum Likelihood Estimation (MLE)
  - Method of Moments
  - Support for multiple distribution families

### 🧪 **Statistical Testing**

#### **Goodness-of-Fit Tests**
- **Pearson's Chi-Square Test**: Test for distribution compliance
- **Kolmogorov-Smirnov Test**: Enhanced KS test implementation
- **Distribution Fitting**: Test against Normal, Exponential, Laplace, Weibull, Uniform distributions
- **Pearson's Chi-Square Test for 2D data**: Implementation of the KS test, which tests 2D data for normal distribution.

#### **Homogeneity Tests**
- **One Sample Tests**:
  - Abbe Test for randomness
- **Two Sample Tests**:
  - Mann-Whitney U Test
  - Normal Homogeneity Test
  - Rank Mean Difference Test
  - Sign Criterion Test
  - Smirnov-Kolmogorov Test
  - Wilcoxon Signed-Rank Test
- **N-Sample Tests**:
  - ANOVA (Analysis of Variance)
  - Bartlett's Test for equal variances
  - Cochran's Q Test
  - Kruskal-Wallis H Test

### **Correlarion Analysis**
  - Multiple correlation methods supported (Pearson, Spearman, Kendall, Correlation Ratio)
  - Testing result displayed alongside confidence intervals for selected correlation metrics

### **Regression Analysis**
  - Configuration
    - Regression model selection (e.g. Linear Regression with OLS)
    - Dependent variables selection: `y` (target array)
    - Independent variable selection: `X` (feature matrix)
    - Fit a model: `fit(X, y)` method trains the model
  - Summary
    - `coefficients`: learned weights for each feature
    - `intercept`: bias term
    - `confidence intervals` confidence intervals for coefficients and intercept
    - `sagnificance testing` Test each coefficient, intercept and model at all on sagnificance
    - `metrics` Calculate metrics for evaluate the trained model (e.g. R^2, Adjusted R^2, MSE, RSE)
  - Prediction
    - `predict(X)` returns predicted values for new data
    - `Confident interval for mean` Claculate confident interval for mean value
    - `Prediction interval` Claculate prediction interval for an individual observation (X)

### 🎲 **Simulation & Modeling**
- **Sample Simulation**: Generate synthetic datasets from theoretical distributions (could be multivariate)
- **Export Capabilities**: Save simulation results as CSV files

### 📊 **Advanced Visualization**

#### **Graphs**
- **Histograms**: 
  - Automatic and manual bin selection
  - Frequency polygons (via checkbox)
  - Density overlays
- **Distribution Plots**:
  - Empirical Distribution Functions (EDF)
  - Theoretical distribution overlays
  - Cumulative frequency curves (ogives) with checkbox control
  - Comparative Analysis: Side-by-side empirical vs theoretical comparisons
- **H-H plot**:
  - Quantile–quantile style diagnostic comparing empirical and theoretical quantiles
  - Visual check for goodness of fit and distribution symmetry
- **3D Histogram as 2D map**:
  - Heatmap-based projection of 3D histograms for two numeric variables
  - Color intensity represents relative joint frequency
- **Correlation field**:
  - Scatter visualization of two variables with color-coded density
  - Real-time Pearson correlation coefficient displayed on the plot
  - Optional plotting regression line, calculated using Simple Linear Regression (OLS based)
- **Correlation Matrix**:
  - Heatmap representation of variable interdependencies
  - Multiple correlation methods supported (Pearson, Spearman, Kendall, Correlation Ratio)

## Technical Architecture

### **Design Patterns**
- **MVC Architecture**: Clean separation of Models, Views, and Controllers
- **Strategy Pattern**: Pluggable algorithms for different statistical tests
- **Factory Pattern**: Dynamic creation of test objects and estimators
- **Observer Pattern**: UI state management and real-time updates
- **Event Bus**: Centralized publish–subscribe system that enables decoupled communication between components.
- **Register Pattern**: Centralized registry maintaining available statistical distributions, tests, etc.

### **Core Components**
- **Models**: Statistical distributions, test implementations, data structures
- **Controllers**: Business logic for analysis, data processing, and UI coordination
- **Services**: Reusable components for data loading, transformation, and rendering
- **Views**: PyQt-based UI components organized in tabs and widgets

## Installation

### Setup
```bash
git clone https://github.com/deyme17/MatStat-Analytics.git
cd MatStat-Analytics
pip install -r requirements.txt
python main.py
```

## Project Structure

```
MatStat-Analytics/
├── controllers/          # Business logic controllers
│   ├── analysis_controller/    # Statistical analysis
│   ├── data_controllers/       # Data management
│   ├── dp_controllers/         # Data preprocessing
├── models/              # Core statistical models
│   ├── gofs/                   # Goodness-of-fit tests
│   ├── homogens/               # Homogeneity tests
│   ├── correlarion_coeffs/     # Correltion coefficients
│   ├── regression/             # Regression algorithms/models
│   ├── params_estimators/      # Parameter estimation
│   ├── data_processors/        # Data preprocessing
│   ├── stat_distributions/     # Statistical distributions
│   ├── simulation_engine.py    # Generation of data samples
│   ├── stat_calculator.py      # Statictics calculation
│   └──data_model.py            # main model of the data 
├── services/            # Reusable services
│   ├── stat_services/          # Statistics utilities
│   ├── data_services/          # Data I/O and management
│   └── ui_services/            # UI rendering and utilities
├── views/               # User interface components
│   ├── tabs/                   # Main application tabs
│   └── widgets/                # Specialized UI widgets
└── utils/               # Helper utilities and decorators
```