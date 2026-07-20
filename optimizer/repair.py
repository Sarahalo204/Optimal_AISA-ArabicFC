# optimizer/repair.py
from validator import PredictionValidator
from normalizer import Normalizer
from schema_caster import SchemaCaster
from argument_completion import ArgumentCompletion

class Coordinator:
    def __init__(self):
        pass

    def coordinate(self, prediction, question_text=""):
        # 1. Normalize (Arabic to English digits, strip spaces)
        prediction = Normalizer.normalize(prediction)
        
        # 2. Validate (Drop non-schema keys & anti-hallucination)
        prediction = PredictionValidator.validate(prediction, question_text)
        
        # 3. Cast to proper types (int/float) based on schema
        prediction = SchemaCaster.cast(prediction)
        
        # 4. Logical Inference / Argument Completion
        prediction = ArgumentCompletion.complete(prediction, question_text)

        # Ensure track B 'think' field is present
        if "think" not in prediction:
            prediction["think"] = "تحليل السؤال لاستدعاء الأداة المناسبة."
            
        return prediction
