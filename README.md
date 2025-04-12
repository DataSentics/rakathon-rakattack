# Medical Text Analysis Web App

A simple web application that uses Azure OpenAI to analyze medical text and present the results in an interactive manner.

## Features

- Single page application with two screens
- Processes medical text using Azure OpenAI API
- Displays structured information extracted from medical text
- Interactive timeline visualization
- Hover over extracted information to highlight relevant text
- Responsive design using Bootstrap

## Setup

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

## Running the Application

Run the following command in the root directory:

```
python app.py
```

The application will be available at `http://localhost:5000/`.

## Usage

1. Enter or paste medical text in the input field on the first screen
2. Click the "Process" button to analyze the text
3. View the analysis results on the second screen
4. Hover over the key-value pairs to highlight the corresponding text
5. Use the "Back to Input" button to return to the first screen

## Requirements

- Python 3.8 or higher
- Flask
- OpenAI Python library
- Azure OpenAI API access 