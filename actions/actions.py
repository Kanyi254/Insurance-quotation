from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher  
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction


class ActionCalculatePremium(Action):
    def name(self) -> Text:
        return "action_calculate_premium"

    def run(self, dispatcher, tracker, domain):
        # Retrieve required slots
        company_name = tracker.get_slot("company")
        base_premium = tracker.get_slot("base_premium")
        annual_fees = tracker.get_slot("annual_fees")
        limit_of_indemnity = tracker.get_slot("limit_of_indemnity")
        profession = tracker.get_slot("profession")
        partners = tracker.get_slot("partners")
        qualified_assistants = tracker.get_slot("qualified_assistants")
        unqualified_assistants = tracker.get_slot("unqualified_assistants")
        others = tracker.get_slot("others")
        profit_status = tracker.get_slot("profit_status")
        
        # Ensure that base premium is filled and positive
        if not base_premium or base_premium <= 1:
            dispatcher.utter_message(
                text="The base premium must be a positive number greater than 1. Please provide a valid base premium."
            )
            return [SlotSet("base_premium", None)]
        
        # Ensure profit status is "yes"
        if profit_status != "yes":
            dispatcher.utter_message(
                text="The company must be making a profit to calculate the premium."
            )
            return []
        
        try:
            base_premium = float(base_premium)

            # Calculate Annual Fees Premium
            annual_fees = float(annual_fees)
            annual_fee_premium = base_premium * (0.0105 if annual_fees <= 1_000_000 else 
                                                 0.0075 if annual_fees <= 2_000_000 else 
                                                 0.0045 if annual_fees <= 5_000_000 else 
                                                 0.0035 if annual_fees <= 10_000_000 else 
                                                 0.00225 if annual_fees <= 20_000_000 else 
                                                 0.00125)

            # Calculate Limit of Indemnity Premium
            limit_of_indemnity = float(limit_of_indemnity)
            indemnity_premium = base_premium * (1.00 if limit_of_indemnity <= 1_000_000 else 
                                                1.50 if limit_of_indemnity <= 2_500_000 else 
                                                1.90 if limit_of_indemnity <= 5_000_000 else 
                                                2.30 if limit_of_indemnity <= 10_000_000 else 
                                                2.75 if limit_of_indemnity <= 20_000_000 else 
                                                3.25 if limit_of_indemnity <= 40_000_000 else 
                                                4.50)

            # Calculate Employee Charges
            partners_charge = int(partners) * 3000 if partners else 0
            qualified_assistants_charge = int(qualified_assistants) * 2500 if qualified_assistants else 0
            unqualified_assistants_charge = int(unqualified_assistants) * 2000 if unqualified_assistants else 0
            others_charge = int(others) * 1000 if others else 0
            employee_charges = partners_charge + qualified_assistants_charge + unqualified_assistants_charge + others_charge

            # Calculate Profession Premium
            profession = profession.lower()
            if profession in ["opticians", "chemists", "accounts", "auditor", "attorneys"]:
                profession_premium = indemnity_premium * 1.00
            elif profession in ["architects", "civil engineers", "quantity surveyors"]:
                profession_premium = indemnity_premium * 1.35
            elif profession in ["dentists", "doctors", "surgeons"]:
                profession_premium = indemnity_premium * 1.75
            else:
                profession_premium = 0  # Default or unlisted professions get no additional premium

            # Calculate Basic Premium
            basic_premium = annual_fee_premium + indemnity_premium + employee_charges + profession_premium

            # Calculate Extensions
            loss_of_documents = tracker.get_slot("loss_of_documents")
            dishonest_employees = tracker.get_slot("dishonest_employees")
            incoming_outgoing_partners = tracker.get_slot("incoming_outgoing_partners")
            breach_of_authority = tracker.get_slot("breach_of_authority")
            libel_and_slander = tracker.get_slot("libel_and_slander")

            extensions_fee = 0
            extensions_count = sum([
                (loss_of_documents == 'yes'), 
                (dishonest_employees == 'yes'), 
                (incoming_outgoing_partners == 'yes'), 
                (breach_of_authority == 'yes'), 
                (libel_and_slander == 'yes')
            ])
            extensions_fee = basic_premium * 0.10 * extensions_count

            # Total Premium
            total_premium = basic_premium + extensions_fee

            dispatcher.utter_message(
                text=f"The total premium for {company_name} is {total_premium:.2f}."
            )
            return [
                SlotSet("basic_premium", basic_premium),
                SlotSet("total_premium", total_premium)
            ]
        except (TypeError, ValueError):
            dispatcher.utter_message(
                text="I'm unable to calculate the premium due to missing or incorrect information."
            )
        return []

class ValidatePremiumCalculationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_premium_calculation_form"

    async def validate_base_premium(
        self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Ensure base premium is a positive number greater than 1."""
        if slot_value and isinstance(slot_value, (int, float)) and slot_value > 1:
            return {"base_premium": slot_value}
        dispatcher.utter_message(text="The base premium must be a positive number greater than 1. Please enter a valid base premium.")
        return {"base_premium": None}

    async def validate_profession(
        self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Ensure profession slot is filled."""
        if slot_value:
            return {"profession": slot_value}
        dispatcher.utter_message(text="Please provide your profession.")
        return {"profession": None}

    async def validate_partners(
        self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Ensure the number of partners is provided."""
        if slot_value and isinstance(slot_value, int) and slot_value >= 0:
            return {"partners": slot_value}
        dispatcher.utter_message(text="Please provide the number of partners (enter 0 if none).")
        return {"partners": None}

    async def validate_qualified_assistants(
        self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Ensure the number of qualified assistants is provided."""
        if slot_value and isinstance(slot_value, int) and slot_value >= 0:
            return {"qualified_assistants": slot_value}
        dispatcher.utter_message(text="Please provide the number of qualified assistants (enter 0 if none).")
        return {"qualified_assistants": None}

    async def validate_unqualified_assistants(
        self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Ensure the number of unqualified assistants is provided."""
        if slot_value and isinstance(slot_value, int) and slot_value >= 0:
            return {"unqualified_assistants": slot_value}
        dispatcher.utter_message(text="Please provide the number of unqualified assistants (enter 0 if none).")
        return {"unqualified_assistants": None}

    async def validate_others(
        self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Ensure the number of other employees is provided."""
        if slot_value and isinstance(slot_value, int) and slot_value >= 0:
            return {"others": slot_value}
        dispatcher.utter_message(text="Please provide the number of other employees (enter 0 if none).")
        return {"others": None}
