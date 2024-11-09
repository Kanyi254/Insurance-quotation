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
        number_partners_principal = tracker.get_slot('number_partners_principal')
        number_qualified_assistants = tracker.get_slot('number_qualified_assistants')
        number_unqualified_assistants = tracker.get_slot('number_unqualified_assistants')
        number_other_staff = tracker.get_slot('number_other_staff')
        indemnity_amount = tracker.get_slot('indemnity_amount')
        extensions = tracker.get_slot('extensions')
        loss_of_documents = tracker.get_slot('loss_of_documents')
        dishonest_employees = tracker.get_slot('dishonest_employees')
        incoming_outgoing_partners = tracker.get_slot('incoming_outgoing_partners')
        breach_of_authority = tracker.get_slot('breach_of_authority')
        libel_and_slander = tracker.get_slot('libel_and_slander')

        # Calculate Staff Fee
        staff_fee = (number_partners_principal * 3600) + (number_qualified_assistants * 3000) + (number_unqualified_assistants * 2000) + (number_other_staff * 1000)

        # Calculate Annual Fee based on Indemnity Amount
        if indemnity_amount < 1000000:
            annual_fee = indemnity_amount * 0.0105
        elif indemnity_amount <= 2000000:
            annual_fee = indemnity_amount * 0.0075
        elif indemnity_amount <= 5000000:
            annual_fee = indemnity_amount * 0.0045
        elif indemnity_amount <= 10000000:
            annual_fee = indemnity_amount * 0.0035
        elif indemnity_amount <= 20000000:
            annual_fee = indemnity_amount * 0.00225
        else:
            annual_fee = indemnity_amount * 0.00125

        # Calculate A
        A = staff_fee + annual_fee

        # Calculate Limit of Indemnity
        if indemnity_amount < 1000000:
            limit_of_indemnity = indemnity_amount
        elif indemnity_amount <= 2500000:
            limit_of_indemnity = indemnity_amount * 1.5
        elif indemnity_amount <= 5000000:
            limit_of_indemnity = indemnity_amount * 1.9
        elif indemnity_amount <= 10000000:
            limit_of_indemnity = indemnity_amount * 2.3
        elif indemnity_amount <= 20000000:
            limit_of_indemnity = indemnity_amount * 2.75
        elif indemnity_amount <= 40000000:
            limit_of_indemnity = indemnity_amount * 3.25
        elif indemnity_amount <= 60000000:
            limit_of_indemnity = indemnity_amount * 3.65
        else:
            limit_of_indemnity = indemnity_amount * 4.5

        # Calculate B
        B = limit_of_indemnity

        # Calculate Profession Fee
        if business_profession in ["estate agents", "valuers", "property consultants", "accountant", "attorney", "auditor", "optician", "chemist", "tax-advisors", "actuaries"]:
            profession_fee = B
        elif business_profession in ["architect", "civil engineer", "construction engineer", "quantity surveyors", "land surveyors"]:
            profession_fee = B * 1.35
        else:  # for optician, chemist, surgeon, veterinary surgeon, doctor, dentist, hospital
            profession_fee = B * 1.75

        # Calculate C
        C = profession_fee

        # Calculate Basic Premium
        basic_premium = A + B + C

        # Calculate Extensions Fee
        extensions_fee = 0
        if loss_of_documents or dishonest_employees or incoming_outgoing_partners or breach_of_authority or libel_and_slander:
            extensions_fee = basic_premium * 0.10 * (
                (loss_of_documents == 'yes') + (dishonest_employees == 'yes') +
                (incoming_outgoing_partners == 'yes') + (breach_of_authority == 'yes') +
                (libel_and_slander == 'yes')
            )

        # Calculate Comprehensive Premium
        comprehensive_premium = basic_premium + extensions_fee

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
            "extensions_fee": extensions_fee,
            "comprehensive_premium": comprehensive_premium,
            "levies_fee": levies_fee,
            "total_premium": total_premium
        }

        # Generate PDF quote (you can use any library like ReportLab to generate PDF)
        # For simplicity, a basic text response can be used here
        pdf_content = f"Reinsured Company: {tracker.get_slot('name_reinsured')}\n"
        pdf_content += f"Broker: {tracker.get_slot('name_broker')}\n"
        pdf_content += f"Reinsured: {tracker.get_slot('name_insured')}:\n"
        pdf_content += f"Total Premium: {total_premium}"

        # Send the quote as a message (you can later send the PDF file instead)
        dispatcher.utter_message(text=pdf_content)

        return []



# class ActionCheckSlotsFilled(Action):

#     def name(self) -> str:
#         return "action_check_slots_filled"

#     def run(self, dispatcher: CollectingDispatcher, tracker, domain):

#         # List of required slots
#         required_slots = [
#             "business_profession",
#             "name_reinsured",
#             "name_broker",
#             "name_insured",
#             "number_partners_principal",
#             "number_qualified_assistants",
#             "number_unqualified_assistants",
#             "number_other_staff",
#             "indemnity_amount",
#             "excess_amount",
#             "extensions"
#             "loss_of_documents",
#             "dishonest_employees",
#             "incoming_outgoing_partners",
#             "breach_of_authority",
#             "libel_and_slander"
#         ]
        
#         # Check for missing slots
#         missing_slots = []
#         for slot in required_slots:
#             if tracker.get_slot(slot) is None:
#                 missing_slots.append(slot)

#         # If any slots are missing, prompt the user to fill them
#         if missing_slots:
#             missing_slots_str = ", ".join(missing_slots)
#             dispatcher.utter_message(text=f"Please provide the following information: {missing_slots_str}.")
#             return []  # Don't proceed with the next action until slots are filled

#         # If all slots are filled, proceed to generate the quote
#         dispatcher.utter_message(text="All required information is provided. Generating your quote now.")
#         return [SlotSet("all_slots_filled", True)]  # Optionally set a slot to indicate all are filled


# class ActionValidateInsuranceForm(Action):
#     def name(self) -> Text:
#         return "validate_insurance_form"

#     def validate_number_partners_principal(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         if slot_value >= 1.0:
#             return {"number_partners_principal": slot_value}
#         else:
#             dispatcher.utter_message(text="The number of partners/principals should be at least 1.")
#             return {"number_partners_principal": None}

#     def validate_number_qualified_assistants(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         if slot_value >= 1.0:
#             return {"number_qualified_assistants": slot_value}
#         else:
#             dispatcher.utter_message(text="The number of qualified assistants should be at least 1.")
#             return {"number_qualified_assistants": None}

#     def validate_number_unqualified_assistants(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         if slot_value >= 0.0:
#             return {"number_unqualified_assistants": slot_value}
#         else:
#             dispatcher.utter_message(text="The number of unqualified assistants cannot be negative.")
#             return {"number_unqualified_assistants": None}

#     def validate_number_other_staff(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         if slot_value >= 0.0:
#             return {"number_other_staff": slot_value}
#         else:
#             dispatcher.utter_message(text="The number of other staff cannot be negative.")
#             return {"number_other_staff": None}

#     def validate_indemnity_amount(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> Dict[Text, Any]:
#         if slot_value >= 1:
#             return {"indemnity_amount": slot_value}
#         else:
#             dispatcher.utter_message(text="The indemnity amount should be at least 1.")
#             return {"indemnity_amount": None}