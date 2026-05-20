# hospital/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("hub/", views.hub_view, name="hub"),
    path("patient-dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/reception/", views.reception_dashboard, name="reception_dashboard"),
    path("dashboard/reception/predictions/", views.reception_predictions_view, name="reception_predictions"),
    path("dashboard/doctor/", views.doctor_dashboard, name="doctor_dashboard"),
    path("dashboard/doctor/analytics/", views.doctor_analytics, name="doctor_analytics"),
    path("dashboard/doctor/specialized/", views.doctor_specialized_insights, name="doctor_specialized"),
    path("staff/", views.staff_view, name="staff_dashboard"),
    path("add-staff/", views.add_staff, name="add_staff"),
    path("edit-staff/", views.edit_staff, name="edit_staff"),
    path("delete-staff/", views.delete_staff, name="delete_staff"),
    
    path("departments/", views.department_dashboard, name="department_dashboard"),
    path("add-department/", views.add_department, name="add_department"),
    path("edit-department/", views.edit_department, name="edit_department"),
    path("delete-department/", views.delete_department, name="delete_department"),
    
    path("reports/", views.reports_view, name="reports"),
    path("api/reports/", views.api_reports, name="api_reports"),
    path("export-reports/", views.export_reports, name="export_reports"),

    path("load-patients/", views.load_patients, name="load_patients"),
    path("add-patient/", views.add_patient, name="add_patient"),
    path("delete-patient/", views.delete_patient, name="delete_patient"),
    path("edit-patient/", views.edit_patient, name="edit_patient"),
    path("add-visit/", views.add_visit, name="add_visit"),
    path("delete-visit/", views.delete_visit, name="delete_visit"),
    path("edit-visit/", views.edit_visit, name="edit_visit"),
    path("load-visits/<str:patient_id>/", views.load_visits, name="load_visits"),
    path("export-visits/", views.export_visits, name="export_visits"),
    path("predict-load/", views.predict_load, name="predict_load"),
    path("prediction/", views.show_prediction, name="prediction"),
    path("predict-load-over-time/", views.predict_load_over_time, name="predict_load_over_time"),
    path("get-suggestions/", views.get_suggestions, name="get_suggestions"),
    path("analytics-data/", views.analytics_data, name="analytics_data"),
    path("analytics-drilldown/", views.analytics_drilldown, name="analytics_drilldown"),
    # path("", views.login_view, name="login"), -> Removed
    # path("logout/", views.logout_view, name="logout"), -> Removed
    path("", views.hub_view, name="home_redirect"), # Root goes to Hub (which requires login)
    path("planning-data/", views.resource_planning, name="resource_planning"),
    path("schedule/", views.schedule_view, name="schedule"),
    path("load-schedules/", views.load_schedules, name="load_schedules"),
    path("edit-schedule/", views.edit_schedule, name="edit_schedule"),
    path("settings/", views.edit_hospital_config, name="hospital-settings"),
]