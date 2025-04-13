# Rakattack - OnkoMiner

![Rakattack Showcase](rakattack_showcase.gif)

Rakattack - OnkoMiner is a web application that helps medical professionals extract and validate structured data from Czech oncology medical records. The application uses Azure OpenAI to analyze medical text and automatically fill in required fields in a standardized format.

## Features

- **Text Analysis**: Upload or paste Czech medical text to automatically extract relevant information
- **Field Validation**: Validate specific fields with AI-powered suggestions
- **Required Fields Check**: Automatic validation of required fields in the medical record
- **Mock Data Support**: Test the application without Azure OpenAI credentials using sample data
- **Interactive UI**: User-friendly interface for reviewing and editing extracted data

## Project Structure

### Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with the following variables:
   ```
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
   AZURE_OPENAI_API_VERSION=2023-05-15
   AZURE_OPENAI_DEPLOYMENT=your_deployment_name_here
   FLASK_ENV=development
   ```

4. Replace the placeholder values with your actual Azure OpenAI credentials.

### Running the Application

Run the following command in the root directory:

```
python app.py
```

The application will be available at `http://localhost:5100/`.

### Requirements

- Python 3.8 or higher
- Flask
- OpenAI Python library
- Azure OpenAI API access 