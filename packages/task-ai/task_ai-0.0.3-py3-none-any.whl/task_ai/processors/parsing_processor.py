from task_ai.utils import get_template_by_type
import click
import json
from task_ai.models.task import Task

class ParsingProcessor:
    def __init__(self, anonymizer, config, processing_config, logger):
        self.anonymizer = anonymizer
        self.config = config
        self.logger = logger
        self.exclude_list = processing_config.get("exclude", [])
        self.include_list = processing_config.get("include", [])
        self.logger.debug(f"Exclude list {self.exclude_list}")
        self.logger.debug(f"Include list {self.include_list}")

    def process(self, json_data):
        # Determine the template based on the 'type' field in actual JSON
        json_type = json_data.get('type')
        if not json_type:
            raise ValueError("The 'type' field is missing in the actual JSON.")
        
        try:
            template_path = self.config.get("template_path", "templates")
            template_json = get_template_by_type(json_type, template_path=template_path)
        except FileNotFoundError as e:
            click.echo(str(e))
            return
        
        extracted_values = self.extract_values(template_json, json_data)
        self.logger.debug("Extracted values: {}".format(extracted_values))

        if json_type.startswith("task"):
            task = Task(extracted_values)
            extracted_values = task.cleanup()
            extracted_values = task.add_helper()

        anonymouse_values, removed_values = self.anonymizer.process(extracted_values)
        self.logger.debug("Anonymized values: {}".format(anonymouse_values))
        self.logger.debug("Removed values: {}".format(removed_values))
        # print(json.dumps(anonymouse_values, indent=2))

        return anonymouse_values, removed_values
        

    def extract_values(self, template, actual):
        extracted = {}
        for key, tmpl_value in template.items():
            if key in self.exclude_list:
                continue

            if key in actual:
                actual_value = actual[key]
                if key in self.include_list:
                    extracted[key] = actual_value
                    continue

                # Compare values
                if isinstance(tmpl_value, dict) and isinstance(actual_value, dict):
                    nested_extracted = self.extract_values(tmpl_value, actual_value)
                    if nested_extracted:  # Only add if there's something different
                        extracted[key] = nested_extracted
                elif isinstance(tmpl_value, list) and isinstance(actual_value, list):
                    if actual_value != tmpl_value:
                        extracted[key] = actual_value
                else:
                    if actual_value != tmpl_value:
                        if actual_value is not None:  # Filter out None values
                            extracted[key] = actual_value

        return extracted