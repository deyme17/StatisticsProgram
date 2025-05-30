import numpy as np
from scipy import interpolate

class EDFRenderer:
    """
    Renderer for drawing the Empirical Distribution Function (EDF)
    as a step function and optional interpolated curve.
    """

    @staticmethod
    def render(ax, data, bin_edges=None, show_edf_curve=False):
        """
        Render the EDF on a given Matplotlib axis.

        :param ax: Matplotlib axis to draw on
        :param data: pandas Series or NumPy array of values
        :param bin_edges: optional array of bin edges for step approximation
        :param show_edf_curve: whether to show a smoothed EDF curve
        """
        data = np.sort(data.dropna().values)
        n = len(data)

        if bin_edges is not None:
            bin_counts, _ = np.histogram(data, bins=bin_edges)
            cum_counts = np.cumsum(bin_counts)
            cum_rel_freq = cum_counts / cum_counts[-1]

            for i in range(len(bin_edges) - 1):
                x = [bin_edges[i], bin_edges[i + 1]]
                y = [cum_rel_freq[i], cum_rel_freq[i]]
                ax.plot(x, y, 'c->', linewidth=2)
            ax.plot(bin_edges[-1], 1, 'c>', markersize=2)

        if show_edf_curve:
            y_edf = np.arange(1, n + 1) / n
            x_curve = np.linspace(data[0], data[-1], 300)
            f_interp = interpolate.interp1d(
                data, y_edf, kind='linear', bounds_error=False, fill_value=(0, 1)
            )
            y_interp = f_interp(x_curve)
            ax.plot(x_curve, y_interp, '-', color='c', label='EDF Curve', linewidth=2, alpha=0.1)

        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel('Values')
        ax.set_ylabel('Probability')
        ax.set_title('Empirical Distribution Function')
        ax.grid(True, alpha=0.3)