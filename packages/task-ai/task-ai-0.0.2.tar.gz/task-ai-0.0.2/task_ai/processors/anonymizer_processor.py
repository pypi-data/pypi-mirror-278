class AnonymizerProcessor:
    def __init__(self, config, logger):
        self.config = config
        self.sensitive_list = self.config.get("fields", [])
        self.logger = logger

    def process(self, json_data):
        extracted = {}
        removed_values = {}
        for key, value in json_data.items():
            if key in self.sensitive_list:
                removed_values[key] = value
                extracted[key] = f"{{{key}}}"
                continue

            # Compare values
            if isinstance(value, dict):
                nested_extracted = self.process(value)
                if nested_extracted:  # Only add if there's something different
                    extracted[key] = nested_extracted
            else:
                extracted[key] = value

        return extracted, removed_values
    