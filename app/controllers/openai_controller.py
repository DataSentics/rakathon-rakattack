import os
from openai import AzureOpenAI
from app.prompts.medical_text_prompt import custom_prompt


class OpenAIController:
    def __init__(self):
        # Initialize Azure OpenAI client with only supported parameters
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2025-01-01-preview",
            azure_endpoint="https://rakathon-openai.openai.azure.com",
        )

        self.deployment_name = "gpt-4o"

    def process_medical_text(self, text):
        """Process medical text using Azure OpenAI with a custom prompt"""

        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": custom_prompt},
                    {"role": "user", "content": text},
                ],
                response_format={"type": "json_object"},
            )
            print(response.choices[0].message.content)

            return {"success": True, "data": response.choices[0].message.content}
        except Exception as e:
            return {"success": False, "error": str(e)}
