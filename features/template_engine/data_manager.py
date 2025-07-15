import json
import os

class TemplateDataManager:
    def __init__(self, data_dir="./template_data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def _get_template_data_path(self, template_path):
        # Create a unique filename for each template's data
        template_filename = os.path.basename(template_path)
        data_filename = f"{template_filename}.json"
        return os.path.join(self.data_dir, data_filename)

    def save_template_data(self, template_path, data):
        data_path = self._get_template_data_path(template_path)
        with open(data_path, 'w') as f:
            json.dump(data, f, indent=4)

    def load_template_data(self, template_path):
        data_path = self._get_template_data_path(template_path)
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                return json.load(f)
        return {}
