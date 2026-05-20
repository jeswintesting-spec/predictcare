# 🛠 PredictCare Database Access Guide

You have three main ways to see and manage your hospital data.

## 1. Django Admin Interface (Easiest)
This is the built-in web interface we enabled. It lets you view, search, and edit data without writing SQL.

- **URL**: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- **Username**: `admin`
- **Password**: `admin123`

*If you don't see the "HOSPITAL" section, try restarting the server.*

---

## 2. PostgreSQL GUI Tool (Recommended for Developers)
You can use apps like **Postico 2** (Mac), **PgAdmin 4**, or **DBeaver** to view the raw tables.

**Connection Details:**
- **Host**: `localhost`
- **Port**: `5432`
- **User**: `bmh_admin`
- **Password**: `bmh_secure_2026`
- **Database**: `bmh_hospital`

---

## 3. Command Line (Terminal)
You can run raw SQL queries directly from your terminal.

**Command to enter the database shell:**
```bash
psql -h localhost -U bmh_admin -d bmh_hospital
```
*(Enter password `bmh_secure_2026` when prompted)*

**Useful Commands inside psql:**
- `\dt` : List all tables
- `SELECT * FROM hospital_doctor;` : Show all doctors
- `\q` : Quit
