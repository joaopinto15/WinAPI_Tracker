import os
import json

class OutputLogger:
    def __init__(self, output_path):
        self.output_path = output_path
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        self.output_data = self._load_or_initialize()

    def _load_or_initialize(self):
        if os.path.exists(self.output_path):
            try:
                with open(self.output_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        else:
            self._save([])
            return []

    def _save(self, data):
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def append(self, entry):
        self.output_data.append(entry)
        self._save(self.output_data)
