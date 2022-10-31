from rest_framework import generics
from api_app_1.models import Students
from api_app_1.serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
# Create your views here.

####________ GET ALL STUDENTS DETAILS AND CREATE STUDENT________####
class StudentGeneric(generics.ListCreateAPIView):
    queryset          = Students.objects.all()
    serializer_class  = StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data={"message": "Student Created successfully."})
       
# ####________DELETE STUDENT AND UPDATE STUDENTS________####
class DeleteStudentGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset          = Students.objects.all()
    serializer_class  = StudentSerializer

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return Response(data={"message": "Student Deleted successfully."})

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": "Student Updated successfully."})





