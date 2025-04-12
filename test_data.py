"""
Test script to generate a sample response from OpenAI.
This can be used to test the frontend without needing actual Azure OpenAI credentials.
"""

import json
import sys

SAMPLE_MEDICAL_TEXT = """
Patient ID: 1234567890
Admission Date: 2023-05-15
Discharge Date: 2023-05-20

Chief Complaint: 
65-year-old male with severe chest pain radiating to the left arm.

Medical History:
- Hypertension (diagnosed 2010)
- Type 2 Diabetes (diagnosed 2015)
- Hyperlipidemia
- Previous MI in 2019

Medications:
- Metformin 500mg BID
- Lisinopril 10mg daily
- Atorvastatin 40mg daily
- Aspirin 81mg daily

Allergies:
- Penicillin (hives)
- Sulfa drugs (rash)

Physical Examination:
Vitals: BP 160/95, HR 88, RR 18, Temp 37.1°C, O2 Sat 94% on RA
General: Alert, oriented, in moderate distress
CV: Regular rate and rhythm, S1 and S2 normal, S4 present, 2/6 systolic murmur at apex
Resp: Clear to auscultation bilaterally
Abd: Soft, non-tender, non-distended

Laboratory Results:
- Troponin I: 2.3 ng/mL (elevated)
- CK-MB: 15 ng/mL (elevated)
- BNP: 450 pg/mL (elevated)
- CBC: WBC 10.5, Hgb 13.2, Plt 230
- Chem7: Na 138, K 4.2, Cl 101, CO2 24, BUN 22, Cr 1.1, Glucose 170

Diagnostic Studies:
- ECG: ST-segment elevation in leads II, III, aVF
- Chest X-ray: No acute cardiopulmonary process
- Echocardiogram: EF 40%, inferolateral wall hypokinesis

Assessment:
1. Acute ST-elevation myocardial infarction (STEMI)
2. Hypertension, uncontrolled
3. Type 2 Diabetes Mellitus
4. Hyperlipidemia

Plan:
1. Emergent cardiac catheterization
2. Dual antiplatelet therapy with aspirin and clopidogrel
3. Heparin drip
4. Beta-blocker therapy
5. Adjustment of antihypertensive regimen
6. Cardiology consultation
7. Diabetes management

Follow-up:
Cardiology clinic in 2 weeks (2023-06-05)
"""

SAMPLE_RESPONSE = {
    "patientID": "1234567890",
    "dates": {
        "admission": "2023-05-15",
        "discharge": "2023-05-20",
        "followUp": "2023-06-05",
        "diagnosisHistory": [
            {"condition": "Hypertension", "date": "2010"},
            {"condition": "Type 2 Diabetes", "date": "2015"},
            {"condition": "Previous MI", "date": "2019"},
        ],
    },
    "medicalConditions": {
        "chiefComplaint": "severe chest pain radiating to the left arm",
        "currentDiagnosis": "Acute ST-elevation myocardial infarction (STEMI)",
        "otherConditions": [
            "Hypertension, uncontrolled",
            "Type 2 Diabetes Mellitus",
            "Hyperlipidemia",
        ],
        "position": {"start": 120, "end": 175},
    },
    "treatments": {
        "planned": [
            "Emergent cardiac catheterization",
            "Dual antiplatelet therapy",
            "Heparin drip",
            "Beta-blocker therapy",
            "Adjustment of antihypertensive regimen",
            "Cardiology consultation",
            "Diabetes management",
        ],
        "position": {"start": 1157, "end": 1353},
    },
    "medications": {
        "current": [
            "Metformin 500mg BID",
            "Lisinopril 10mg daily",
            "Atorvastatin 40mg daily",
            "Aspirin 81mg daily",
        ],
        "newPrescriptions": ["clopidogrel", "Heparin"],
        "position": {"start": 289, "end": 377},
    },
    "diagnosticResults": {
        "laboratory": {
            "cardiac": {
                "Troponin I": "2.3 ng/mL (elevated)",
                "CK-MB": "15 ng/mL (elevated)",
                "BNP": "450 pg/mL (elevated)",
            },
            "position": {"start": 759, "end": 849},
        },
        "ecg": "ST-segment elevation in leads II, III, aVF",
        "imaging": {
            "chestXRay": "No acute cardiopulmonary process",
            "echocardiogram": "EF 40%, inferolateral wall hypokinesis",
        },
        "position": {"start": 943, "end": 1053},
    },
}


def main():
    """Print the sample text and response for testing."""
    if len(sys.argv) > 1 and sys.argv[1] == "text":
        print(SAMPLE_MEDICAL_TEXT)
    else:
        print(json.dumps(SAMPLE_RESPONSE, indent=2))


if __name__ == "__main__":
    main()
