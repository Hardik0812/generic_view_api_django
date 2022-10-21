from django.urls import path,include

from api_app_1.views import StudentGeneric,CreateStudentGeneric



 #### _________ ENDPOINT ________ ####
urlpatterns = [
   
   path('get_students/',StudentGeneric.as_view(),name='get_students'),
   path('create_students/',CreateStudentGeneric.as_view(),name='create_students')
   
    
]
