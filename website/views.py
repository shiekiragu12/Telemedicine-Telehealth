from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def signin(request):
    return render(request, 'auth/signin.html', {})

def signup(request):
    return render(request, 'auth/sign-up.html', {})

# Services nav-links
def service(request):
    return render(request, 'services/services.html', {})

def emergencies(request):
    return render(request, 'services/emergencies.html', {})

def birthingcare(request):
    return render(request, 'services/birthing-care.html', {})

def cancercare(request):
    return render(request, 'services/cancer-care.html', {})

def familymedicine(request):
    return render(request, 'services/family-medicine.html', {})

def emergencymedicine(request):
    return render(request, 'services/emergency-medicine.html', {})

def laboratiescenter(request):
    return render(request, 'services/laboraties-center.html', {})

def onlinereferral(request):
    return render(request, 'services/online-referral.html', {})

def firstaid(request):
    return render(request, 'services/first-aid.html', {})

# about
def about(request):
    return render(request, 'about.html', {})

# Health in Hand
def health(request):
    return render(request, 'health/health.html', {})

def diseaselist(request):
    return render(request, 'health/disease-list.html', {})

def healthtopic(request):
    return render(request, 'health/health-topic.html', {})

def healthyliving(request):
    return render(request, 'health/healthy-living.html', {})

def location(request):
    return render(request, 'health/medical-facilities.html', {})