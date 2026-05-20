# PredictCare HMS - Multi-Level Data Flow Diagrams (DFD)

This document contains the formalized Data Flow Diagrams broken down into Context (Level-0), High-Level (Level-1), and Sub-Process (Level-2) representations for the Hospital Management and Analytics System.

---

## 1. Level-0 DFD (Context Diagram)
The Level-0 diagram treats the entire Hospital Management System as a single centralized process, showing only the external boundaries (Users) trading data with the main system.

```mermaid
flowchart TD
    %% Styling
    classDef sys fill:#1E40AF,stroke:#1E3A8A,stroke-width:3px,color:#fff,font-weight:bold
    classDef entity fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff

    %% External Entities
    Patient[Patient]:::entity
    Doctor[Doctor]:::entity
    Nurse[Nurse / Receptionist]:::entity
    Pharmacist[Pharmacist]:::entity
    Admin[Hospital Administrator]:::entity

    %% Core System
    HMS((PredictCare HMS\n& AI Engine)):::sys

    %% Data Flows
    Patient -- 1. Basic Demographics\n2. Appointment Requests --> HMS
    HMS -- 1. Visit Slots\n2. Prescriptions & Invoices --> Patient

    Nurse -- 1. Uploads Lab Reports\n2. Registers Patient Intake --> HMS
    HMS -- 1. Today's Roster\n2. Patient Files --> Nurse

    Doctor -- 1. Issues Diagnosis\n2. Prescribes Medicine --> HMS
    HMS -- 1. Patient Medical History\n2. AI Department Forecasts --> Doctor

    Pharmacist -- 1. Confirms Dispensation --> HMS
    HMS -- 1. Prescription Queues\n2. AI Restock Recommendations --> Pharmacist

    Admin -- 1. Staff Profiles\n2. Department Parameters --> HMS
    HMS -- 1. 24/7 Staff Schedules\n2. Resource Utilization Flags --> Admin
```

---

## 2. Level-1 DFD (Major Sub-Systems)
The Level-1 diagram breaks the monolithic system out into its core application modules (Registration, Clinical, Pharmacy, HR, and AI Analytics) and their interactions with the relational databases.

```mermaid
flowchart TD
    classDef process fill:#10B981,stroke:#047857,stroke-width:2px,color:#fff,shape:circle
    classDef entity fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff
    classDef db fill:#F59E0B,stroke:#B45309,stroke-width:2px,color:#fff,shape:cylinder

    %% External Entities
    Patient[Patient]:::entity & Nurse[Nurse]:::entity
    Doctor[Doctor]:::entity
    Pharmacist[Pharmacist]:::entity
    Admin[Administrator]:::entity

    %% Level-1 Processes (Modules)
    P1((1.0 Registration\n& Appointments)):::process
    P2((2.0 Clinical\nOperations)):::process
    P3((3.0 Pharmacy\n& Billing)):::process
    P4((4.0 Admin\n& HR Scheduling)):::process
    P5((5.0 AI Predictive\nAnalytics)):::process

    %% Data Stores (Tables)
    D1[(D1: Patients DB)]:::db
    D2[(D2: Visits DB)]:::db
    D3[(D3: Pharmacy DB)]:::db
    D4[(D4: Staff DB)]:::db

    %% Flows from Entities to Processes
    Patient & Nurse -- Intake Info --> P1
    Doctor -- Diagnoses &\nPrescriptions --> P2
    Pharmacist -- Verify Cart --> P3
    Admin -- Configuration --> P4

    %% Processes to DB
    P1 -- Create/Update --> D1
    P1 -- Book Slot --> D2
    P2 -- Append Records --> D2
    P3 -- Adjust Stock --> D3
    P3 -- Generates Bill --> D1
    P4 -- Manage Shifts --> D4

    %% Complex DB to AI Flows
    D2 -. 2M Rows\nHistorical Data .-> P5
    D4 -. Active Capacity .-> P5
    D3 -. Existing Stock .-> P5

    %% AI Outputs back to Entities
    P5 -. 3-Month Trajectory .-> Doctor
    P5 -. Restock Forecast .-> Pharmacist
    P5 -. Staffing Flags .-> Admin
```

---

## 3. Level-2 DFD (AI Forecasting Sub-Processes)
The Level-2 diagram selectively zooms deeply into Process 5.0 (AI Predictive Analytics) to detail exactly how the unformatted Django query data is mathematically transformed into dashboard predictions.

```mermaid
flowchart LR
    classDef subproc fill:#8B5CF6,stroke:#5B21B6,stroke-width:2px,color:#fff,shape:hexagon
    classDef db fill:#F59E0B,stroke:#B45309,stroke-width:2px,color:#fff,shape:cylinder
    classDef ext fill:#1F2937,stroke:#111827,stroke-width:2px,color:#fff

    %% Databases (Inputs)
    D2[(D2: Visit Logs)]:::db
    D4[(D4: Staff Roster)]:::db

    %% Level-2 Sub-Processes for 5.0
    P5_1{{5.1 Extract & Clean\nDataFrame}}:::subproc
    P5_2{{5.2 TruncMonth\nAggregation}}:::subproc
    P5_3{{5.3 Scikit-Learn\nLinear Regression}}:::subproc
    P5_4{{5.4 Staff Utilization\nRatio Math}}:::subproc

    %% Outputs (Dashboard Views)
    O1[Department Load\nForecast Charts]:::ext
    O2[Medicine Depletion\nForecast Matrix]:::ext
    O3[HR Diagnostic\nFlags]:::ext

    %% Flows
    D2 -- Raw QuerySet --> P5_1
    P5_1 -- Pandas DataFrame --> P5_2
    
    %% ML Path 1 (Regression)
    P5_2 -- Grouped Time-Series\n(excluding current incomplete month) --> P5_3
    P5_3 -- Extrapolated Vectors --> O1
    P5_3 -- Projected Prescription Strings --> O2

    %% ML Path 2 (Diagnostics)
    D4 -- Active Employee Counts --> P5_4
    P5_1 -- Recent Volume / Department --> P5_4
    P5_4 -- Calculated Ratios\n(Visits/Doc & Visits/Nurse) --> O3
```
