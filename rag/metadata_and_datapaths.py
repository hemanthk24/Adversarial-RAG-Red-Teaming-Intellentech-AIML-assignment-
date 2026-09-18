DOCUMENT_METADATA = [
    {
        "doc_id": "D01",
        "filename": "D01_Fever_Guidelines_v1.txt",
        "title": "BasicCare Fever & Temperature Guidelines",
        "version": "1.0",
        "effective_date": "2023-03-01",
        "topic": "fever"
    },
    {
        "doc_id": "D02",
        "filename": "D02_Fever_Guidelines_v2.txt",
        "title": "BasicCare Fever & Temperature Guidelines",
        "version": "2.0",
        "effective_date": "2025-01-01",
        "topic": "fever"
    },
    {
        "doc_id": "D03",
        "filename": "D03_Hydration_Guidelines_v1.txt",
        "title": "BasicCare Hydration Guidelines",
        "version": "1.0",
        "effective_date": "2024-02-01",
        "topic": "hydration"
    },
    {
        "doc_id": "D04",
        "filename": "D04_Hydration_Guidelines_v2.txt",
        "title": "BasicCare Hydration Guidelines",
        "version": "2.0",
        "effective_date": "2026-04-01",
        "topic": "hydration"
    },
    {
        "doc_id": "D05",
        "filename": "D05_Minor_Burn_Care_v1.txt",
        "title": "BasicCare Minor Burn Care Guidelines",
        "version": "1.0",
        "effective_date": "2023-05-01",
        "topic": "burn_care"
    },
    {
        "doc_id": "D06",
        "filename": "D06_Minor_Burn_Care_v2.txt",
        "title": "BasicCare Minor Burn Care Guidelines",
        "version": "2.0",
        "effective_date": "2025-06-01",
        "topic": "burn_care"
    },
    {
        "doc_id": "D07",
        "filename": "D07_Sleep_Guidelines_2024.txt",
        "title": "BasicCare Sleep Guidelines",
        "version": "1.0",
        "effective_date": "2024-01-01",
        "topic": "sleep"
    },
    {
        "doc_id": "D08",
        "filename": "D08_Sleep_Guidelines_2026.txt",
        "title": "BasicCare Sleep Guidelines",
        "version": "2.0",
        "effective_date": "2026-01-01",
        "topic": "sleep"
    },
    {
        "doc_id": "D09",
        "filename": "D09_Exercise_Safety_General.txt",
        "title": "BasicCare General Exercise Safety Guidelines",
        "version": "1.0",
        "effective_date": "2024-01-01",
        "topic": "exercise_safety_general"
    },
    {
        "doc_id": "D10",
        "filename": "D10_Exercise_Safety_Workplace.txt",
        "title": "BasicCare Workplace Exercise Safety Guidelines",
        "version": "1.0",
        "effective_date": "2024-01-01",
        "topic": "exercise_safety_workplace"
    },
    {
        "doc_id": "D11",
        "filename": "D11_Hand_Hygiene_General.txt",
        "title": "BasicCare General Hand Hygiene Guidelines",
        "version": "1.0",
        "effective_date": "2023-01-01",
        "topic": "hand_hygiene_general"
    },
    {
        "doc_id": "D12",
        "filename": "D12_Hand_Hygiene_Healthcare.txt",
        "title": "BasicCare Clinic Hand Hygiene Guidelines",
        "version": "1.0",
        "effective_date": "2023-01-01",
        "topic": "hand_hygiene_clinic"
    },
    {
        "doc_id": "D13",
        "filename": "D13_Headache_Rest_Guidelines.txt",
        "title": "BasicCare Headache & Rest Guidelines",
        "version": "1.0",
        "effective_date": "2024-01-01",
        "topic": "headache"
    },
    {
        "doc_id": "D14",
        "filename": "D14_Common_Cold_Self_Care.txt",
        "title": "BasicCare Common Cold & Self-Care Guidelines",
        "version": "1.0",
        "effective_date": "2024-01-01",
        "topic": "common_cold"
    },
    {
        "doc_id": "D15",
        "filename": "D15_Photography_Basics.txt",
        "title": "Photography Basics Handbook",
        "version": "1.0",
        "effective_date": "2024-01-01",
        "topic": "photography"
    },
    {
        "doc_id": "D16",
        "filename": "D16_Computer_Troubleshooting.txt",
        "title": "Basic Computer Troubleshooting Guide",
        "version": "1.0",
        "effective_date": "2024-01-01",
        "topic": "computer_troubleshooting"
    },
]

# datapaths for documents and metadata
from pathlib import Path

DOCUMENTS_DIR = Path("data") / "Documents"

DATA_DIR = [
    DOCUMENTS_DIR / "D01_Fever_Guidelines_v1.txt",
    DOCUMENTS_DIR / "D02_Fever_Guidelines_v2.txt",
    DOCUMENTS_DIR / "D03_Hydration_Guidelines_v1.txt",
    DOCUMENTS_DIR / "D04_Hydration_Guidelines_v2.txt",
    DOCUMENTS_DIR / "D05_Minor_Burn_Care_v1.txt",
    DOCUMENTS_DIR / "D06_Minor_Burn_Care_v2.txt",
    DOCUMENTS_DIR / "D07_Sleep_Guidelines_2024.txt",
    DOCUMENTS_DIR / "D08_Sleep_Guidelines_2026.txt",
    DOCUMENTS_DIR / "D09_Exercise_Safety_General.txt",
    DOCUMENTS_DIR / "D10_Exercise_Safety_Workplace.txt",
    DOCUMENTS_DIR / "D11_Hand_Hygiene_General.txt",
    DOCUMENTS_DIR / "D12_Hand_Hygiene_Healthcare.txt",
    DOCUMENTS_DIR / "D13_Headache_Rest_Guidelines.txt",
    DOCUMENTS_DIR / "D14_Common_Cold_Self_Care.txt",
    DOCUMENTS_DIR / "D15_Photography_Basics.txt",
    DOCUMENTS_DIR / "D16_Computer_Troubleshooting.txt",
]

