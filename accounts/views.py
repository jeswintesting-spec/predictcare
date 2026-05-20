from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from hospital.models import Doctor, Department

def logout_view(request):
    logout(request)
    return redirect('/')

class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass all doctors to the template for the dropdown
        context['doctors'] = Doctor.objects.select_related('department').all().order_by('doctor_name')
        context['departments'] = Department.objects.all().order_by('name')
        
        # Pass Staff/Admin users
        from django.contrib.auth.models import User
        from django.db.models import Q
        # Fetch users who are Superusers OR in Receptionist/Pharmacy groups
        # Exclude doctors (assuming they are in Doctor group)
        context['staff_users'] = User.objects.filter(
            Q(is_superuser=True) | 
            Q(groups__name__in=['Receptionist', 'Pharmacy'])
        ).exclude(groups__name='Doctor').distinct().order_by('username')
        
        return context
