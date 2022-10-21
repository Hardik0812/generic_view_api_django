
from rest_framework import generics
from api_app_1.models import Students
from api_app_1.serializers import StudentSerializer


# Create your views here.

####________ GET ALL STUDENTS DETAILS________####
class StudentGeneric(generics.ListAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer


####________CREATE STUDENT________####    
class CreateStudentGeneric(generics.ListCreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

####________DELETE STUDENT________####


