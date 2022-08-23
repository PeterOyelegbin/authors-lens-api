from django.shortcuts import render
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


# Create your views here.
@csrf_exempt
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/list/',
        'Details': '/view/<str:pk>/',
        'Create': '/create/',
        'Update': '/edit/<str:pk>/',
        'Delete': '/delete/<str:pk>/',
    }
    return Response(api_urls)

#  CRUD - Read all function
@csrf_exempt
@api_view(['GET'])
def postList(request):
    post = Post.objects.all()
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)

#  CRUD - Read one function
@csrf_exempt
@api_view(['GET'])
def postView(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

#  CRUD - Create function
@csrf_exempt
@api_view(['POST'])
def postCreate(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#  CRUD - Update function
@csrf_exempt
@api_view(['POST'])
def postEdit(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#  CRUD - Delete function
@csrf_exempt
@api_view(['DELETE'])
def postDelete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response('Item successfully deleted!')
    