import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

class Hist:
    def __init__(self, data, bins=10):
        self.data = data
        self.bins = bins


    def plot_hist(self, ax):
        if self.data is not None:
            # hist
            sns.histplot(self.data, bins=self.bins, kde=True, ax=ax, 
                        edgecolor='black', alpha=0.7, stat='probability', label='Histogram')
            
            ax.set_title('Histogram with Density Curve')
            ax.set_xlabel('Values')
            ax.set_ylabel('Relative Frequency')