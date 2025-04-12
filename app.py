import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")

REQUIRED_FIELDS = {
    "administrativni_udaje": {
        "identifikator_pacienta",
        "komunikacni_jazyk"
    },
    "modul_a_pacient_parametry": {
        "onkologicky_suspektni_rodinna_anamneza":{
            "pribuzensky_stav"
        }
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
        from app.controllers.openai_controller import OpenAIController

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
