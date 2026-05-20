# Detailed System Design (HMAS)

## 1. Architectural Overview

The Hospital Management and Analytics System (HMAS) utilizes a monolithic **Model-View-Template (MVT)** architecture imposed by the Django framework. This design pattern ensures a clean separation between data modeling, business logic, and user interface presentation.

### 1.1 Technology Stack
* **Frontend:** HTML5, TailwindCSS (for utility-first responsive styling), Vanilla JS, and Chart.js (for data visualization).
* **Backend Framework:** Django 5.x (Python 3.12).
* **Database Management System (DBMS):** PostgreSQL.
* **Data Science/Machine Learning Stack:** Pandas (for DataFrame manipulation) and Scikit-Learn (for Linear Regression predictions).

---

## 2. Data Flow Architecture

The data lifecycle within HMAS operates via strict directional flows to ensure security and referential integrity:

1. **Client Request:** An authenticated user (e.g., Doctor, Admin) clicks a dashboard link in their browser.
2. **URL Routing (`urls.py`):** Django intercepts the HTTP request and routes it to the designated functional view.
3. **Business Logic (`views.py`):** The view parses the request. If analytics are requested, it passes raw data to the `ml/predict_load.py` module.
4. **Database Querying (ORM):** `models.py` executes a secure SQL query via psycopg2 against the PostgreSQL database.
5. **Data Processing:** If an AI prediction is requested, Pandas converts the returned Django QuerySet into a DataFrame. Scikit-learn applies historical regression modeling to forecast future variables.
6. **Template Rendering:** The processed data (or JSON predictions) are securely injected into the HTML templates.
7. **Client Response:** TailwindCSS and Chart.js visually render the HTTP response on the user's viewport.

---

## 3. Database Design (Entity-Relationship)

The PostgreSQL database is fully normalized, highly relational, and leverages foreign key constraints to map the physical hospital structure.

### 3.1 Core Entity Map
* **User (Abstracted):** Extends Django's native authentication model.
* **Patient:** Primary key `patient_id` (e.g., `BMH0001`). Stores demographics, vitals, and acts as the root node for medical files.
* **Department:** Represents structural wards (e.g., Cardiology, Orthopedics).
* **Doctor / Nurse:** Inherit basic staff profiles but restrict operational privileges based on role. Linked to specific `Departments`.
* **Visit (The Central Log):**
  * Links `Patient` $\xrightarrow{1:N}$ `Visit` $\xleftarrow{N:1}$ `Doctor`.
  * Records the timestamp (`visit_date`), observed `Symptoms`, active `Case_Type`, and issued `Medicines`.

### 3.2 Inventory & Financial Entity Map
* **Medicine:** The root inventory log. Holds `stock_quantity`, `price`, and `min_stock_level`.
* **PharmacyBill:** Auto-generated financial record linked to a `Patient`.
* **PrescriptionLine:** Bridge table linking a `PharmacyBill` to specific `Medicine` quantities deducted during a visit.

---

## 4. Sub-System Component Design

### 4.1 The AI & Analytics Sub-System
The most advanced component of HMAS is the decoupled Artificial Intelligence forecasting module located at `/ml/predict_load.py`. 

**A. Load Forecasting Engine**
* **Input:** Millions of rows of historical `Visit` timestamps categorized by `Department`.
* **Process:** Groups daily organic hospital traffic into normalized monthly aggregation vectors.
* **Algorithm:** Feeds vectors into `sklearn.linear_model.LinearRegression`. It purposefully slices off the current active month from the training set to prevent anomalous negative-sloping caused by incomplete contemporary data. 
* **Output:** A JSON array projecting the precise mathematical expected patient footprint for $Months_{Y+1}, Months_{Y+2}$, and $Months_{Y+3}$.

**B. Smart Staff Diagnostic Engine**
* **Input:** The active census of total registered `Doctors` and `Nurses` cross-referenced with the last 250,000 clinic visits.
* **Process:** Computes live `Load/Doc` and `Load/Nurse` diagnostic ratios.
* **Output:** Flags departments critically breaching safety thresholds ("Overloaded") against under-performing financial sinks ("Underutilized").

### 4.2 The File & Vault Sub-System
* **Input:** Users uploading encrypted PDFs, JPEGs, or direct text parameters.
* **Process:** Handled by Django's `MEDIA_ROOT`. The `PatientDocument` model validates the payload, storing the absolute local file path (`/media/patient_documents/YYYY/MM/DD/`) inside PostgreSQL rather than bloat-storing binary data.
* **Safety:** Protected by standard Django CSRF security tokens preventing cross-site hijacking.

---

## 5. Security & Access Control Design

HMAS implements strict **Role-Based Access Control (RBAC)** across the system hierarchy defined inherently during user creation:

1. **System Admin:** The root entity. Has full raw DB access and permission to trigger global database migrations.
2. **Physician Role (`@login_required(doctor_only)`):** Confined to their specific roster of associated `Visits`. They can view the AI forecasting model explicitly filtered exclusively for their own localized workload.
3. **Nursing Role:** Read-only access to wide-scale hospital shift rotations and limited access to ingest root patient demographics.
4. **Pharmacist Role:** Hard-fenced into the `pharmacy` module. Cannot access predictive analytics for hospital footprints, but have full access to predictive AI modules projecting `Medicine` depletion timelines.
