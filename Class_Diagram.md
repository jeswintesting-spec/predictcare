# PredictCare Hospital Management System - High-Fidelity Class Diagram

This document contains a comprehensive Unified Modeling Language (UML) Class Diagram for the PredictCare Hospital Management System. It illustrates the relationships, multiplicities, attributes, and methods for all core entities in the system.

---

## 1. Professional Relational Architecture

The following diagram maps out the system's class structures and multiplicities (1-to-N and Many-to-Many), following the design style and logical depth of the "PROCTOR EDGE" reference.

```mermaid
classDiagram
    %% Core Django Base (Logical)
    class Model {
        <<Django Internal>>
        +save()
        +delete()
    }

    class User {
        <<Django Auth>>
        +int id
        +string username
        +string email
        +set_password()
        +check_password()
    }

    %% -------------------------------------
    %% Hospital Business Analytics Module
    %% -------------------------------------

    class Department {
        +string name PK
        +__str__() string
    }

    class Doctor {
        +string staff_id PK
        +string doctor_name
        +string specialization
        +time shift_start
        +time shift_end
        +string work_days
        +int slot_duration
        +int max_patients
        +__str__() string
    }

    class Nurse {
        +string staff_id PK
        +string nurse_name
        +time shift_start
        +time shift_end
        +string work_days
        +__str__() string
    }

    class Patient {
        +string patient_id PK
        +string patient_name
        +int age
        +date dob
        +string gender
        +text location
        +datetime created_at
        +save()
        +__str__() string
    }

    class Visit {
        +int id PK
        +string case_type
        +date visit_date
        +text symptoms
        +text diagnosis
        +time slot
        +datetime created_at
        +save()
        +__str__() string
    }

    class PatientDocument {
        +int id PK
        +string document_name
        +string document_type
        +file file_path
        +datetime uploaded_at
        +__str__() string
    }

    %% -------------------------------------
    %% Pharmacy & Billing Module
    %% -------------------------------------

    class Medicine {
        +int id PK
        +string name
        +decimal price
        +int stock_quantity
        +int min_stock_level
        +date expiry_date
        +is_low_stock() boolean
        +__str__() string
    }

    class PrescriptionLine {
        +int id PK
        +int quantity
        +string dosage_instructions
        +datetime created_at
        +save()
        +__str__() string
    }

    class PharmacyBill {
        +int id PK
        +string customer_name
        +decimal total_amount
        +datetime created_at
        +calculate_total() decimal
        +__str__() string
    }

    class BillItem {
        +int id PK
        +int quantity
        +decimal price_per_unit
        +decimal total_price
        +save()
        +__str__() string
    }

    %% -------------------------------------
    %% Relationships & Multiplicities
    %% -------------------------------------
    
    %% Inheritance
    Model <|-- Department
    Model <|-- Doctor
    Model <|-- Nurse
    Model <|-- Patient
    Model <|-- Visit
    Model <|-- Medicine
    Model <|-- PharmacyBill

    %% Hospital Associations
    Department "1" -- "*" Doctor : employs
    Department "1" -- "*" Nurse : employs
    Department "1" -- "*" Visit : hosts

    Doctor "1" -- "*" Patient : treats
    Doctor "1" -- "*" Visit : conducts

    Patient "1" -- "*" Visit : makes
    Patient "1" -- "*" PatientDocument : owns
    Patient "0..1" -- "*" PharmacyBill : receives

    %% Pharmacy Associations
    Visit "1" -- "*" PrescriptionLine : generates
    Medicine "1" -- "*" PrescriptionLine : prescribed_as
    Medicine "1" -- "*" BillItem : billed_as
    
    PharmacyBill "1" *-- "*" BillItem : contains
```

---

## 2. Diagram Legend & Relationship Definitions

- **1 to * (One-to-Many)**: A single record in the first class relates to zero or more records in the second class. For example, one **Department** manages many **Doctors**.
- **0..1 to * (Optional One-to-Many)**: A record may or may not relate. For example, a **PharmacyBill** can belong to a registered **Patient** (0..1) or be a "Walk-in" sale.
- **Inheritance (`<|--`)**: Denotes that one class inherits internal logic and attributes from another (e.g., all models inherit the base Django `Model` logic).
- **Composition (`*--`)**: A strong "has-a" relationship where the child cannot exist without the parent (e.g., a **BillItem** must belong to a **PharmacyBill**).

## 3. Why This Format?
This high-fidelity diagram mirrors the style of professional system documentation (as seen in the "PROCTOR EDGE" reference). It prioritizes **data encapsulation** (attributes) and **functional logic** (methods) while explicitly defining the relational constraints that govern the PredictCare ecosystem.
