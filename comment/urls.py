# django 库
from django.urls import path
# 本地库
from .import views

urlpatterns = [
    # localhost:8000/comment/
    path('submit_comment/',views.submit_comment,name="submit_comment"),
]
