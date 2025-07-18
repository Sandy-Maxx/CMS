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
        
        # Load existing data
        existing_data = self.load_template_data(template_path)
        
        # Update with new data, appending to history
        for key, value in data.items():
            if key not in existing_data or not isinstance(existing_data[key], dict):
                # If the key doesn't exist or the existing data is not in the new format, create it
                existing_data[key] = {"current": value, "history": [value]}
            else:
                # Otherwise, update the existing data
                existing_data[key]["current"] = value
                if value not in existing_data[key]["history"]:
                    existing_data[key]["history"].append(value)

        with open(data_path, 'w') as f:
            json.dump(existing_data, f, indent=4)

    def load_template_data(self, template_path):
        data_path = self._get_template_data_path(template_path)
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                return json.load(f)
        return {}

    def get_historical_data(self, template_path, placeholder_name):
        data = self.load_template_data(template_path)
        if placeholder_name in data and "history" in data[placeholder_name]:
            return data[placeholder_name]["history"]
        return []
