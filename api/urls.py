from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from .views import *

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'users', UserViewSet)

router.register(r'product-types', ProductTypeViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

router.register(r'locations/counties', CountyViewSet)
router.register(r'locations/constituencies', ConstituencyViewSet)

router.register(r'emailconfigs', EmailConfigViewSet)
router.register(r'emails', EmailViewSet)

router.register(r'conditions', ConditionViewSet)
router.register(r'illness', IllnessViewSet)

router.register(r'specialities', SpecialityViewSet)

router.register(r'facilities', FacilityViewSet)
router.register(r'types/facilities', FacilityTypeViewSet)

router.register(r'qualifications', QualificationViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'medical-reports', EncounterViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'shared-prescriptions', SharedPrescriptionViewSet)
router.register(r'prescription-orders', PrescriptionOrderViewSet)

router.register(r'topics', TopicViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'replies', ReplyViewSet)

# Main app routes
# Contact messages
router.register(r'contact/contact-form/messages', ContactViewSet)
router.register(r'contact/schedule-form/messages', ScheduleViewSet)
router.register(r'contact/analytic-form/messages', AnalyticViewSet)
router.register(r'contact/apply-form/messages', ApplyViewSet)
router.register(r'contact/equip-form/messages', EquipViewSet)
router.register(r'contact/telehealth-form/messages', TelehealthViewSet)
router.register(r'contact/topbutton-form/messages', TopButtonViewSet)
router.register(r'contact/book-form/messages', BookViewSet)
router.register(r'contact/firstaid-form/messages', FirstAidViewSet)

# App settings
router.register(r'appconfigs', AppConfigViewSet)

schema_view = get_swagger_view(title='Resq247 API')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view, name='api-docs'),
    # path('docs/', TemplateView.as_view(
    #     template_name='swagger.html',
    #     extra_context={'schema_url': 'openapi-schema'}
    # ), name='swagger-ui')
]
