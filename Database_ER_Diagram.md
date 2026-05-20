# PredictCare Hospital Management System - ER Diagram

This document contains the Entity-Relationship (ER) diagram for the PredictCare Hospital Management System, mapping the relationships between the Core Hospital module and the Pharmacy & Billing module.

```mermaid
erDiagram
    %% Core Hospital Module
    DEPARTMENT {
        string name PK
    }
    
    DOCTOR {
        string staff_id PK
        string doctor_name
        string gender
        string qualifications
        string email
        string phone
        string specialization
        time shift_start
        time shift_end
        string work_days
        string shift_type
        int slot_duration
        int max_patients
        string department FK
    }
    
    NURSE {
        string staff_id PK
        string nurse_name
        string gender
        string qualifications
        string email
        string phone
        time shift_start
        time shift_end
        string work_days
        string shift_type
        string department FK
    }
    
    PATIENT {
        string patient_id PK
        string patient_name
        int age
        date dob
        string gender
        text location
        time assigned_slot
        datetime created_at
        datetime updated_at
        string doctor FK
    }
    
    VISIT {
        int id PK
        string case_type
        date visit_date
        text medicines
        text symptoms
        time slot
        datetime created_at
        string patient FK
        string department FK
        string doctor FK
    }
    
    PATIENT_DOCUMENT {
        int id PK
        string document_name
        string document_type
        string file
        datetime uploaded_at
        text notes
        string patient FK
    }

    %% Pharmacy & Billing Module
    MEDICINE {
        int id PK
        string name
        decimal price
        int stock_quantity
        int min_stock_level
        date expiry_date
        datetime created_at
        datetime updated_at
    }
    
    PRESCRIPTION_LINE {
        int id PK
        int quantity
        string dosage_instructions
        datetime created_at
        int visit FK
        int medicine FK
    }
    
    PHARMACY_BILL {
        int id PK
        string customer_name
        decimal total_amount
        datetime created_at
        string patient FK
    }
    
    BILL_ITEM {
        int id PK
        int quantity
        decimal price_per_unit
        decimal total_price
        int bill FK
        int medicine FK
    }

    %% Relationships Definition
    
    %% Department Relationships
    DEPARTMENT ||--o{ DOCTOR : "employs"
    DEPARTMENT ||--o{ NURSE : "employs"
    DEPARTMENT ||--o{ VISIT : "hosts"
    
    %% Doctor Relationships
    DOCTOR ||--o{ PATIENT : "currently assigned to"
    DOCTOR ||--o{ VISIT : "conducts"
    
    %% Patient Relationships
    PATIENT ||--o{ VISIT : "makes"
    PATIENT ||--o{ PATIENT_DOCUMENT : "owns"
    PATIENT ||--o{ PHARMACY_BILL : "receives"
    
    %% Clinical & Visit Relationships
    VISIT ||--o{ PRESCRIPTION_LINE : "generates"
    
    %% Inventory & Billing Relationships
    MEDICINE ||--o{ PRESCRIPTION_LINE : "prescribed in"
    MEDICINE ||--o{ BILL_ITEM : "billed in"
    
    PHARMACY_BILL ||--o{ BILL_ITEM : "contains"
```

## How to Read This Diagram:
* **`PK`**: Primary Key (Unique Identifier for the record)
* **`FK`**: Foreign Key (Reference to another table's Primary Key)
* **`||--o{`**: One-to-Many Relationship (e.g., One `DEPARTMENT` employs Many `DOCTORS`).
