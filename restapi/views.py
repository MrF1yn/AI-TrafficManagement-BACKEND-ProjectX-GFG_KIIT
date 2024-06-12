from django.shortcuts import render
import os
import shutil

from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
def upload_video(request):
    traffic_lights = []

    if request.FILES['video_file']:
        video_files = request.FILES.getlist('video_file')
        fs = FileSystemStorage()
        video_dir = 'uploaded_videos/' + request.user.username + '/'
        if fs.exists(video_dir) and len(os.listdir(video_dir)) > 3:
            # if fs.exists(video_dir):
            #     shutil.rmtree(video_dir)
            return HttpResponse("FILE UPLOAD LIMIT REACHED", status=400)

        uploaded_file_urls = []
        for video_file in video_files:
            filename = fs.save(video_dir + video_file.name, video_file)
            print(video_file.name)
            uploaded_file_urls.append(fs.path(filename))
            print("Uploaded successfully")
        return HttpResponse("SUCCESS")
    return HttpResponse("Incomplete Data, No Video File", status=400)


@api_view(['GET'])
def clear_uploads(request):
    fs = FileSystemStorage()
    video_dir = 'uploaded_videos/' + request.user.username
    if fs.exists(video_dir):
        shutil.rmtree(video_dir)
    return HttpResponse("SUCCESS")


@api_view(['DELETE'])
def delete_video(request):
    if request.data and request.data['name']:
        fs = FileSystemStorage()
        video_dir = 'uploaded_videos/' + request.user.username + '/' + request.data['name']
        if fs.exists(video_dir):
            fs.delete(video_dir)
    return HttpResponse("SUCCESS")


@api_view(['GET'])
def get_uploads(request):
    fs = FileSystemStorage()
    video_dir = 'uploaded_videos/' + request.user.username + '/'
    if fs.exists(video_dir):
        [folders, files] = fs.listdir(video_dir)
        return Response(files)
    return Response([])
