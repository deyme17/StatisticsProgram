from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from models.stat_distributions import registered_distributions
from services.analysis_services.parameter_estimation import ParameterEstimation
import pandas as pd

class ParamEstimationTab(QWidget):
    """
    A QWidget tab that allows users to estimate distribution parameters using different methods.
    """

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.estimation_service = ParameterEstimation()
        self._init_ui()

    def _init_ui(self):
        """
        Initializes and lays out all widgets in the tab.
        """
        layout = QVBoxLayout()

        # choosing distribution
        self.dist_combo = QComboBox()
        self.dist_combo.addItems(registered_distributions.keys())

        # choosing estimation method
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Method of Moments", "Maximum Likelihood Method"])

        self.estimate_button = QPushButton("Estimate Parameters")
        self.estimate_button.clicked.connect(self.estimate_parameters)

        # results
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Parameter", "Estimated Value"])

        # layout
        layout.addWidget(QLabel("Select Distribution:"))
        layout.addWidget(self.dist_combo)
        layout.addWidget(QLabel("Select Estimation Method:"))
        layout.addWidget(self.method_combo)
        layout.addWidget(self.estimate_button)
        layout.addWidget(self.result_table)
        self.setLayout(layout)

    def estimate_parameters(self):
        """
        Estimates parameters of the selected distribution using the chosen method.
        Displays results in the table.
        """
        if not hasattr(self.window, 'data_model') or self.window.data_model is None:
            self.window.show_error_message("No Data", "No data loaded. Please load a dataset first.")
            return

        data = self.window.data_model.series
        if data.empty or data.isna().all():
            self.window.show_error_message("Invalid Data", "Loaded data is empty or contains only NaN values.")
            return

        dist_name = self.dist_combo.currentText()
        method = self.method_combo.currentText()
        method_map = {
            "Method of Moments": "method_of_moments",
            "Maximum Likelihood Method": "maximum_likelihood"
        }
        method = method_map.get(method)
        # Estimate parameters
        try:
            params = self.estimation_service.estimate(dist_name, method, data)
            if params is None:
                self.window.show_error_message("Estimation Failed", f"Could not estimate parameters for {dist_name}.")
                return

            # parameter names
            dist_class = registered_distributions.get(dist_name)
            if not dist_class:
                self.window.show_error_message("Unsupported", f"Distribution {dist_name} is not supported.")
                return
            dist_instance = dist_class()
            param_names = list(dist_instance.distribution_params.keys())

            # results
            self.result_table.setRowCount(len(params))
            for i, (name, value) in enumerate(zip(param_names, params)):
                self.result_table.setItem(i, 0, QTableWidgetItem(name))
                self.result_table.setItem(i, 1, QTableWidgetItem(f"{value:.4f}"))

        except Exception as e:
            self.window.show_error_message("Error", f"Failed to estimate parameters: {str(e)}")