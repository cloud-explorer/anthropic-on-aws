import json
from utils.constants import ModelIDs
from utils.bedrockutility import BedrockUtils

class ApplicationValidator:
    def __init__(self):
        self.haiku_bedrock_utils = BedrockUtils(model_id=ModelIDs.anthropic_claude_3_haiku)

    def check_required_documents(self, input_data):
        """Check for required documents"""
        return self._check_required_documents(input_data['classified_documents'])

    def reject_incomplete_application(self, input_data):
        """Reject incomplete application"""
        return self._reject_incomplete_application(input_data['missing_documents'])

    def _check_required_documents(self, classified_documents):
        """
        Check if all required documents are present.
        """
        keys_list = []
        if 'classified_documents' in classified_documents:
            keys_list = [doc["category"] for doc in classified_documents["classified_documents"]]
        else:
            keys_list = {doc["category"] for doc in classified_documents}
        
        required_documents = ["URLA", "DRIVERS_LICENSE"]

        missing_documents = [doc for doc in required_documents if doc not in keys_list]
        
        if not missing_documents:
            return []
        else:
            return missing_documents

    def _reject_incomplete_application(self, missing_documents):
        """
        Generate a rejection message for incomplete applications.
        """
        if not missing_documents:
            return []
        missing_docs = ", ".join(missing_documents)
        message_list = [
            {
                "role": "user",
                "content": [
                    {"text": f"These documents are missing {missing_docs}. Write a note asking for additional documentation?"}
                ]
            }
        ]
        system_message = [
            {"text": "<task>You are a mortgage agent. Your main task is to write notes to users asking for missing documentation</task>"}
        ]
        
        response = self.haiku_bedrock_utils.invoke_bedrock(message_list=message_list, system_message=system_message)
        return [response['output']['message']]
