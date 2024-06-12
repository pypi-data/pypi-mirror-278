from task_ai.utils import del_safe, duration_to_str
class Task():
    def __init__(self, json_data):
        self.json_data = json_data

    def cleanup(self):
        if not self.json_data.get("lfEnabled", False):
            self.delete_late_finish_fields()
        if not self.json_data.get("efEnabled", False):
            self.delete_early_finish_fields()
        if not self.json_data.get("lsEnabled", False):
            self.delete_late_start_fields()
        
        return self.json_data
    
    def add_helper(self):
        if "lfDuration" in self.json_data:
            self.json_data["lfDuration"] = duration_to_str(self.json_data["lfDuration"])
        if "efDuration" in self.json_data:
            self.json_data["efDuration"] = duration_to_str(self.json_data["efDuration"])
        if "lsDuration" in self.json_data:
            self.json_data["lsDuration"] = duration_to_str(self.json_data["lsDuration"])
        
        return self.json_data


    def delete_late_finish_fields(self):
        field_list = [ 
                "lfDayConstraint",
                "lfDuration",
                "lfEnabled",
                "lfNthAmount",
                "lfOffsetDuration",
                "lfOffsetDurationUnit",
                "lfOffsetPercentage",
                "lfOffsetType",
                "lfTime",
                "lfType"]
        for field in field_list:
            del_safe(self.json_data, field)

    def delete_early_finish_fields(self):
        field_list = [ 
                "efDayConstraint",
                "efDuration",
                "efEnabled",
                "efNthAmount",
                "efOffsetDuration",
                "efOffsetDurationUnit",
                "efOffsetPercentage",
                "efOffsetType",
                "efTime",
                "efType"
        ]

        for field in field_list:
            del_safe(self.json_data, field)

    def delete_late_start_fields(self):
        field_list = [ 
                "lsDayConstraint",
                "lsDuration",
                "lsEnabled",
                "lsNthAmount",
                "lsTime",
                "lsType",
        ]

        for field in field_list:
            del_safe(self.json_data, field)