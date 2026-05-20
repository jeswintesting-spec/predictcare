import os
import django
import sys
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmh_project.settings')
django.setup()

from hospital.models import PatientDocument, Patient

def test_document_upload():
    print("Testing PatientDocument model...")
    # Find a patient
    patient = Patient.objects.first()
    if not patient:
        print("No patients found in DB. Test skipped.")
        return

    # Create dummy file content
    file_content = b"This is a test medical report content."
    dummy_file = SimpleUploadedFile("test_report.pdf", file_content, content_type="application/pdf")

    # Create document record
    doc = PatientDocument.objects.create(
        patient=patient,
        document_name="Initial Blood Test",
        document_type="Lab Report",
        file=dummy_file,
        notes="Automated test upload"
    )

    print(f"Successfully created: {doc}")
    
    # Retrieve it back
    retrieved_doc = PatientDocument.objects.get(id=doc.id)
    print(f"Retrieved Document Name: {retrieved_doc.document_name}")
    print(f"File Path stored in DB: {retrieved_doc.file.name}")
    print(f"File Size: {retrieved_doc.file.size} bytes")
    
    # Cleanup dummy test data
    doc.file.delete()
    doc.delete()
    print("Test passed! Cleaned up dummy data.")

if __name__ == '__main__':
    test_document_upload()
