# optimizer/schema.py
# القالب المرجعي (Schema) للـ 27 دالة المعتمدة في المسابقة

TOOL_SCHEMAS = {
    # 1. الخدمات الإسلامية
    "get_prayer_times": {
        "required": {"city": "string"},
        "optional": {"date": "string", "country": "string"}
    },
    "calculate_zakat": {
        "required": {"amount": "float", "type": "string"},
        "optional": {"currency": "string", "weight_unit": "string"}
    },
    "get_qibla_direction": {
        "required": {"city": "string"},
        "optional": {"latitude": "float", "longitude": "float"}
    },
    "search_quran": {
        "required": {"query": "string"},
        "optional": {"search_type": "string", "surah_number": "integer"}
    },
    "get_hadith": {
        "required": {"query": "string"},
        "optional": {"narrator": "string"}
    },
    "calculate_inheritance": {
        "required": {"estate_value": "float", "deceased_gender": "string", "heirs": "array"},
        "optional": {"currency": "string"}
    },

    # 2. الخدمات الحكومية
    "check_visa_status": {
        "required": {}, 
        "optional": {"visa_number": "string", "passport_number": "string", "nationality": "string"}
    },
    "check_iqama_status": {
        "required": {"iqama_number": "string"},
        "optional": {"border_number": "string"}
    },
    "check_traffic_violations": {
        "required": {"id_number": "string"},
        "optional": {"plate_number": "string"}
    },
    "book_government_appointment": {
        "required": {"department": "string", "city": "string"},
        "optional": {"date": "string"}
    },
    "calculate_end_of_service": {
        "required": {"salary": "float", "years_of_service": "float"},
        "optional": {"termination_type": "string", "country": "string"}
    },

    # 3. البنوك والمالية
    "convert_currency": {
        "required": {"amount": "float", "from_currency": "string", "to_currency": "string"},
        "optional": {}
    },
    "get_gold_price": {
        "required": {"karat": "integer"},
        "optional": {"currency": "string", "country": "string"}
    },
    "calculate_loan": {
        "required": {"amount": "float", "years": "integer", "interest_rate": "float"},
        "optional": {}
    },
    "transfer_money": {
        "required": {"amount": "float", "currency": "string", "recipient_name": "string"},
        "optional": {"recipient_iban": "string", "bank_name": "string"}
    },

    # 4. التجارة الإلكترونية
    "track_shipment": {
        "required": {"tracking_number": "string"},
        "optional": {"carrier": "string"}
    },
    "compare_prices": {
        "required": {"product_name": "string", "country": "string"},
        "optional": {"category": "string"}
    },
    "calculate_customs": {
        "required": {"product_value": "float", "destination_country": "string", "category": "string"},
        "optional": {"currency": "string"}
    },
    "order_food": {
        "required": {"restaurant": "string", "items": "string"},
        "optional": {"delivery_address": "string"}
    },

    # 5. السفر
    "search_flights": {
        "required": {"origin": "string", "destination": "string", "departure_date": "string"},
        "optional": {"return_date": "string", "passengers": "integer"}
    },
    "search_hotels": {
        "required": {"city": "string"},
        "optional": {"check_in": "string", "check_out": "string", "guests": "float", "stars": "integer"}
    },
    "search_umrah_packages": {
        "required": {"departure_city": "string", "num_persons": "float"},
        "optional": {"departure_date": "string", "duration_days": "integer", "hotel_rating": "integer"}
    },

    # 6. الصحة
    "book_doctor_appointment": {
        "required": {"city": "string", "specialty": "string"},
        "optional": {"date": "string", "doctor_name": "string"}
    },
    "search_medications": {
        "required": {"medication_name": "string"},
        "optional": {"country": "string"}
    },
    "check_insurance_coverage": {
        "required": {"procedure": "string"},
        "optional": {"insurance_number": "string"}
    },

    # 7. الطقس
    "get_weather": {
        "required": {"city": "string"},
        "optional": {"days": "float", "country": "string"}
    },
    "get_air_quality": {
        "required": {"city": "string"},
        "optional": {"country": "string"}
    }
}
