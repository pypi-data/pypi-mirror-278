from django.contrib import admin
import requests
from .models import UploadedFile,ChatSession,Feedback,SimilarQuestion
import csv
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import reverse

admin.site.register(UploadedFile),
# admin.site.register(ChatSession),
admin.site.register(Feedback)
admin.site.register(SimilarQuestion)



class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'session_start_time', 'question', 'question_asked_time', 'answer', 'user_identifier', 'retrieval_count','verification_count','cluster_id')
    actions = ['download_csv','upload_csv']

    def download_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="chatsessions.csv"'
        writer = csv.writer(response)
        writer.writerow(['session_id', 'session_start_time', 'question', 'question_asked_time', 'answer', 'user_identifier', 'retrieval_count', 'verification_count','cluster_id'])
        for session in queryset:
            writer.writerow([session.session_id,session.session_start_time,session.question,session.question_asked_time,session.answer,session.user_identifier,session.retrieval_count,session.verification_count,session.cluster_id])
        return response
    download_csv.short_description = "Download selected sessions as CSV"






admin.site.register(ChatSession, ChatSessionAdmin)

