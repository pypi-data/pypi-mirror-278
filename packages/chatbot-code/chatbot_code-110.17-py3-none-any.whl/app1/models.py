from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    chatbot_name = models.TextField()
    chatbot_description = models.TextField()
    file = models.FileField(upload_to='uploaded_files/')
    content = models.TextField() 
    link = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class ChatSession(models.Model):
    session_id = models.CharField(max_length=32)
    session_start_time = models.DateTimeField()
    question = models.TextField()
    question_asked_time = models.DateTimeField()
    answer = models.TextField()
    user_identifier = models.CharField(max_length=32)
    retrieval_count = models.IntegerField(default=1)
    verification_count = models.IntegerField(default=0)
    positive_count = models.IntegerField(default=0)  # Field to store positive feedback count
    negative_feedback_count = models.IntegerField(default=0)
    verified_by = models.ManyToManyField(User, related_name='verified_questions', blank=True)
    cluster_id = models.CharField(max_length=64, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file_id = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f"Session ID: {self.session_id}, User: {self.user_identifier}, Question: {self.question}"

class Feedback(models.Model):
    session_id = models.CharField(max_length=150)  
    user_identifier = models.CharField(max_length=32)
    question = models.TextField()
    answer = models.TextField()
    feedback = models.BooleanField()  # True for positive feedback, False for negative
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for '{self.question}'"
    

class SimilarQuestion(models.Model):
    question = models.TextField()
    answer = models.TextField()
    session_id = models.CharField(max_length=50)
    user_session_id = models.CharField(max_length=50)
    cluster_id = models.CharField(max_length=64, blank=True, null=True)
    session_start_time = models.DateTimeField()
    question_asked_time = models.DateTimeField()
    user_name = models.CharField(max_length=100)
    file_id = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f"Session ID: {self.session_id}, User: {self.user_session_id}, Question: {self.question}"
    

