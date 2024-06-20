from django.urls import include, path, reverse_lazy
from . import views
from .models import Test, Result

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('add-test/', views.add_test, name='add_test'),
    path('delete-test/<int:pk>', views.DeleteView.as_view(model=Test, success_url=reverse_lazy('profile')),
         name='delete_test'),
    path('delete-result/<int:pk>', views.DeleteView.as_view(model=Result, success_url=reverse_lazy('profile')),
         name='delete_result'),
    path('start-test/<int:test_id>/', views.start_test, name='start_test'),
    path('solve/<int:test_id>/<int:question_id>', views.get_question, name='question'),
    path('result/<int:result_id>', views.ShowResult.as_view(), name='result'),
    path('profile/', views.show_profile, name='profile')
]
