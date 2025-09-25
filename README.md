# MatStat-Analytics

A comprehensive Python application for statistical analysis, data processing, and visualization with support for multidimensional datasets and advanced statistical testing.

## Overview

MatStat-Analytics is a full-featured statistical analysis tool built with PyQt that provides extensive capabilities for data analysis, hypothesis testing, parameter estimation, and simulation. The application supports both univariate and multivariate data analysis with an intuitive tabbed interface.

## Key Features

### 📊 **Data Management & Processing**
- **Multi-format Support**: Load data from `.txt`, `.csv`, `.xls`, `.xlsx` files
- **Multidimensional Data**: Full support for datasets with multiple columns/variables
- **Column Selection**: Choose specific columns for analysis operations
- **Data Versioning**: Track changes with rollback capabilities to original or previous states
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

### 🎲 **Simulation & Modeling**
- **Sample Simulation**: Generate synthetic datasets from theoretical distributions
- **Export Capabilities**: Save simulation results as CSV files

### 📊 **Advanced Visualization**

#### **Interactive Graphs**
- **Histograms**: 
  - Automatic and manual bin selection
  - Frequency polygons (via checkbox)
  - Density overlays
- **Distribution Plots**:
  - Empirical Distribution Functions (EDF)
  - Theoretical distribution overlays
  - Cumulative frequency curves (ogives) with checkbox control
- **Comparative Analysis**: Side-by-side empirical vs theoretical comparisons

## Technical Architecture

### **Design Patterns**
- **MVC Architecture**: Clean separation of Models, Views, and Controllers
- **Strategy Pattern**: Pluggable algorithms for different statistical tests
- **Factory Pattern**: Dynamic creation of test objects and estimators
- **Observer Pattern**: UI state management and real-time updates

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
│   └── ui_controllers/         # UI state management
├── models/              # Core statistical models
│   ├── gofs/                  # Goodness-of-fit tests
│   ├── homogens/             # Homogeneity tests
│   ├── params_estimators/    # Parameter estimation
│   └── stat_distributions/   # Statistical distributions
├── services/            # Reusable services
│   ├── analysis_services/    # Analysis utilities
│   ├── data_services/        # Data I/O and management
│   ├── dp_services/          # Data preprocessing
│   └── ui_services/          # UI rendering and utilities
├── views/               # User interface components
│   ├── tabs/                 # Main application tabs
│   └── widgets/              # Specialized UI widgets
└── utils/               # Helper utilities and decorators
```