# MatStat-Analytics 
A Python tool for basic statistical analysis and visualization of datasets.

## Key Features

1. **Data Preparation**  
   - Load `.txt`, `.csv`, `.xls(x)` files  
   - Clean and manage missing data  
   - Apply transformations (standardize, log, shift)

2. **Exploratory Analysis**  
   - Generate frequency distributions  
   - Build histograms and CDF (auto/manual bin selection)  
   - Calculate key statistics (mean, median, std.dev, skewness, kurtosis)

3. **Advanced Options**  
   - Confidence intervals (custom precision)  
   - Goodness-of-fit tests (Pearson's χ², Refined Kolmogorov-Smirnov)  
   - Compare empirical and theoretical CDFs with confidence bands  
   - Data transformations (normalization, log, shift)  
   - Outlier detection and removal (σ-rule, asymmetry, γ-confidence)  
   - Missing data imputation (mean, median, interpolation) or removal  
   - Version control and rollback to original or previous data states

4. **Visualization**  
   - Histograms with optional KDE  
   - Distribution overlays (Normal, Laplace, Weibull, Exponential, Uniform)  
   - Cumulative distribution function (empirical + theoretical with CI bands)  
   - Interactive PyQt interface with data version selector and state tracking
