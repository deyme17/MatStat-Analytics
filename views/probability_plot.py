import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def plot_exponential_grid(ax, data):
    """
    Creates an exponential probability grid and plots data on it.
    
    Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot.
        data (array-like): Input dataset without NaN values.
    """
    if data is None or len(data) == 0:
        ax.clear()
        ax.text(0.5, 0.5, "No valid data available", 
                ha='center', va='center', transform=ax.transAxes)
        return
    
    try:
        ax.clear()
        
        data_sorted = np.sort(data)
        n = len(data_sorted)
        
        # median rank method
        i = np.arange(1, n + 1)
        empirical_probs = (i - 0.3) / (n + 0.4)
        
        # exp
        transformed_probs = -np.log(1 - empirical_probs)
        
        # vert lines
        x_max = max(data_sorted) * 1.1
        x_grid = np.linspace(0, x_max, 11)
        
        # hor lines
        prob_values = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
        y_grid = [-np.log(1 - p) for p in prob_values]
        
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, max(transformed_probs) * 1.1)
        
        # add grid
        ax.grid(True, color='lightgray', linestyle='-', alpha=0.7)
        
        for p, y in zip(prob_values, y_grid):
            ax.axhline(y=y, color='gray', linestyle='-', alpha=0.5)
            if p in [0.1, 0.3, 0.5, 0.7, 0.9]:
                ax.text(-0.01 * x_max, y, f"{p:.2f}", 
                        va='center', ha='right', fontsize=7)
        
        ax.set_yticks(y_grid)
        ax.set_yticklabels([])
        
        # plot the data
        ax.plot(data_sorted, transformed_probs, 'o', markersize=5, 
                color='blue', label='Data')
        
        # set labels and title
        ax.set_xlabel('Data Values')
        ax.set_ylabel('Probability')
        ax.set_title('Exponential Probability Grid')
        
        # stright line
        lambda_est = 1 / np.mean(data_sorted)
        x_line = np.linspace(0, x_max, 100)
        y_line = lambda_est * x_line
        ax.plot(x_line, y_line, 'r--', linewidth=1.5, 
                label=f'Reference Line (λ={lambda_est:.4f})')
        
        ax.legend(framealpha=0.5)
        ax.set_facecolor('#f0f8ff')
        
    except Exception as e:
        ax.clear()
        ax.text(0.5, 0.5, f"Error creating probability grid: {str(e)}", 
                ha='center', va='center', transform=ax.transAxes)