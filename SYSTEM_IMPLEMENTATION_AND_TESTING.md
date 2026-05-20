# 6. SYSTEM IMPLEMENTATION & TESTING

## 6.1 SYSTEM IMPLEMENTATION

The **PredictCare** system is implemented using the **Django 5.x** framework following the **Model-View-Template (MVT)** architectural pattern. This decoupling allows for independent scaling of the data models, administrative logic, and the responsive user interface.

### 6.1.1 Core Technological Stack
- **Backend**: Python 3.10+ and Django 5.x for robust server-side processing and RESTful routing.
- **Database**: **PostgreSQL** serves as the primary relational storage, utilizing composite indexing on `visit_date`, `department`, and `staff_id` to maintain sub-second query performance even as the `hospital_visit` table scales beyond 1,000,000 records.
- **Frontend**: A combination of **Tailwind CSS** for layout and **Chart.js** for high-fidelity interactive data visualizations of hospital traffic and resource distribution.

### 6.1.2 Advanced Modules & Logic
- **AI Analytics Engine**: Built on **Scikit-Learn** and **Pandas**, the system executes **Ordinary Least Squares (OLS) Linear Regression** to forecast department-wise load and medicine demand. The engine includes a confidence scoring mechanism (Average R-squared) to inform administrators of prediction reliability.
- **SMSR Algorithm**: The *Staff Management & Shift Rotation* engine implements a modulo-based mathematical rotation that ensures 24/7 hospital coverage without temporal gaps or staff fatigue.
- **Pharmacy Integration**: Automated stock management triggers recursive inventory updates upon `PrescriptionLine` generation, ensuring real-time alignment between clinical consultations and pharmacy billing.

## 6.2 SYSTEM TESTING

System testing is a multi-layered validation phase designed to ensure the **PredictCare** platform achieves 100% operational reliability within a production hospital environment.

### 6.2.1 White Box Testing (Structural Validation)
- **Unit Testing**: Leveraging Django’s `TestCase` framework, individual functions such as stock deduction logic, patient ID generation, and shift overlap calculations are verified (`pharmacy/tests.py`).
- **Model Integrity**: Strict validation is applied to data types, `MinValueValidator` constraints for age/quantity, and `on_delete=models.PROTECT` behaviors to prevent accidental loss of clinical history.
- **Algorithmic Verification**: The ML engine is tested using `test_analytics.py` to ensure that dataframes are correctly sampled and that regression results remain mathematically consistent.

### 6.2.2 Black Box Testing (Functional Validation)
- **Role-Based Access Control (RBAC)**: Verified through simulated login sessions (`test_login.py`) to ensure Pharmacists, Doctors, and Receptionists only access authorized endpoints and data sets.
- **UAT (User Acceptance Testing)**: End-to-end workflows, from patient registration to diagnostic logging and final bill generation, are tested for usability and functional correctness.
- **Document Management**: The `PatientDocument` upload feature is stress-tested for secure file handling and correct associations with the patient root entity (`test_document_upload.py`).

### 6.2.3 Integration & Performance Testing
- **Cross-App Communication**: Ensuring that consultations logged in the `hospital` app immediately sync with the `pharmacy` billing portal.
- **Stress Testing**: Validating that database aggregations, such as `TruncMonth` trends and traffic heatmaps, execute efficiently on datasets containing hundreds of thousands of visits.
