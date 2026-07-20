# optimizer/schema_caster.py
from schema import TOOL_SCHEMAS
import re

class SchemaCaster:
    @staticmethod
    def _safe_cast_number(value, target_type):
        if value is None:
            return None
        
        # If it's already a number
        if isinstance(value, (int, float)):
            if target_type == "integer":
                return int(value)
            elif target_type == "float":
                return float(value)
            return value

        # If it's a string, attempt to extract number
        str_val = str(value)
        # Extract first number from string (e.g. "1200.5" -> "1200.5")
        match = re.search(r'-?\d+(\.\d+)?', str_val)
        if not match:
            return value # If no number found, keep string to avoid crash
            
        num_str = match.group(0)
        try:
            if target_type == "integer":
                return int(float(num_str))
            elif target_type == "float":
                return float(num_str)
        except ValueError:
            return value
            
        return value

    @staticmethod
    def cast(prediction):
        tool = prediction.get("tool_called", "none")
        args = prediction.get("arguments", {})

        if tool == "none" or tool not in TOOL_SCHEMAS or not isinstance(args, dict):
            return prediction

        schema_req = TOOL_SCHEMAS[tool].get("required", {})
        schema_opt = TOOL_SCHEMAS[tool].get("optional", {})
        
        # Combine schemas
        full_schema = {**schema_req, **schema_opt}

        for key, value in args.items():
            if key in full_schema:
                expected_type = full_schema[key]
                if expected_type in ["integer", "float"]:
                    args[key] = SchemaCaster._safe_cast_number(value, expected_type)
                # If expected_type is "string", we deliberately don't cast to float even if it looks like one.
                elif expected_type == "string" and not isinstance(value, str):
                    args[key] = str(value)

        prediction["arguments"] = args
        return prediction
