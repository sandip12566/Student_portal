from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.singin, name="login"),
    path('register/', views.register, name="register"),
    path('forgetPassword/', views.forget_password, name="forgetPassword"),
    path('resetPassword/', views.reset_password, name="resetPassword"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.profile, name="profile"),
    path('notes/', views.notes, name="notes"),
    path('notes-detail/', views.notesDetail, name="notesDetail"),
    path('delete_note/<int:pk>', views.delete_note, name="delete-note"),
    path('homework/', views.homework, name="homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update-homework"),
     path('delete_homework/<int:pk>', views.delete_homework, name="delete-homework"),
    path('todo/', views.todo, name="todo"),
    path('update_todo/<int:pk>',views.update_todo,name="update-todo"),
     path('delete_todo/<int:pk>',views.delete_todo,name="delete-todo"),
    path('books/', views.books, name="books"),
    path('dictionary/', views.dictionary, name="dictionary")
]