from .models import Doctor, Nurse, HospitalConfiguration

def hospital_roles(request):
    # Always provide hospital config, even to unauthenticated users (for login page etc if needed)
    config = HospitalConfiguration.get_solo()
    
    if not request.user.is_authenticated:
        return {'hospital_config': config}
        
    user = request.user
    
    # Persistent flags for the template sidebar
    is_doctor = user.groups.filter(name='Doctor').exists() or Doctor.objects.filter(staff_id=user.username).exists()
    is_reception = user.groups.filter(name='Receptionist').exists() or user.username == 'receptionist'
    is_pharmacy = user.groups.filter(name='Pharmacy').exists() or user.username == 'pharmacy'
    
    # Administrator has access to everything
    if user.is_superuser:
        is_doctor = True
        is_reception = True
        is_pharmacy = True

    return {
        'hospital_config': config,
        'is_doctor': is_doctor,
        'is_reception': is_reception,
        'is_pharmacy': is_pharmacy,
        'is_staff_member': user.is_staff or is_doctor or is_reception or is_pharmacy
    }
