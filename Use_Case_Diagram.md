# PredictCare Hospital Management System - Use Case Diagram

This document contains a comprehensive Unified Modeling Language (UML) Use Case Diagram for the PredictCare system. It defines the primary actors, their roles, and the functional interactions within the system boundary.

---

## 1. Professional Use Case Model

Following the layout and structural depth of the "PROCTOR EDGE" reference, the following diagram illustrates the functional scope for all system actors.

```mermaid
graph LR
    %% Actors Definition
    subgraph ActorsLeft [" "]
        P((Patient))
        R((Receptionist))
    end
    
    subgraph ActorsRight [" "]
        D((Doctor))
        Ph((Pharmacist))
        A((Admin))
    end

    %% PredictCare System Boundary
    subgraph SystemBoundary ["PredictCare Hospital Management System"]
        UC1([Login / Auth])
        UC2([Register Profile])
        UC3([View Health Records])
        UC4([Book Appointment])
        UC5([Manage Time Slots])
        UC6([Examine Patient])
        UC7([Prescribe Medicine])
        UC8([Dispense Medication])
        UC9([Generate Billing])
        UC10([AI Load Forecasting])
        UC11([Staff Management])
        UC12([Predictive Insights])
    end

    %% Relationships - Patient
    P --- UC1
    P --- UC3
    P --- UC4

    %% Relationships - Receptionist
    R --- UC1
    R --- UC2
    R --- UC4
    R --- UC5

    %% Relationships - Doctor
    D --- UC1
    D --- UC6
    D --- UC7
    D --- UC12

    %% Relationships - Pharmacist
    Ph --- UC1
    Ph --- UC8
    Ph --- UC9

    %% Relationships - Admin
    A --- UC1
    A --- UC10
    A --- UC11
    A --- UC12

    %% Visual Styling
    style SystemBoundary fill:#f9f9f9,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    style UC1 fill:#e1f5fe,stroke:#01579b
    style UC2 fill:#e1f5fe,stroke:#01579b
    style UC3 fill:#e1f5fe,stroke:#01579b
    style UC4 fill:#e1f5fe,stroke:#01579b
    style UC5 fill:#e1f5fe,stroke:#01579b
    style UC6 fill:#fff9c4,stroke:#fbc02d
    style UC7 fill:#fff9c4,stroke:#fbc02d
    style UC8 fill:#ffe0b2,stroke:#ef6c00
    style UC9 fill:#ffe0b2,stroke:#ef6c00
    style UC10 fill:#f1f8e9,stroke:#558b2f
    style UC11 fill:#f1f8e9,stroke:#558b2f
    style UC12 fill:#f1f8e9,stroke:#558b2f
```

---

## 2. Actor Roles & Primary Responsibilities

| Actor | Primary Responsibilities |
| :--- | :--- |
| **Patient** | User seeking health services, manages personal appointments and health history. |
| **Receptionist** | Front-desk staff managing patient onboarding, registration, and hospital queues. |
| **Doctor** | Clinical professional responsible for diagnosis, treatment, and medical prescriptions. |
| **Pharmacist** | Manages medication dispensing and invoice generation based on prescriptions. |
| **Admin** | System manager who utilizes AI load forecasting and analytics for resource planning. |

## 3. System Components Summary

- **Core Module**: Handles user authentication, patient registration, and appointment workflow.
- **Clinical Module**: Specifically designed for doctors to manage symptoms, diagnosis, and digital prescriptions.
- **Service Module**: Provides the AI engine for load forecasting and high-level administrative insights.
- **Pharmacy Module**: Manages inventory reconciliation and atomic billing transactions.
