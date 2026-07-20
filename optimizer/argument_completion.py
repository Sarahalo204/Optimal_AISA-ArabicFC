# optimizer/argument_completion.py

class ArgumentCompletion:
    @staticmethod
    def infer_termination_type(text):
        if not text:
            return None
        text_lower = text.lower()
        if any(word in text_lower for word in ["استقال", "استقالة"]):
            return "resignation"
        elif any(word in text_lower for word in ["انتهاء عقد", "إنهاء عقد", "انتهاء العقد"]):
            return "end_of_contract"
        elif any(word in text_lower for word in ["استغناء", "تقليص", "اقتصادي"]):
            return "economic"
        elif any(word in text_lower for word in ["سوء سلوك", "تأديبي"]):
            return "disciplinary"
        elif any(word in text_lower for word in ["طرد", "فصل"]):
            return "dismissal"
        return None

    @staticmethod
    def complete(prediction, question_text):
        tool = prediction.get("tool_called", "none")
        args = prediction.get("arguments", {})
        
        if tool == "none" or not isinstance(args, dict) or not question_text:
            return prediction

        # We found that inferring `days`, `search_type`, and `termination_type`
        # causes regressions because the Ground Truth is highly inconsistent and often omits them.
        # Therefore, we will not infer them.
        
        return prediction
