# **Insurance Quotation Automation Using Rasa Chatbot**
![Alt text](./images/pic2.webp)


# Table of Contents
1. [Business Understanding](#business-understanding)
   - [Business Overview](#business-overview)
   - [Business Objective](#business-objective)
   - [Business Success Criteria](#business-success-criteria)
   - [Requirements](#requirements)
   - [Assumptions and Constraints](#assumptions-and-constraints)
   - [Data Mining Goals](#data-mining-goals)
   - [Data Mining Success Criteria](#data-mining-success-criteria)
2. [Data Understanding](#data-understanding)
   - [Data Understanding Overview](#data-understanding-overview)
   - [Data Description](#data-description)
   - [Verifying Data Quality](#verifying-data-quality)
   - [Data Mining Success Criteria](#data-mining-success-criteria)
   - [Data Mining Goals](#data-mining-goals)
3. [Data Preparation](#data-preparation)
   - [Loading Data](#loading-data)
   - [Cleaning Data](#cleaning-data)
4. [Analysis](#analysis)
5. [Conclusion](#conclusion)
6. [Recommendations](#recommendations)
7. [Next Steps](#next-steps)
8. [Libraries and Tools Used](#libraries-and-tools-used)
9. [Installation Guide](#installation-guide)


## **Business Understanding**

### **Overview**
The project automates the facultative underwriting process for Professional Indemnity Insurance (PII) quotation requests, which includes analyzing proposal forms and other relevant documents submitted by clients. Facultative reinsurance allows insurance companies to transfer some of their liabilities to other insurers, thus managing risk effectively. This process, however, traditionally involves manual analysis, which is time-consuming and prone to errors. This project aims to automate the analysis and processing of these requests to speed up the quotation generation and improve operational efficiency.

### **Goal**
The goal of the project is to develop a chatbot that automates the underwriting process for facultative insurance quotations. This includes extracting relevant data from documents submitted by clients, validating the information, and generating a professional indemnity insurance quote.

### **Objectives**
1. Automate the extraction of relevant information from the proposal forms and associated documents.
2. Use predefined business rules to calculate insurance premiums based on input data.
3. Generate a detailed quote document for the client.
4. Enable faster and more accurate responses to clients by automating the quote generation process.
5. Improve the efficiency of the underwriting team by reducing manual intervention.

### **Stakeholders**
- **Insurance Underwriters**: Responsible for reviewing and approving the generated quotes.
- **Insurance Brokers**: Intermediaries who submit insurance proposals on behalf of their clients.
- **Clients (Reinsured Companies)**: The entities purchasing Professional Indemnity Insurance.
- **Software Developers**: Responsible for the development and maintenance of the system.
- **Data Analysts**: Responsible for interpreting results and refining the data models.

---

## **Data Understanding**

### **Source of Data**
The system uses proposal forms which contain details such as business profession, indemnity amount, staff numbers and a rating guide used to calculate the quote.

- **Client Input Data**: Manually entered by an underwritter, including details like the number of staff, business profession, and other factors that influence the quote calculation.

### **Description of Data**
The data is primarily structured information from the proposal form, and unstructured data from documents (PDFs, text files). Key fields include:

- **business_profession**: Type of business or profession seeking insurance.
- **name_reinsured**: Name of the insured company.
- **name_broker**: Name of the broker facilitating the insurance.
- **name_insured**: Name of the insured entity.
- **number_partners_principal**: Number of partners/principals in the business.
- **number_qualified_assistants**: Number of qualified assistants.
- **number_unqualified_assistants**: Number of unqualified assistants.
- **number_other_staff**: Other staff in the business.
- **indemnity_amount**: The amount the company wishes to be covered for in case of a claim.

---

## **Analysis**
The analysis involves processing the input data to calculate the insurance quote based on the business profession, indemnity amount, and the number of staff in different categories. Using predefined business rules, the system calculates:

- **Staff Fee**: Based on the number of partners and assistants in the business.
- **Annual Fee**: Based on the indemnity amount requested.
- **Limit of Indemnity**: Based on the indemnity amount.
- **Profession Fee**: Based on the type of profession.
- **Basic Premium**: Sum of staff fee, annual fee, and profession fee.
- **Comprehensive Premium**: Basic premium, potentially adjusted by additional fees such as levies.
- **Total Premium**: Final premium payable, including levies.

The calculated premiums and the final quote are then presented in a text format for the underwritter.

---

## **Conclusion**
The automation of the facultative underwriting process significantly reduces the time needed to generate insurance quotes. By eliminating manual analysis, the process becomes faster, more consistent, and less prone to human error. This solution also allows for more accurate underwriting decisions based on predefined criteria, ultimately improving customer satisfaction and operational efficiency.

---

## **Recommendation**
- **Further Automation**: Extend the automation to cover other aspects of the underwriting process, such as policy issuance and claims handling.
- **Data Quality**: Ensure data entered into the system is accurate and complete to improve the quality of quotes generated.
- **Client Communication**: Implement additional communication tools to automatically send quotes and updates to clients.
- **Integration**: Integrate the system with other parts of the insurance company’s infrastructure (e.g., policy management systems, CRM).

---

## **Next Steps**
- **Testing & Validation**: Thoroughly test the system using real-world insurance proposal data to ensure accuracy in premium calculations.
- **User Training**: Provide training to underwriters and brokers on how to use the system effectively.
- **Deploy the System**: Deploy the system in a production environment for real-time use.

---

## **Libraries and Tools Used**

- **Rasa SDK**: Used for developing the chatbot (https://rasa.com/docs/rasa/).
- **Python 3.8+**: Programming language used for implementing the logic (https://www.python.org/downloads/).
- **Pandas**: Used for data manipulation and calculations (https://pandas.pydata.org/).
- **NumPy**: Used for numerical calculations (https://numpy.org/).

---

## **Installation Guide**

### **For Windows**
1. **Clone the Repository:**
   Open Command Prompt or PowerShell and run the following command:
   ```bash
   git clone https://github.com/Kanyi254/Insurance-quotation
   cd facultative-underwriting-automation
   ```

2. **Create a Virtual Environment:**
   In the Command Prompt, run:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   ```bash
   .\venv\Scripts\activate
   ```

4. **Install Required Libraries:**
   Install dependencies listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the Rasa Server (if using Rasa for chatbot):**
   ```bash
   rasa run
   ```

6. **Start the Flask App (if applicable):**
   ```bash
   flask run
   ```

7. **For Testing:**
   Run any pre-configured unit tests or test scripts to ensure the system works as expected.

---

### **For Mac**
1. **Clone the Repository:**
   Open Terminal and run the following command:
   ```bash
   git clone https://github.com/Kanyi254/Insurance-quotation
   cd facultative-underwriting-automation
   ```

2. **Create a Virtual Environment:**
   In Terminal, run:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Required Libraries:**
   Install dependencies listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the Rasa Server (if using Rasa for chatbot):**
   ```bash
   rasa run
   ```

6. **Start the Flask App (if applicable):**
   ```bash
   flask run
   ```

7. **For Testing:**
   Run any pre-configured unit tests or test scripts to ensure the system works as expected.

---

### **For Linux**
1. **Clone the Repository:**
   Open a terminal window and run the following command:
   ```bash
   git clone https://github.com/Kanyi254/Insurance-quotation
   cd facultative-underwriting-automation
   ```

2. **Create a Virtual Environment:**
   In the terminal, run:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install Required Libraries:**
   Install dependencies listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the Rasa Server (if using Rasa for chatbot):**
   ```bash
   rasa run
   ```

6. **Start the Flask App (if applicable):**
   ```bash
   flask run
   ```

7. **For Testing:**
   Run any pre-configured unit tests or test scripts to ensure the system works as expected.

---
