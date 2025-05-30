from services.analysis_services.statistics_service import StatisticsService

class StatisticController:
    """
    Controller for managing the display of statistical characteristics in the UI.
    """

    def __init__(self, window):
        self.window = window

    def update_statistics_table(self):
        """
        Recalculate statistics and update the UI statistics table.
        """
        model = self.window.data_model
        if model is None or model.series.empty:
            return
        
        bins = self.window.graph_panel.bins_spinbox.value()
        model.update_bins(bins)

        confidence = self.window.graph_panel.confidence_spinbox.value()

        StatisticsService.update_table(
            self.window.stat_tab.conf_table,
            model.hist,
            model.series,
            precision=self.window.precision_spinbox.value(),
            confidence_level=confidence
        )

    def clear(self):
        """
        Clear the contents of the statistics table.
        """
        self.window.stat_tab.conf_table.clearContents()
        self.window.stat_tab.conf_table.setRowCount(0)
