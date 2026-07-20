import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from repair import Coordinator

def run_tests():
    coordinator = Coordinator()

    # Test 1: Arabic Numbers
    p1 = {
        "id": "18",
        "tool_called": "check_iqama_status",
        "arguments": {"iqama_number": "٤٤٥٥٦٦"}
    }
    q1 = "يا ترى صلاحية إقامتي انتهت؟ رقمي ٤٤٥٥٦٦"
    
    out1 = coordinator.coordinate(p1, q1)
    assert out1["arguments"]["iqama_number"] == "445566", f"Failed: {out1}"
    print("Test 1 (Arabic Numbers): PASSED")

    # Test 2: Termination Type Inference (end_of_contract)
    p2 = {
        "id": "38",
        "tool_called": "calculate_end_of_service",
        "arguments": {"salary": 3000.0, "years_of_service": 8.0}
    }
    q2 = "كيف بتنحسب مكافأة نهاية الخدمة إذا راتبي 3000 وسنوات الخدمة 8 وسبب الفصل إنهاء عقد؟"
    
    out2 = coordinator.coordinate(p2, q2)
    assert out2["arguments"]["termination_type"] == "end_of_contract", f"Failed: {out2}"
    print("Test 2 (Inference end_of_contract): PASSED")

    # Test 3: IBAN Preservation (No deletion)
    p3 = {
        "id": "332",
        "tool_called": "transfer_money",
        "arguments": {
            "amount": 1000.0,
            "currency": "درهم",
            "recipient_name": "عيسى",
            "recipient_iban": "OM1122334455"
        }
    }
    q3 = "أبي أحول ١٠٠٠ درهم لحساب عيسى في عمان رقم الحساب OM1122334455"
    out3 = coordinator.coordinate(p3, q3)
    assert out3["arguments"]["recipient_iban"] == "OM1122334455", f"Failed: {out3}"
    print("Test 3 (IBAN Preservation): PASSED")

    # Test 4: Weather Days Inference
    p4 = {
        "id": "298",
        "tool_called": "get_weather",
        "arguments": {"city": "بيروت"}
    }
    q4 = "كيف الجو في بيروت اليوم؟"
    out4 = coordinator.coordinate(p4, q4)
    assert out4["arguments"]["days"] == 1.0, f"Failed: {out4}"
    print("Test 4 (Weather Days Inference): PASSED")

    # Test 5: Float casting
    p5 = {
        "id": "999",
        "tool_called": "calculate_end_of_service",
        "arguments": {"salary": "3000", "years_of_service": "8.5"}
    }
    out5 = coordinator.coordinate(p5, "")
    assert isinstance(out5["arguments"]["salary"], float) and out5["arguments"]["salary"] == 3000.0, f"Failed: {out5}"
    assert isinstance(out5["arguments"]["years_of_service"], float) and out5["arguments"]["years_of_service"] == 8.5, f"Failed: {out5}"
    print("Test 5 (Float Casting): PASSED")

    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
