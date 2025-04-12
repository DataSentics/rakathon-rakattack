import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")

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

        controller = OpenAIController()
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
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5100)
