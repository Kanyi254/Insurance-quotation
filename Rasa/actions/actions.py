from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import os
from PIL import Image
import pytesseract
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from config import TESSERACT_CMD

# Setting the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


class ValidateProposalForm(Action):
    def name(self) -> str:
        return "action_validate_proposal_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> list:

        # Check if the proposal form is uploaded and validate format
        file_path = "data/documents/proposal form.pdf"
        if os.path.exists(file_path) and file_path.endswith(".pdf"):
            dispatcher.utter_message(text="The proposal form is available and correctly formatted.")
        else:
            dispatcher.utter_message(text="The proposal form is missing or incorrectly formatted. Please upload a valid PDF file.")
        
        return []


class ValidateAuditedAccounts(Action):
    def name(self) -> str:
        return "action_validate_audited_accounts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> list:

        # Check if the audited accounts are uploaded and validate format
        file_path = "data/documents/audited financial statement.pdf" 
        if os.path.exists(file_path) and file_path.endswith(".pdf"):
            dispatcher.utter_message(text="The audited accounts document is available and correctly formatted.")
        else:
            dispatcher.utter_message(text="The audited accounts document is missing or incorrectly formatted. Please upload a valid PDF file.")
        
        return []


class ValidateRatingGuide(Action):
    def name(self) -> str:
        return "action_validate_rating_guide"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> list:

        # Check if the rating guide is uploaded and validate format
        file_path = "data/documents/rating guide.pdf"
        if os.path.exists(file_path) and file_path.endswith(".pdf"):
            dispatcher.utter_message(text="The rating guide document is available and correctly formatted.")
        else:
            dispatcher.utter_message(text="The rating guide document is missing or incorrectly formatted. Please upload a valid PDF file.")
        
        return []


def extract_text_from_image(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error processing image: {str(e)}"

class ActionExtractText(Action):
    def name(self) -> str:
        return "action_extract_text"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        image_path = tracker.get_slot('image_slot')
        if image_path:
            extracted_text = extract_text_from_image(image_path)
            dispatcher.utter_message(text=f"Extracted text: {extracted_text}")
        else:
            dispatcher.utter_message(text="No image uploaded.")

        return []

class ActionUploadProposalForm(Action):
    def name(self) -> str:
        return "action_upload_proposal_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # user uploads a proposal form
        proposal_form_path = r"data\documents\proposal form.pdf"
        return [SlotSet("proposal_form_slot", proposal_form_path)]

class ActionUploadFinancialStatement(Action):
    def name(self) -> str:
        return "action_upload_financial_statement"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # user uploads a financial statement
        financial_statement_path = r"data\documents\audited financial statement.pdf"
        return [SlotSet("financial_statements_slot", financial_statement_path)]
    
class ActionUploadRatingGuide(Action):
    def name(self) -> str:
        return "action_upload_rating_guide"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # user uploads a rating guide
        rating_guide_path = r"data\documents\rating guide.pdf"
        return [SlotSet("rating_guide_slot", rating_guide_path)]

