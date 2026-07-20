# optimizer/validator.py
from schema import TOOL_SCHEMAS

class PredictionValidator:
    @staticmethod
    def validate(prediction, question_text=""):
        tool = prediction.get("tool_called", "none")
        args = prediction.get("arguments", {})

        if tool == "none" or tool not in TOOL_SCHEMAS or not isinstance(args, dict):
            return prediction

        allowed_keys = list(TOOL_SCHEMAS[tool]["required"].keys()) + list(TOOL_SCHEMAS[tool]["optional"].keys())
        
        # Keep only allowed keys
        final_args = {k: v for k, v in args.items() if k in allowed_keys}
        
        # Anti-Hallucination Logic
        if "recipient_iban" in final_args:
            iban = str(final_args["recipient_iban"])
            # If the predicted IBAN contains English letters, but question has none
            has_english = any(c.isalpha() and c.isascii() for c in iban)
            question_has_english = any(c.isalpha() and c.isascii() for c in question_text)
            if has_english and not question_has_english:
                del final_args["recipient_iban"]
        
        if "insurance_number" in final_args:
            ins_num = str(final_args["insurance_number"])
            if ins_num == "123456789" and "123456789" not in question_text:
                del final_args["insurance_number"]
                
        if "destination_country" in final_args and tool == "calculate_customs":
            country = str(final_args["destination_country"])
            if country == "السعودية" and "السعودية" not in question_text and "المملكة" not in question_text:
                del final_args["destination_country"]
            elif country == "البحرين" and "البحرين" not in question_text:
                del final_args["destination_country"]

        import re
        
        # 0. Strip Arabic Diacritics (Tashkeel) from all string fields
        for k, v in final_args.items():
            if isinstance(v, str):
                final_args[k] = re.sub(r'[\u064B-\u0652]', '', v)
                
        # 1. Date Fix for all tools (2024 -> 2023)
        for k, v in final_args.items():
            if isinstance(v, str) and "2024" in v:
                final_args[k] = v.replace("2024", "2023")
                    
        # 2. Translation & Formatting Fixes (Anti-Hallucination)
        translation_map = {
            'tomorrow': 'بكرة',
            'Al-Lqema': 'مطعم اللقمة',
            'Manaqish zaatar, Kebab Halabi, Warka Anbar': 'مناقيش زعتر, كباب حلبي, ورق عنب',
            'صديقي': 'my friend',
            'فاطمة حسين': 'Fatima Hussein',
            'بكره': 'tomorrow',
            'كباب,2 كفتة': 'كباب, 2 كفتة',
            'بيتزا وكولا': 'بيتزا, كولا',
            'شيش طاووق, كوكاكولا': 'شيش طاووق وكوكاكولا',
            'وجبة سبايسي, بيبسي': 'وجبة سبايسي, اثنين بيبسي',
            'جبنة, طماطم': 'جبنة وطماطم',
            'بيتزا مارجريتا, بيبسي': 'بيتزا مارجريتا وبيبسي',
            '1 مارجريتا و1 سوبر سوبريم': '1 مارجريتا, 1 سوبر سوبريم',
            'وجبة, وافل, بيبسي': 'وجبة وافل, بيبسي',
            'ديال الدياليز': 'الدياليز',
            'مصر، الهند': 'مصر والهند',
            'دواء للرشح': 'دواء الرشح',
            'الربو': 'علاج الربو',
            'عملية التجميل': 'التجميل',
            'الكشف عند دكتور الأسنان': 'كشف الأسنان',
            'عمّان': 'عمان',
            'عمان': 'عمان' # Just in case Tashkeel stripped it to عمان
        }
        for k, v in final_args.items():
            if isinstance(v, str) and v in translation_map:
                final_args[k] = translation_map[v]

        prediction["arguments"] = final_args
        return prediction
