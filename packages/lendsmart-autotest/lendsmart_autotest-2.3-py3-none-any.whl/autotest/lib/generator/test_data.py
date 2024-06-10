"""
    Hold the test data sets
"""

TEST_DATA_SETS = [
    {
        "use_case_name": "mbwi_credit_card_approved",
        "namespaces": ["mbwi", "mbwidev"],
        "data": [
            {
                "category": "NAME_TEXT",
                "sub_categories": [
                    {
                        "key_fields": [],
                        "valid": {
                            "datas": [
                                {
                                    "first_name": "makesh",
                                    "last_name": "Muthu",
                                    "middle_name": "Mk",
                                }
                            ]
                        },
                    }
                ],
            },
            {
                "category": "TEXT_DATE",
                "sub_categories": [
                    {"key_fields": [], "valid": {"datas": ["10/30/1999"]}}
                ],
            },
            {
                "category": "ADDRESS",
                "sub_categories": [
                    {
                        "key_fields": [],
                        "valid": {"datas": ["123 Benton Camp Rd, Benton, IL, USA"]},
                    }
                ],
            },
            {
                "category": "SSN_QUESTION",
                "sub_categories": [
                    {"key_fields": [], "valid": {"datas": ["111111114"]}}
                ],
            },
            {
                "category": "PHONE_NUMBER",
                "sub_categories": [
                    {"key_fields": [], "valid": {"datas": ["2344444444"]}}
                ],
            },
            {
                "category": "SLIDER_AMOUNT",
                "sub_categories": [
                    {
                        "key_fields": [
                            "income_value",
                            "business_monthly_income_or_loss",
                        ],
                        "valid": {"datas": ["11123"]},
                    }
                ],
            },
            {
                "category": "TEXT",
                "sub_categories": [
                    {"key_fields": [], "valid": {"datas": ["Ahasjdh", "Hljaldjs"]}}
                ],
            },
        ],
    },
    {
        "use_case_name": "mbwi_credit_card_declined",
        "namespaces": ["mbwi", "mbwidev"],
        "data": [
            {
                "category": "NAME_TEXT",
                "sub_categories": [
                    {
                        "key_fields": [],
                        "valid": {
                            "datas": [
                                {
                                    "first_name": "Shniy",
                                    "last_name": "sk",
                                    "middile_name": "Mk",
                                }
                            ]
                        },
                    }
                ],
            },
            {
                "category": "TEXT_DATE",
                "sub_categories": [
                    {"key_fields": [], "valid": {"datas": ["10/30/1999"]}}
                ],
            },
            {
                "category": "ADDRESS",
                "sub_categories": [
                    {
                        "key_fields": [],
                        "valid": {"datas": ["123 Benton Camp Rd, Benton, IL, USA"]},
                    }
                ],
            },
            {
                "category": "SSN_QUESTION",
                "sub_categories": [
                    {"key_fields": [], "valid": {"datas": ["111-11-1112"]}}
                ],
            },
            {
                "category": "PHONE_NUMBER",
                "sub_categories": [
                    {"key_fields": [], "valid": {"datas": ["2344444444"]}}
                ],
            },
            {
                "category": "SLIDER_AMOUNT",
                "sub_categories": [{"key_fields": [], "valid": {"datas": ["11000"]}}],
            },
            {
                "category": "TEXT",
                "sub_categories": [
                    {"key_fields": [], "valid": {"datas": ["Ahasjdh", "Hljaldjs"]}}
                ],
            },
        ],
    },
]
