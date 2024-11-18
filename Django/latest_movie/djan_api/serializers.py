# from rest_framework import serializers
# from djan.models import *

# class UserSerializer(serializers.ModelSerializer):
#     questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'questions']

# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['id', 'subject', 'content', 'game_date']

