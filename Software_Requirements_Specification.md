# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document provides a comprehensive architectural and functional overview of the Hospital Management and Analytics System. It details the system's capabilities, constraints, and software interfaces to guide developers, stakeholders, and testers.

### 1.2 Document Conventions
This document utilizes standard Markdown formatting. High-level features are divided into major modules, followed by detailed sub-features. Technical terminology associated with Django, Python, PostgreSQL, and Machine Learning (scikit-learn) is used throughout.

### 1.3 Intended Audience and Reading Suggestions
This document is intended for:
- **Developers & Engineers:** To understand the architectural flow, database schema, and exact functional requirements for further feature scaling.
- **Project Managers & Stakeholders:** To evaluate the project scope, AI capabilities, and resource management solutions.
- **Testers:** To formulate test cases for both the CRUD interfaces and the Predictive AI models.

### 1.4 Project Scope
The proposed system is a fully digitized Hospital Management System (HMS) heavily augmented with Artificial Intelligence. It encompasses:
- Core Hospital Administration (Staff, Patients, Departments)
- Smart 24/7 Staff Scheduling and Shift Management
- Pharmacy and Inventory Management integrated with Patient Billing
- Clinical Data Logging (Symptoms, Prescriptions, Case Types)
- Predictive AI Dashboards (Future load forecasting, AI staffing diagnostics, Medicine demand predictions)
- Secure Digital File & Document Management

---

## 2. Overall Description

### 2.1 Product Perspective
The system operates as a monolithic web application structured on the Django framework. It transitions traditional hospital workflows from disconnected physical or basic digital registries into a unified PostgreSQL-backed ecosystem. It implements predictive data science to convert passive historical data into proactive management recommendations.

### 2.2 Product Features
* **Patient & Clinical Records:** Registration, real-time visit tracking, diagnosis, and medical history.
* **Intelligent Staff Scheduling:** Automated generation of 24/7 shift rotations spanning multiple departments without temporal conflicts.
* **Pharmacy Operations:** Tracking dynamic medicine stock, auto-generating prescription bills, and evaluating unit costs.
* **AI Analytics Dashboard:** 
  * Linear-regression-based prediction algorithms for estimating department crowding up to 3 months in advance.
  * Real-time analytical evaluation of "Doctor-to-Patient" ratios to diagnose underutilized or critically overloaded departments.
  * Future medicine stock depletion forecasting based on organic historical prescription trends.
* **Document Vault:** Secure upload, classification, and retrieval of sensitive patient assets (Lab Reports, Scans, etc.).

### 2.3 User Classes and Characteristics
1. **Administrators:** Full access to all analytics, raw database management, and staff registration.
2. **Doctors/Physicians:** Access to assigned patient histories, specialized AI load predictions for their specific schedules, and prescription issuing interfaces.
3. **Nurses/Staff:** View-access to shift schedules, patient routing, and document ingestion interfaces.
4. **Pharmacists:** Access to billing portals, inventory alerts, and AI stock replenishment forecasts.

### 2.4 Operating Environment
* **Server-side:** Python 3.x, Django 5.x Framework, Pandas, Scikit-learn
* **Database:** PostgreSQL (with psycopg2 adapter)
* **Frontend:** HTML5, TailwindCSS, JavaScript (Chart.js for rendering analytics)
* **OS:** Cross-platform (Linux/Unix servers for deployment, accessible via any modern web browser)

---

## 3. System Features

### 3.1 Patient Management Module
* **Description:** Manages the entire lifecycle of a patient within the hospital DB.
* **Functional Requirements:**
  * System must allow creating, reading, updating, and deleting (CRUD) patient profiles.
  * System must associate unique Patient IDs (`BMHXXXX`) to individuals.
  * System must log sequential clinical "Visits", associating an active Doctor, Department, Symptoms, and Prescribed Medicines.
  * System must allow associating digital files (`PatientDocument`) directly to the patient's root entity.

### 3.2 Staff & Shift Handling
* **Description:** Administration of hospital personnel and their respective time allocations.
* **Functional Requirements:**
  * System must distinguish between `Doctors` and `Nurses` structurally, assigning them to exact `Departments`.
  * System must support an algorithmic 24/7 auto-scheduler capable of assigning Morning, Evening, and Night shifts mathematically to prevent hospital coverage gaps.

### 3.3 Pharmacy & Patient Billing
* **Description:** Tracking chemical inventory and converting clinical visits into financial transactions.
* **Functional Requirements:**
  * System must deduct `stock_quantity` from the `Medicine` table when a formal `PrescriptionLine` is generated.
  * System must automatically compute the `total_amount` for a `PharmacyBill` by summing the prices of the prescribed units.
  * System must enforce a `min_stock_level` threshold to identify shortage risks.

### 3.4 Predictive AI & Analytics
* **Description:** The intelligence core extrapolating future states from Django database query sets.
* **Functional Requirements:**
  * System must utilize `scikit-learn`'s `LinearRegression` fed via `pandas` DataFrames to plot future trends.
  * *Department Load Prediction:* Calculate future patient volume recursively for $n$ months based on daily department throughput.
  * *Medicine Forecasting:* Isolate individual string-split medicine occurrences from visit logs and project required unit stock for the next 30-day window.
  * *Staffing Diagnostics:* Normalize recent visit traffic over the total temporal span of the dataset, dividing by active active staff limits to issue binary ("Optimal", "Overloaded", "Underutilized") operational commands to administrators.
  * Machine learning logic must actively exclude the "current incomplete calendar month" to prevent negative sloping and artificial data drops.

## 4. Software Architecture (Modules)

The system is organized into **five primary modules** (Django Apps), each enforcing a strong separation of concerns:

### 4.1 Core Module: `hospital`
* **Purpose:** The nucleus of clinical and administrative operations. 
* **Scope:** Manages all CRUD workflows for registering Patients, hiring Doctors and Nurses, and establishing Departments. It is responsible for logging sequential clinical "Visits" and acting as the digital registry for uploaded `PatientDocuments`.

### 4.2 Utility Module: `pharmacy`
* **Purpose:** Financial and Inventory Management.
* **Scope:** Tracks `Medicine` stock properties (pricing, minimum thresholds). Converts doctor-issued prescriptions into `PrescriptionLine` database entries, auto-triggering corresponding financial invoices via the `PharmacyBill` models.

### 4.3 Security Module: `accounts`
* **Purpose:** Authentication and Authorization.
* **Scope:** Inherits and extends Django's native authentication framework. Manages login sessions and enforces Role-Based Access Control (RBAC) to ensure a pharmacist cannot access sensitive clinical predictions, and a nurse cannot alter core HR infrastructure.

### 4.4 Analytical Module: `ml`
* **Purpose:** Mathematics and Artificial Intelligence.
* **Scope:** Contains the core algorithmic implementations. It extracts aggregated dictionaries from the `hospital` and `pharmacy` PostgreSQL databases, converts them into memory-efficient `pandas` DataFrames, and executes `LinearRegression` analysis to predict future traffic and stock demands.

### 4.5 Configuration Module: `bmh_project`
* **Purpose:** The orchestration wrapper combining the four functional modules into a cohesive ecosystem.
* **Scope:** This is the core infrastructural hub. It contains the universal `settings.py` defining the PostgreSQL credentials, `wsgi.py`/`asgi.py` for cloud server deployment, and the master `urls.py` router that maps incoming HTTP requests to their appropriate sub-module endpoints.

---

## 5. External Interface Requirements

### 4.1 User Interfaces
* **Responsive Design:** Interfaces build using Tailwind CSS mapping to Desktop, Tablet, and Mobile viewports.
* **Data Visualization:** Dashboard heavily leverages Chart.js to render Interactive Line Charts, Pie Charts, and Bar Graphs for multidimensional data.
* **Interactive Tooling:** Graphs support click-to-enlarge modal features scaling canvases dynamically for legibility.

### 4.2 Software Interfaces
* **PostgreSQL Engine:** Primary source of truth. Accessed strictly via the Django ORM to prevent SQL injection constraints.
* **Pandas / Scikit-learn Ecosystem:** Memory-level dataframe processing; connects via native Python arrays converted from Django QuerySet dictionaries.

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
* The system should be robust enough to handle dataframes exceeding $1,000,000$ rows. Analytics aggregations (such as absolute historical trends) should rely on native SQL aggregation (e.g., `TruncMonth`) to execute in milliseconds natively on the Postgres layer rather than via Python logic.

### 5.2 Security Requirements
* Uses Django's built-in session authentication middleware. 
* Media files and patient documents uploaded to `MEDIA_ROOT` must not be directly executable by the server infrastructure.

### 5.3 Reliability & Availability
* The monolithic architecture allows standard WSGI/ASGI deployments behind NGINX/Gunicorn ensuring standard 99.9% uptime for internal hospital routing.

### 5.4 Maintainability
* Modularized application structure (`hospital`, `pharmacy`, `ml`); isolating database schema from analytical mathematics.
