import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import json
from app.controllers.openai_controller import OpenAIController

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")

REQUIRED_FIELDS = {
    "administrativni_udaje": {"identifikator_pacienta": True, "uredni_pohlavi": True},
    "modul_a_pacient_parametry": {
        "relevantni_faktory_v_anamneze_pacienta": True,
        "nadorovy_predispozicni_syndrom": {
            "nazev_predispozicniho_syndromu": True,
            "jiny_predispozicni_syndrom": True,
        },
        "relevantni_komorbidity_a_stav_pacienta": {
            "zavazne_onemocneni_srdce_a_cev": True,
            "zavazne_metabolicke_onemocneni": True,
            "zavazne_plicni_onemocneni": True,
            "zavazne_onemocneni_git": True,
            "zavazne_onemocneni_ledvin": True,
            "autoimunitni_onemocneni": True,
            "zavazne_endokrinologicke_onemocneni": True,
            "neuropsychiatricke_onemocneni": True,
            "gynekologicke_onemocneni_anamneza": True,
            "zavazne_onemocneni_infeccni": True,
            "organova_transplantace": True,
            "organ": True,
        },
        "predchozi_onkologicke_onemocneni": {"predchozi_onkologicke_onemocneni": True},
        "onkologicky_screening": {
            "mamograficky_screening": True,
            "screening_nadoru_delozniho_hrdla": True,
            "screening_kolorektalniho_karcinomu": True,
            "plicni_screening": True,
            "screening_prostaty": True,
        },
        "alergie": {
            "lekova_alergie": True,
            "alergia_na_jod_kontrastni_latky": True,
            "jine_alergie": True,
        },
        "abusus": {"koureni": True, "alkohol": True},
        "antropometricke_udaje": {"datum_mereni": True, "vyska": True, "hmotnost": True},
        "celkovy_stav_pacienta": {},
        "performance_status_ecog": {"performance_status_ecog": True, "datum_hodnoceni": True},
        "karnofskeho_index_ki": {"opatreni_k_zachovani_plodnosti_pred_onkologickou_lecbou": True},
        "opatreni_zachovani_plodnosti_pred_onkologickou_lecbou": {"typ_opatreni": True},
    },
    "modul_b_cast_b1": {
        "modul_b_diagnostika_cast_b1_obecne_parametry_popisujici_onkologickou_diagnozu_spolecne_vsemdiagnozam": True,
        "poradove_cislo_onkologicke_diagnozy_pacienta": True,
        "klasifikace_nadoru": {
            "datum_stanoveni_definitivni_diagnozy": True,
            "diagnoza_slovne": True,
            "diagnoza_kod_mkn": True,
            "lateralita": True,
            "topografie": True,
        },
        "diagnosticka_skupina": {"vyber_diagnosticke_skupiny": True},
    },
    "modulc_dospelionk_pac": {
        "modulc_souhrn_provedene_onkologicke_lecby_v_koc_odpoved_na_lecbu_a_relevantni_toxicita": True,
        "chirurgicka_lecba": {"datum_operace": True, "makroskopicke_rezidum_nadoru_r2": True},
        "radioterapie": {
            "datum_zahajeni_serie": True,
            "zevni_radioterapie": True,
            "brachyterapie": True,
        },
        "cilena_lecba": {"datum_zahajeni": True, "rezim": True},
        "hormonoterapie": {"datum_zahajeni": True, "rezim": True},
        "imunoterapie": {"datum_zahajeni": True, "rezim": True},
        "cytokinova_terapie": {"datum_zahajeni": True, "rezim": True},
        "jine_lecebne_modality_v_ramci_onkologicke_lecby": {
            "datum_zahajeni": True,
            "jina_lecba": True,
        },
        "presetreni": {"datum_hodnoceni_lecebne_odpovedi": True, "hodnoceni_lecebne_odpoved": True},
        "zavazna_toxicita_onkologicke_lecby_relevantni_prosledujici_peci": {"nazev": True},
    },
}

# Initialize controller based on environment variables
use_mock = os.getenv("USE_MOCK", "false").lower() == "true"

if use_mock:
    from app.controllers.mock_controller import MockOpenAIController

    controller = MockOpenAIController()
    print("Using mock OpenAI controller for testing")
else:
    # Check for required Azure OpenAI environment variables
    required_vars = ["AZURE_OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Warning: Missing required environment variables: {', '.join(missing_vars)}")
        print("Falling back to mock controller")
        from app.controllers.mock_controller import MockOpenAIController

        controller = MockOpenAIController()
    else:
        # Define controller as a broader type (any object with process_medical_text method)
        controller = OpenAIController()  # type: ignore
        print("Using Azure OpenAI controller")


@app.route("/")
def index():
    """Render the main page"""
    return render_template("index.html")


@app.route("/api/process", methods=["POST"])
def process_text():
    """Process text using OpenAI controller"""
    data = request.json

    text = data.get("text", "")

    if not text:
        return jsonify({"success": False, "error": "No text provided"}), 400

    result = controller.process_medical_text(text)

    # If success, validate required fields
    if result.get("success"):
        try:
            # Parse the response data
            parsed_data = json.loads(result["data"])

            # Check for missing required fields
            missing_fields = validate_required_fields(parsed_data, REQUIRED_FIELDS)

            # Add missing fields information to the response
            if missing_fields:
                result["missing_required_fields"] = missing_fields
        except json.JSONDecodeError:
            # If JSON parsing fails, continue with original result
            pass

    return jsonify(result)


@app.route("/api/validate", methods=["POST"])
def validate_field():
    """Validate a specific field using OpenAI with validation prompt"""
    # get the data
    data = request.json
    text = data.get("text", "")
    field = data.get("field", "")

    print(f"Looking for field: {field}")

    validation_prompt = f"""
        You are a medical expert specializing in oncology medical records, particularly Czech cancer treatment reports.
        Your task is to analyze the given medical text and suggest possible values for a specific missing field in the medical record. The field name will be provided along with the full medical text.
        The validation reason should be written in Czech language.
        The field you are validating has the following name: {field}
    """

    controller = OpenAIController()
    try:
        response = controller.client.chat.completions.create(
            temperature=0.7,
            max_tokens=500,
            model=controller.deployment_name,
            messages=[
                {"role": "system", "content": validation_prompt},
                {"role": "user", "content": text},
            ],
        )

        return jsonify({"success": True, "suggestion": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


def validate_required_fields(data, required_fields, path=""):
    """
    Recursively validate that all required fields are present and not null
    Returns a list of missing field paths
    """
    missing = []

    for key, value in required_fields.items():
        current_path = f"{path}.{key}" if path else key

        # Check if the key exists in data
        if key not in data:
            missing.append(current_path)
            continue

        # If the data value is null or "null" string
        if data[key] is None or data[key] == "null":
            missing.append(current_path)
            continue

        # If value is a dict, recurse into it
        if isinstance(value, dict) and isinstance(data[key], dict):
            nested_missing = validate_required_fields(data[key], value, current_path)
            missing.extend(nested_missing)

        # If value is a set (list of required fields), check if all are present
        elif isinstance(value, set):
            for req_field in value:
                if (
                    req_field not in data[key]
                    or data[key][req_field] is None
                    or data[key][req_field] == "null"
                ):
                    missing.append(f"{current_path}.{req_field}")

    return missing


if __name__ == "__main__":
    app.run(debug=True, port=5100)
