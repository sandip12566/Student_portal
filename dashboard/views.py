from django.shortcuts import render, redirect
from .models import *
from . forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
import requests
import wikipedia
from django.urls import reverse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def singin(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user_object = User.objects.filter(username=username).first()
        error_msg = ""
        if user_object is None:
            error_msg = "User not found. Please try again"
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                error_msg = "Wrong password."
            else:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html', {'error': error_msg})

def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('confirm_password')
        error_msg = None
        if password != re_password:
            error_msg = "Hey! Your Password Not Matched"
        elif User.objects.filter(username=username).first():
            error_msg = "This Username Has Been Already Registered"
        elif len(password) < 8:
            error_msg = "Password must Be 8 character"

        if not error_msg:
            user_object = User.objects.create(username=username, email=email)
            user_object.set_password(password)
            user_object.save()
            messages.success(request,f"Account created for {username} !!")
            return redirect('home')
        else:
            data = {
                "error": error_msg,
            }
            return render(request, 'register.html', data)

# def logout(request):
#     return render(request, 'logout.html')

def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user_object = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            user_object = None
        error_msg = ""
        if user_object is None:
            error_msg = "User not found. Please try again."
            return render(request, 'forgetPassword.html', {'error': error_msg})
        else:
            reset_password_url = reverse('resetPassword') + f'?user_id={user_object.id}'
            return redirect(reset_password_url)
    else:
        return render(request, 'forgetPassword.html')
    
def reset_password(request):
    if request.method == 'POST':
        user_id = request.GET.get('user_id')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        error_msg = ""
        if new_password != confirm_password:
            error_msg = 'New password and confirm password do not match.'
        else:
            user_obj = authenticate(request, username=user.username, password=old_password)
            if user_obj is not None:
                # set the new password and log the user in
                user_obj.set_password(new_password)
                user_obj.save()
                return redirect('login')
            else:
                error_msg = "Invalid old password."
        return render(request, 'resetPassword.html', {'error': error_msg})
    else:
        return render(request, 'resetPassword.html')

@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    print(request.user.username)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    if len(todos)==0:
        todos_done=True
    else:
        todos_done=False
    context={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done,
        'user_detail':request.user
    }
    return render(request, "profile.html", context)

@login_required
def notes(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        # print(title, description)
        try:
            # create a user object
            note_object = Notes.objects.create(user=request.user, title=title, description=description)
            note_object.save()
            messages.success(request, f"Notes Added from {request.user.username} Successfully")
            return redirect('notesDetail')
        except Exception as e:
            print(e)
    return render(request, 'notes.html')

@login_required
def notesDetail(request):
    notes = Notes.objects.filter(user=request.user)
    return render(request, 'notes_detail.html', {'notes':notes})

@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notesDetail")

@login_required
def homework(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due = request.POST.get('due')
        finished = request.POST['is_finished']
        # print(subject, title, description, due, finished)
        if finished == "yes":
            finished = True
        else:
            finished = False
        
        try:
            # create a user object
            homework_object = Homework.objects.create(user=request.user, subject=subject, title=title, description=description, date=due, is_finished=finished)
            homework_object.save()
            return redirect('homework')
        except Exception as e:
            print(e)
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks)==0:
        homework_done= True
    else:
        homework_done=False
    return render(request, 'homework.html', {'homeworks':homeworks, 'homework_done':homework_done})

@login_required
def update_homework(request, pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

@login_required
def todo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        due = request.POST.get('due')
        finished = request.POST['is_finished']
        # print(title, due, finished)
        if finished == "yes":
            finished = True
        else:
            finished = False
        try:
            # create a user object
            todo_object = Todo.objects.create(user=request.user, title=title, date=due, is_finished=finished)
            todo_object.save()
            return redirect('todo')
        except Exception as e:
            print(e)

    todos = Todo.objects.filter(user=request.user)
    if len(todos)==0:
        todo_done = True
    else:
        todo_done = False
    return render(request, 'todo.html', {"todos": todos, "todo_done": todo_done})

@login_required
def update_todo(request, pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

@login_required
def books(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                 'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                 'description':answer['items'][i]['volumeInfo'].get('description'),
                 'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                 'categories':answer['items'][i]['volumeInfo'].get('categories'),
                 'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                 'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                 'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'books.html',context)
    else:
        form=DashboardForm()
    form=DashboardForm()
    context={'form':form}
    return render(request,'books.html', context)

@login_required
def dictionary(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        print("In")
        p="input"
        phonetics=answer[0]['phonetics'][0]['text']
        audio=answer[0]['phonetics'][0]['audio']
        definition=answer[0]['meanings'][0]['definitions'][0]['definition']
        # example=answer[0]['meanings'][0]['definitions'][0]['example']
        synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
        context={
                'url':url,
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                # 'example':example,
                'synonyms':synonyms
            }
        context2={
            'form':form,
            'results':result_list
        }
        result_list.append(context)
        print(url)
        print(text)
            # print(context)
        return render(request,'dictionary.html',context)
          
        # except:
        #     print("sai")
        #     context={
        #         'form':form,
        #         input:''
        #     }
        return render(request,'dictionary.html',context)
    else:
        form=DashboardForm()
        context1={'form':form}
   
    return render(request,'dictionary.html',context1)

