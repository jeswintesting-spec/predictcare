# 🏥 PredictCare (Built for BMH Hospital)

A comprehensive, production-ready hospital management application built with **Django 5.x** and **PostgreSQL**, featuring smart scheduling, pharmacy management, and predictive analytics.

## 🚀 Overview
The PredictCare system is a state-of-the-art solution built for **BMH Hospital** to digitize and optimize hospital operations. From patient registration and visit tracking to complex staff scheduling and data-driven load forecasting, PredictCare provides a robust platform for modern healthcare facilities.

## 🛠 Tech Stack
-   **Backend**: Python 3.10+, Django 5.x
-   **Database**: PostgreSQL (Primary Storage)
-   **Frontend**: HTML5, Vanilla CSS / Tailwind CSS, JavaScript (Dynamic UI)
-   **Data Science**: Pandas, Scikit-learn (Patient Load Prediction)
-   **Reporting**: OpenPyXL (Professional Excel Exports)

## ✨ Core Modules

### 🏥 Hospital Core
-   **Patient Management**: Full CRUD operations for patient records with unique ID generation.
-   **Staff Management**: Manage Doctors and Nurses, tracking qualifications, shifts, and specializations.
-   **Visit Tracking**: Comprehensive log of patient consultations, including case types (Normal/Emergency/Critical), symptoms, and diagnoses.

### 💊 Pharmacy Management
-   **Inventory Control**: Real-time tracking of medicine stock levels with low-stock alerts.
-   **Digital Billing**: Automated billing generation for dispensed medicines.
-   **Prescription Integration**: Seamlessly link doctor prescriptions to pharmacy dispensing.

### 📅 Smart Scheduling (SMSR Algorithm)
-   **24/7 Coverage**: Implements the **SMSR (Staff Management & Shift Rotation)** algorithm.
-   **Modulo-Based Rotation**: Ensures fair and consistent shift distribution for doctors and nurses.
-   **Resource Optimization**: Automatically assigns staff to ensure every department is covered around the clock.

### 🧠 Predictive Analytics
-   **Traffic Forecasting**: Scikit-Learn powered models to predict daily patient traffic per department.
-   **Resource Planning**: Helps administrators allocate staff based on predicted surges.
-   **Visual Dashboards**: Interactive charts showing visit trends and hospital load.

## 👥 User Roles & Access
| Role | Primary Responsibilities |
| :--- | :--- |
| **Admin** | Full system configuration, user management, and database oversight. |
| **Receptionist** | Patient registration, visit logging, and general appointment management. |
| **Doctor** | Consultation tracking, symptom recording, and patient history review. |
| **Pharmacist** | Inventory management, medicine dispensing, and bill generation. |

## 🏁 Quick Start

### Prerequisites
-   Python 3.10+
-   PostgreSQL installed and running

### Installation & Launch
1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd project-duplicate
    ```
2.  **Environment Setup**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Database Configuration**:
    Configure your `.env` file with PostgreSQL credentials.
4.  **Run the App**:
    -   **On Mac/Linux**: Double-click `LAUNCH_ON_MAC.command` or run `./LAUNCH_ON_MAC.command`
    -   **On Windows**: Double-click `LAUNCH_ON_WINDOWS.bat`
5.  **Access**:
    -   App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    -   Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (Default: `admin` / `admin123`)

## 📂 Project Structure
-   `hospital/`: Main app for patient, staff, and visit logic.
-   `pharmacy/`: Dedicated module for inventory and billing.
-   `accounts/`: Role-based authentication and user profiles.
-   `ml/`: Machine learning models for load prediction.
-   `templates/`: Rich, responsive HTML frontend.
-   `smsr_scheduler.py`: The core SMSR scheduling engine.

---
*Developed for excellence in healthcare management.*
