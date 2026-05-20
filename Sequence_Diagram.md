# PredictCare Hospital Management System - Master Sequence Diagram

This document contains a comprehensive, high-fidelity Unified Modeling Language (UML) Sequence Diagram for the PredictCare project. It illustrates the complete lifecycle of a patient and hospital operations, featuring multiple actors and specialized sub-systems.

---

## 1. Integrated Hospital Lifecycle Workflow

This diagram covers the end-to-end journey from registration to pharmacy dispensing, including advanced AI-driven load forecasting and clinical examination.

```mermaid
sequenceDiagram
    autonumber
    
    actor P as Patient
    actor R as Receptionist
    actor D as Doctor
    actor Ph as Pharmacist
    actor A as Admin
    
    participant UI as PredictCare UI (Browser)
    participant Server as Django Application Server
    participant DB as PostgreSQL Database
    participant AI as AI Prediction Engine (Scikit-Learn)
    
    %% Section 1: Patient Registration & Onboarding
    rect rgb(240, 248, 255)
    Note over R, UI: Phase 1: Patient Onboarding & Registration
    R->>+UI: Input Patient Demographics (Name, Age, DOB, Gender)
    activate R
    UI->>+Server: POST /register_patient/
    Server->>Server: Validate Form Data & Sanitize Inputs
    Server->>+DB: INSERT INTO hospital_patient
    DB-->>-Server: Return 201 Created & New patient_id
    Server-->>-UI: 200 OK (Registration Success)
    UI-->>-R: Display New Patient Profile
    deactivate R
    R->>P: Issue Physical Patient ID Card
    end
    
    %% Section 2: Appointment Scheduling & Queue Management
    rect rgb(245, 245, 245)
    Note over R, UI: Phase 2: Appointment Scheduling
    R->>+UI: Select Department & Preferred Doctor
    activate R
    UI->>+Server: GET /get_available_slots/?doctor_id=X
    Server->>+DB: SELECT available_slots FROM hospital_doctor
    DB-->>-Server: Return Time Grid (JSON)
    Server-->>-UI: Render Interactive Slot Picker
    R->>UI: Select Slot (e.g., 10:30 AM) & Case Type
    UI->>+Server: POST /book_appointment/
    Server->>+DB: INSERT INTO hospital_visit (Status=Pending, Slot=10:30 AM)
    DB-->>-Server: Confirm Insertion
    Server-->>-UI: 200 OK (Appointment Confirmed)
    UI-->>-R: Generate Digital Token / Print Entry Slip
    deactivate R
    end
    
    %% Section 3: Clinical Consultation & Digital Prescribing
    rect rgb(255, 255, 240)
    Note over D, UI: Phase 3: Clinical Examination & Diagnosis
    D->>+UI: Access Doctor Dashboard (Live Patient Queue)
    activate D
    UI->>+Server: GET /doctor_dashboard/
    Server->>+DB: SELECT * FROM hospital_visit WHERE doctor_id=X & date=TODAY
    DB-->>-Server: Return Active Patient List
    Server-->>-UI: Render Active Queue View
    UI-->>-D: Highlight Next Pending Patient (P)
    
    D->>+UI: Click "Examine Patient", Input Symptoms & Diagnosis
    D->>UI: Prescribe Medications (Medicine Name, Qty, Dosage)
    UI->>+Server: POST /complete_visit/
    
    par Atomic Data Commit
        Server->>+DB: UPDATE hospital_visit (Add Symptoms, Diagnosis)
        Server->>DB: INSERT INTO pharmacy_prescriptionline (Prescribed Meds)
        DB-->>-Server: Transaction Successfully Committed
    end
    
    Server-->>-UI: 302 Redirect (Return to Dashboard)
    UI-->>-D: Patient Marked as "Visited"
    deactivate D
    end
    
    %% Section 4: AI-Driven Analytics & Forecasting (The Monitoring Logic)
    rect rgb(240, 255, 240)
    Note over A, AI: Phase 4: AI Analytics & Predictive Modeling
    A->>+UI: Open "Health Informatics & Planning" Dashboard
    activate A
    UI->>+Server: GET /predict_load/ (Department Load Forecast)
    
    Server->>+DB: SELECT * FROM hospital_visit (Historical Trends)
    DB-->>-Server: Return Raw Data Dictionary
    
    Server->>+AI: Execute Forecast Logic (Pandas + Scikit-Learn)
    AI->>AI: Feature Engineering (Time Series Analysis)
    AI->>AI: Linear Regression Fit(X, y)
    AI->>AI: Predict Future Patient Load (T+1, T+2)
    AI-->>-Server: Return JSON Payload (Predicted Values)
    
    Server-->>-UI: Deliver AI Insights (JSON)
    UI->>UI: Chart.js Parses & Renders Predictive Graph
    UI-->>-A: Display Visualized Forecast & Resource Planning
    deactivate A
    end
    
    %% Section 5: Pharmacy Operations & Inventory Billing
    rect rgb(255, 250, 250)
    Note over Ph, UI: Phase 5: Pharmacy Fulfillment & Billing
    Ph->>+UI: Open Pharmacy Queue (Dispensing Dashboard)
    activate Ph
    UI->>+Server: GET /pharmacy_queue/
    Server->>+DB: SELECT Pending Prescriptions
    DB-->>-Server: Return Active Medication List for Patient (P)
    Server-->>-UI: Render Fulfillment View
    
    Ph->>+UI: Verify Stock & Click "Generate Bill & Dispense"
    UI->>+Server: POST /generate_bill/
    
    par Dynamic Stock Deduction
        Server->>+DB: INSERT INTO pharmacy_pharmacybill (Total Invoice)
        Server->>DB: UPDATE pharmacy_medicine SET stock = stock - QTY
        DB-->>-Server: Atomic Commit Success
    end
    
    Server-->>-UI: 200 OK (Render Invoice Template)
    UI-->>-Ph: Display Printable Invoice
    deactivate Ph
    Ph-->>P: Dispense Medication & Hand Over Bill
    end
```

---

## 2. Key Component Definitions

- **PredictCare UI (Browser)**: A modern, responsive dashboard built with Django Templates and Chart.js for real-time visualization.
- **Django Application Server**: The core logic layer handling request routing, form validation, and business rules.
- **PostgreSQL Database**: The relational storage engine ensuring data integrity through atomic transactions.
- **AI Prediction Engine**: A specialized Python environment utilizing Scikit-Learn to provide data-driven insights for hospital management.

## 3. Workflow Summary

The system ensures seamless transition between different hospital roles (Front Desk, Clinic, AI Planning, Pharmacy) by maintaining a single source of truth in the PostgreSQL database. Each phase utilizes real-time API calls to keep all dashboards synchronized.
