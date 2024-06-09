from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('add-test/', views.add_test, name='add_test'),
    path('start-test/<int:test_id>/', views.start_test, name='start_test'),
    path('solve/<int:test_id>/<int:question_id>', views.get_question, name='question'),
    path('result//<int:result_id>', views.ShowResult.as_view(), name='result')
]
