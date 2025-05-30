class DataHistoryManager:
    """
    Manager for handling versions of datasets (DataModel instances).
    """

    def __init__(self):
        """
        Initialize an empty dataset manager.
        """
        self.datasets = {}        # {label: DataModel}
        self.current_key = None   # label of active dataset

    def add_dataset(self, label: str, model):
        """
        Add a new dataset and set it as current.

        :param label: name/description of the dataset
        :param model: DataModel instance
        """
        self.datasets[label] = model
        self.current_key = label

    def switch_to(self, label: str):
        """
        Switch to a previously added dataset by its label.

        :param label: label of dataset to switch to
        """
        if label in self.datasets:
            self.current_key = label

    def get_current_data(self):
        """
        Return the currently active DataModel.

        :return: DataModel or None if not found
        """
        if self.current_key and self.current_key in self.datasets:
            return self.datasets[self.current_key]
        return None

    def get_original_data(self):
        """
        Return the original (first) version of the current dataset.

        :return: original DataModel or None
        """
        current = self.get_current_data()
        return current.revert_to_original() if current else None

    def update_current_data(self, new_model):
        """
        Replace the current dataset with a new version.

        :param new_model: new DataModel instance to assign
        """
        if self.current_key:
            self.datasets[self.current_key] = new_model

    def get_all_descriptions(self) -> list[str]:
        """
        Return all labels of stored datasets.

        :return: list of strings (dataset labels)
        """
        return list(self.datasets.keys())

    def get_data_description(self) -> str:
        """
        Return the label of the current dataset.

        :return: label string or "Unnamed"
        """
        return self.current_key or "Unnamed"