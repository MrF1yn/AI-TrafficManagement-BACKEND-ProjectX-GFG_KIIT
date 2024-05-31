from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from . import eval

# Create your views here.
def home(request):
    return HttpResponse("Hello home")

def errorpage(request):
    return HttpResponse("Bad Credentials")

# Addtion of email authentication and activation

def signin(request):
    if request.method == "POST":
        name = request.POST['name']
        pass1 = request.POST['password']
        # print("got details")
        user = authenticate(username=name, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            # print("Bad ceds")
            messages.error(request, "Bad Credentials")
            # ask what to do here
            return redirect('errorpage')



    return render(request, 'signin/login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(username, email, password)
        myuser.save()

        print("Your account has been successfully created")

        messages.success(request, "Your account has been successfully created")
        return redirect('signin')

    return render(request, 'signin/register.html')

def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def user_func(request):
    return render(request, "user/user.html")
    # return HttpResponse("user html")

def results_func(request):
    return HttpResponse("result html")

def upload_video(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_files = request.FILES.getlist('video_file')
        if len(video_files) < 4:
            return HttpResponse("Incomplete Data")
        uploaded_file_urls = []
        fs = FileSystemStorage()
        for video_file in video_files:
            filename = fs.save(video_file.name, video_file)
            print(video_file.name)
            uploaded_file_urls.append(fs.path(filename))
            print("Uploaded successfully")

        eval.evaluate(uploaded_file_urls)
    # return redirect('/signin/results')
        # Do something with the uploaded file, e.g., save it to a model
        # return render(request, 'your_template.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
    return HttpResponse("Not uploaded")