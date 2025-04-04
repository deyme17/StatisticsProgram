import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

class StatisticalDistributions:
    """Class for handling various statistical distributions and their visualization."""
    
    def __init__(self):
        self.available_distributions = {
            'Normal': self._fit_normal,
            'Exponential': self._fit_exponential,
            'Uniform': self._fit_uniform,
            'Weibull': self._fit_weibull,
        }
        
        self.dist_colors = {
            'Normal': 'red',
            'Exponential': 'green',
            'Uniform': 'purple',
            'Weibull': 'orange',
        }
    
    def get_available_distributions(self):
        """Return list of available distribution names."""
        return list(self.available_distributions.keys())
    
    def get_distribution_color(self, dist_name):
        """Get the default color for a distribution."""
        return self.dist_colors.get(dist_name, 'blue')
    
    def fit_distribution(self, data, dist_name):
        """Fit specified distribution to data and return parameters."""
        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        
        if len(data_clean) == 0:
            raise ValueError("No valid data points after removing NaN values")
            
        if dist_name in self.available_distributions:
            return self.available_distributions[dist_name](data_clean)
        else:
            raise ValueError(f"Distribution '{dist_name}' not supported")
    
    def plot_distribution(self, ax, data, dist_name, color=None, label=None, **kwargs):
        """
        Plot the specified distribution fitted to data.
        
        Parameters:
            ax: matplotlib axis to plot on
            data: data to fit the distribution to
            dist_name: name of the distribution to fit
            color: color for the line (uses defaults if None)
            label: label for the legend (uses distribution name if None)
            **kwargs: Additional plotting parameters like linewidth
        
        Returns:
            bool: True if successful, False otherwise
        """
        if dist_name not in self.available_distributions:
            return False

        data_clean = data.dropna() if hasattr(data, 'dropna') else data[~np.isnan(data)]
        
        if len(data_clean) == 0:
            return False

        try:
            # get hist vals for proper normalization
            hist_values, bin_edges = np.histogram(data_clean, bins='auto', density=True)
            max_hist_value = np.max(hist_values) if len(hist_values) > 0 else 1.0
            
            if color is None:
                color = self.get_distribution_color(dist_name)
                
            if dist_name == 'Exponential':
                min_val = np.nanmin(data_clean)
                x_min = max(0, min_val * 0.8) if min_val > 0 else 0
                x_max = np.nanmax(data_clean) * 1.2
            elif dist_name == 'Uniform':
                params = self.fit_distribution(data_clean, dist_name)
                x_min = params[0] - 0.1 * (params[1] - params[0])  
                x_max = params[1] + 0.1 * (params[1] - params[0])  
            else:
                x_min = np.nanmin(data_clean) * 0.8
                x_max = np.nanmax(data_clean) * 1.2

            x = np.linspace(x_min, x_max, 1000)
            
            # fit dist
            params = self.fit_distribution(data_clean, dist_name)
            pdf_values = self._get_pdf_values(x, dist_name, params)
            
            # scaling
            pdf_max = np.max(pdf_values) if len(pdf_values) > 0 else 1.0
            if pdf_max > 0:
                pdf_values = pdf_values * (max_hist_value / pdf_max)
            
            # label
            if label is None:
                label = f"{dist_name} Distribution"
            
            # plot
            ax.plot(x, pdf_values, color=color, label=label, **kwargs)
                
            return True
        except Exception as e:
            print(f"Error plotting {dist_name} distribution: {str(e)}")
            return False
    
    def _get_pdf_values(self, x, dist_name, params):
        """Calculate PDF values for the given distribution and parameters."""
        if dist_name == 'Normal':
            return stats.norm.pdf(x, loc=params[0], scale=params[1])
        
        elif dist_name == 'Exponential':
            return stats.expon.pdf(x, loc=0, scale=1/params[0] if params[0] > 0 else 1)
        
        elif dist_name == 'Uniform':
            return stats.uniform.pdf(x, loc=params[0], scale=params[1]-params[0])
        
        elif dist_name == 'Weibull':
            shape = max(0.1, params[0]) 
            scale = max(0.1, params[1])
            return stats.weibull_min.pdf(x, c=shape, loc=0, scale=scale)
            
        else:
            return np.zeros_like(x)
    
    def _fit_normal(self, data):
        """Fit normal distribution and return parameters (mean, std)."""
        mean = np.nanmean(data)
        std = np.nanstd(data)
        if std == 0:
            std = 0.01
        return (mean, std)
    
    def _fit_exponential(self, data):
        """Fit exponential distribution and return parameters (lambda)."""
        min_val = np.nanmin(data)
        if min_val <= 0:
            data = data - min_val + 0.01
            
        mean = np.nanmean(data)
        if mean == 0:
            mean = 0.01
        return (1/mean,)
    
    def _fit_uniform(self, data):
        """Fit uniform distribution and return parameters (min, max)."""
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        if min_val == max_val:
            max_val = min_val + 0.01
        return (min_val, max_val)
    
    def _fit_weibull(self, data):
        """Fit Weibull distribution and return parameters (shape, scale)."""
        min_val = np.nanmin(data)
        if min_val <= 0:
            data = data - min_val + 0.01
        
        try:
            shape, _, scale = stats.weibull_min.fit(data, floc=0)
            shape = max(0.1, shape) 
            scale = max(0.1, scale) 
            return (shape, scale)
        except:
            mean = np.nanmean(data)
            std = np.nanstd(data)
            if std == 0:
                std = 0.01

            shape = 1.5  
            scale = mean / 0.9  
            return (shape, scale)