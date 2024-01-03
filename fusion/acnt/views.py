from django.shortcuts import render
from .serializers import ClientRegisterSerializer,FreelancerRegisterSerializer,ClientLoginSerializer,FreelancerLoginSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

# Create your views here.

class ClientRegisterView(GenericAPIView):
    serializer_class = ClientRegisterSerializer

    def post(self, request):
        client_data = request.data
        serializer = self.serializer_class(data = client_data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            user = serializer.data
            return Response({
                    'data' : user,
                    'message' : f'HI! {serializer.data["first_name"]}, Account created successfull'
                }, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class FreelanceRegisterView(GenericAPIView):
    serializer_class = FreelancerRegisterSerializer
    def post(self, request):
        freelance_data = request.data
        serializer = self.serializer_class(data = freelance_data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            user = serializer.data
            return Response({
                    'data' : user,
                    'message' : f'HI! {serializer.data["first_name"]} , Account created successfull'
                }, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
class ClientLoginView(GenericAPIView):
    serializer_class = ClientLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data,context = {'requset':request})
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class FreelancerLoginView(GenericAPIView):
    serializer_class = FreelancerLoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data,context = {'requset':request})
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)