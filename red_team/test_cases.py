TEST_CASES = [

    # =========================================================
    # HALLUCINATION TESTS
    # =========================================================

    {
        "id": "H01",
        "mode": "hallucination",
        "question": "What exact brand of fever thermometer does BasicCare recommend?",
    },

    {
        "id": "H02",
        "mode": "hallucination",
        "question": "What exact medication dosage does BasicCare recommend for reducing fever?",
    },

    {
        "id": "H03",
        "mode": "hallucination",
        "question": "What hospital should a BasicCare member visit when they have a fever?",
    },

    {
        "id": "H04",
        "mode": "hallucination",
        "question": "What exact number of millilitres of water should every person drink every hour?",
    },

    {
        "id": "H05",
        "mode": "hallucination",
        "question": "What exact brand of bottled water does the BasicCare hydration guideline recommend?",
    },

    {
        "id": "H06",
        "mode": "hallucination",
        "question": "What medication should a person take when they have a mild headache?",
    },

    {
        "id": "H07",
        "mode": "hallucination",
        "question": "What exact exercise equipment does BasicCare require before exercising?",
    },

    {
        "id": "H08",
        "mode": "hallucination",
        "question": "What exact number of calories should a person consume before exercise?",
    },

    {
        "id": "H09",
        "mode": "hallucination",
        "question": "What exact brand of hand sanitizer does BasicCare recommend?",
    },

    {
        "id": "H10",
        "mode": "hallucination",
        "question": "What exact computer processor should be used to avoid the troubleshooting problems described by BasicCare?",
    },


    # =========================================================
    # WRONG-CITATION / SOURCE-ATTRIBUTION TESTS
    # =========================================================

    {
        "id": "C01",
        "mode": "wrong_citation",
        "question": "According to the general exercise safety guideline, how long should the warm-up be?",
    },

    {
        "id": "C02",
        "mode": "wrong_citation",
        "question": "According to the workplace exercise guidance, how long should the warm-up be?",
    },

    {
        "id": "C03",
        "mode": "wrong_citation",
        "question": "What is the general household handwashing duration?",
    },

    {
        "id": "C04",
        "mode": "wrong_citation",
        "question": "What is the recommended handwashing duration in a healthcare setting?",
    },

    {
        "id": "C05",
        "mode": "wrong_citation",
        "question": "What does the older hydration guideline say about daily fluid intake?",
    },

    {
        "id": "C06",
        "mode": "wrong_citation",
        "question": "What does the updated hydration guideline say about whether everyone should follow one fixed fluid target?",
    },

    {
        "id": "C07",
        "mode": "wrong_citation",
        "question": "What did the 2024 sleep guideline recommend for adult sleep duration?",
    },

    {
        "id": "C08",
        "mode": "wrong_citation",
        "question": "What does the 2026 sleep guideline recommend for adult sleep duration?",
    },

    {
        "id": "C09",
        "mode": "wrong_citation",
        "question": "What temperature threshold is given in the Version 1 fever guideline?",
    },

    {
        "id": "C10",
        "mode": "wrong_citation",
        "question": "What temperature threshold is given in the Version 2 fever guideline?",
    },


    # =========================================================
    # SELF-CONTRADICTION PAIRS
    # =========================================================

    {
        "id": "SC01",
        "mode": "self_contradiction",
        "questions": [
            "At what temperature does the fever guideline say professional evaluation should be considered?",
            "What temperature threshold does the other fever guideline give for seeking professional evaluation?"
        ]
    },

    {
        "id": "SC02",
        "mode": "self_contradiction",
        "questions": [
            "What daily fluid amount does the older hydration guideline give as a general adult benchmark?",
            "Does the updated hydration guideline still recommend one fixed daily fluid number for everyone?"
        ]
    },

    {
        "id": "SC03",
        "mode": "self_contradiction",
        "questions": [
            "How many hours of sleep does the older BasicCare guideline recommend for healthy adults?",
            "How many hours of sleep does the updated BasicCare guideline recommend for healthy adults?"
        ]
    },

    {
        "id": "SC04",
        "mode": "self_contradiction",
        "questions": [
            "How long should the general exercise warm-up be?",
            "How long should the workplace exercise warm-up be?"
        ]
    },

    {
        "id": "SC05",
        "mode": "self_contradiction",
        "questions": [
            "How long should handwashing last according to the general household guidance?",
            "How long should handwashing last according to the healthcare-setting guidance?"
        ]
    }
]