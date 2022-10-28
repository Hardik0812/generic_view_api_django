from django.urls import path

from api_app_1.views import StudentGeneric,DeleteStudentGeneric


 #### _________ ENDPOINT ________ ####
urlpatterns = [
   
   path('students/',StudentGeneric.as_view(),name='get_students'),
   path('deletestudent/<pk>/',DeleteStudentGeneric.as_view(),name='delete_students'),
  
]
