"""
Mock controller for testing the frontend without actual Azure OpenAI API access.
"""

import json
import time
import sys
import os

# Add the project root to the Python path to properly import test_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from test_data import SAMPLE_RESPONSE


class MockOpenAIController:
    """A mock version of the OpenAI controller for testing."""

    def process_medical_text(self, text):
        """Process medical text and return a mock response."""
        # Simulate processing delay
        # time.sleep(1.5)

        try:
            # Return the sample response
            return {"success": True, "data": json.dumps(SAMPLE_RESPONSE)}
        except Exception as e:
            return {"success": False, "error": str(e)}
