# optimizer/normalizer.py

class Normalizer:
    @staticmethod
    def _normalize_arabic_digits(text):
        if not isinstance(text, str):
            return text
            
        arabic_digits = "٠١٢٣٤٥٦٧٨٩"
        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        english_digits = "0123456789"
        
        translation_table = str.maketrans(arabic_digits + persian_digits, english_digits * 2)
        return text.translate(translation_table)

    @staticmethod
    def normalize(prediction):
        args = prediction.get("arguments", {})
        if not isinstance(args, dict):
            return prediction

        for key, value in args.items():
            if isinstance(value, str):
                # 2. Strip excess whitespaces safely
                normalized = value.strip()
                
                # 1. Convert Arabic/Persian digits to English ONLY for ID/number fields
                # Do NOT convert for product_name, items, query etc. to preserve exact match
                if any(x in key for x in ["number", "iqama", "visa", "passport", "id", "tracking", "insurance"]):
                    normalized = Normalizer._normalize_arabic_digits(normalized)
                    
                args[key] = normalized
        
        prediction["arguments"] = args
        return prediction
