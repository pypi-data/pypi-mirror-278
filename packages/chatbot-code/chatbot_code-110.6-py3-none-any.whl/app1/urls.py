from django.urls import path
from .views import index,chat,file_queries_log,chatbot_delete,unique_questions_table,chatbot_details,  upload_file,clear_all_sessions,upload_csv,custom_login_view,dashboard_view,qna_create,logout, qna_update,qna_delete,qna_delete_log,submit_feedback,verify_question,dashboard_log_question,file_queries
# ,reset_session_timeout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('upload_file/', upload_file, name='upload_file'),
    path('chat/<str:user_name>/<int:file_id>/', chat, name='chat'),
    path('clear-sessions/', clear_all_sessions, name='clear_all_sessions'),
    # path('reset_session_timeout/', reset_session_timeout, name='reset_session_timeout'),
    path("admin_login/", custom_login_view, name="admin_login"),
    # path("admin_login/", CustomLoginView.as_view(), name="admin_login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("log_questions/", dashboard_log_question, name="dashboard_log_questions"),
    path("submit_feedback/", submit_feedback, name="submit_feedback"),
    path('new/', qna_create, name='qna_create'),
    path('edit/<int:pk>/', qna_update, name='qna_update'),
    path('delete/<int:pk>/', qna_delete, name='qna_delete'),
    path('delete_log/<int:pk>/', qna_delete_log, name='qna_delete_log'),
    path('chatbot_delete/<int:pk>/', chatbot_delete, name='chatbot_delete'),
    path('verify/<str:session_id>/<int:file_id>/', verify_question, name='verify_question'),
    path('logout/', logout, name='logout'),
    path('',index,name='index'),
    path("unique_questions/", unique_questions_table, name="unique_questions"),


    path('file-details/<int:file_id>/', file_queries, name='file_details'),
    path('file-details_log/<int:file_id>/', file_queries_log, name='file_details_log_questions'),



    path('chat_sessions/<int:file_id>/', chatbot_details, name='chatbot_details'),
    path('upload-csv/', upload_csv, name='upload_csv'),


]
