from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker
from rasa_sdk.forms import ValidationAction
from rasa_sdk.events import ActionExecuted, UserUtteranceReverted
from rasa_sdk.forms import FormValidationAction
from typing import Any, Dict, Text, List
from rasa.shared.core.events import Event

class ActionGenerateQuote(Action):

    def name(self) -> str:
        return "action_generate_quote"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):

        # Retrieve slot values
        business_profession = tracker.get_slot('business_profession')

        # Business profession check
        if business_profession in ["Directors and Officers Liability", "Insurance Brokers", "Reinsurance Brokers", "Investment Advisors",
                                   "Computer Bureaus", "Consultants", "Advertising Agents", "Shipping and Forwarding Custom Agents",
                                   "Foreign activities of Multi-National Accountants", "Project Managers", "Plastic Surgery and Blood Banks",
                                   "F & O in respect of Hospital Administrators", "Medical and Biological Research Facilities",
                                   "Genetic damage connected with X-ray and other radiation equipment"]:
            dispatcher.utter_message(text="Sorry, we do not offer insurance solutions for your business profession. How else may I help you?")
            return []

        # Proceed with the quote generation logic if business profession is valid

        # Retrieve other slot values
        name_reinsured = tracker.get_slot('name_reinsured')
        name_broker = tracker.get_slot('name_broker')
        name_insured = tracker.get_slot('name_insured')
        number_partners_principal = int(tracker.get_slot('number_partners_principal'))
        number_qualified_assistants = int(tracker.get_slot('number_qualified_assistants'))
        number_unqualified_assistants = int(tracker.get_slot('number_unqualified_assistants'))
        number_other_staff = int(tracker.get_slot('number_other_staff'))
        indemnity_amount = int(tracker.get_slot('indemnity_amount'))

        # Calculate Staff Fee
        staff_fee = (number_partners_principal * 3600) + (number_qualified_assistants * 3000) + (number_unqualified_assistants * 2000) + (number_other_staff * 1000)

        # Calculate Annual Fee based on Indemnity Amount
        if indemnity_amount < 1000000:
            annual_fee = indemnity_amount * 0.0105
        elif 1000000 <= indemnity_amount <= 2000000:
            annual_fee = indemnity_amount * 0.0075
        elif 2000001 <= indemnity_amount <= 5000000:
            annual_fee = indemnity_amount * 0.0045
        elif 5000001 <= indemnity_amount <= 10000000:
            annual_fee = indemnity_amount * 0.0035
        elif 10000001 <= indemnity_amount <= 20000000:
            annual_fee = indemnity_amount * 0.00225
        else:
            annual_fee = indemnity_amount * 0.00125

        # Calculate A
        A = staff_fee + annual_fee

        # Calculate Limit of Indemnity
        if indemnity_amount < 1000000:
            limit_of_indemnity = indemnity_amount
        elif 1000001 <= indemnity_amount <= 2500000:
            limit_of_indemnity = indemnity_amount * 0.035
        elif 2500001 <= indemnity_amount <= 5000000:
            limit_of_indemnity = indemnity_amount * 0.039
        elif 5000001 <= indemnity_amount <= 10000000:
            limit_of_indemnity = indemnity_amount * 0.043
        elif 10000001 <= indemnity_amount <= 20000000:
            limit_of_indemnity = indemnity_amount * 0.0475
        elif 20000001 <= indemnity_amount <= 40000000:
            limit_of_indemnity = indemnity_amount * 0.0525
        elif 40000001 <= indemnity_amount <= 60000000:
            limit_of_indemnity = indemnity_amount * 0.0565
        else:
            limit_of_indemnity = indemnity_amount * 0.065

        # Calculate B
        B = limit_of_indemnity

        # Calculate Profession Fee
        if business_profession in ["Estate Agents", "Valuers", "Property Consultants", "Accountant", "Attorney", "Auditor", "Optician", "Chemist", "Tax-Advisors", "Actuaries"]:
            profession_fee = B
        elif business_profession in ["Architect", "Civil Engineer", "Construction Engineer", "Quantity Surveyors", "Land Surveyors"]:
            profession_fee = B * 1.35
        else: # business_profession in ["Optician", "Chemist", "Surgeon", "Veterinary Surgeon", "Doctor", "Dentist", "Hospital"] 
            profession_fee = B * 1.75

        # Calculate C
        C = profession_fee

        # Calculate Basic Premium
        basic_premium = A + B + C

        # Calculate Comprehensive Premium
        comprehensive_premium = basic_premium

        # Calculate Levies Fee
        levies_fee = comprehensive_premium * 0.005

        # Calculate Total Premium
        total_premium = comprehensive_premium + levies_fee

        # Save responses
        responses = {
            "staff_fee": staff_fee,
            "annual_fee": annual_fee,
            "A": A,
            "limit_of_indemnity": limit_of_indemnity,
            "B": B,
            "profession_fee": profession_fee,
            "C": C,
            "basic_premium": basic_premium,
            "comprehensive_premium": comprehensive_premium,
            "levies_fee": levies_fee,
            "total_premium": total_premium
        }

        # Generate PDF quote 
        pdf_content = f"Reinsured Company: {tracker.get_slot('name_reinsured')}\n"
        pdf_content += f"Broker: {tracker.get_slot('name_broker')}\n"
        pdf_content += f"Insured: {tracker.get_slot('name_insured')}:\n"
        pdf_content += f"Total Premium Payable: {total_premium}"

        # Send the quote as a message
        dispatcher.utter_message(text=pdf_content)

        return []
