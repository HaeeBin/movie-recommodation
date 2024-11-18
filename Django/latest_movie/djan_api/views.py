# from djan.models import Question
# from djan_api.serializers import QuestionSerializer
# from rest_framework import status

# from rest_framework.response import Response
# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from django.contrib.auth.models import User
# from djan_api.serializers import UserSerializer
# from rest_framework import generics

# class QuestionList(generics.ListCreateAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

# class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer