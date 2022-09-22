from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post
from .serializers import PostSerializer, UserSerializer


# Create your views here.
@csrf_exempt
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Sign Up': '/signup/',
        'Log In': '/login/',
        'Log Out': '/logout/',
        'List': '/list/',
        'Details': '/view/<str:pk>/',
        'Create': '/create/',
        'Update': '/edit/<str:pk>/',
        'Delete': '/delete/<str:pk>/',
    }
    return Response(api_urls)


# User registration
@csrf_exempt
@api_view(['POST'])
def signUp(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        if data['username'] != authenticate(request, username=data['username']):
            user = User.objects.create(first_name=serializer.data['first_name'], last_name=serializer.data['last_name'], username=serializer.data['username'], email=serializer.data['email'])
            user.set_password(serializer.data['password'])
            user.save()
            return Response('Signed Up successfully', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Log in user
@csrf_exempt
@api_view(['POST'])
def logIn(request):
    data = request.data
    if request.method == 'POST':
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response('Logged in successfully', status=status.HTTP_202_ACCEPTED)
        except:
            return Response('User does not exist!', status=status.HTTP_401_UNAUTHORIZED)

# Log out user
@csrf_exempt
@api_view(['GET'])
def logOut(request):
    logout(request)
    return Response('Logged out successfully', status=status.HTTP_200_OK)


#  CRUD - Read all function
@csrf_exempt
@api_view(['GET'])
def postList(request):
    post = Post.objects.all()
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#  CRUD - Read one function
@csrf_exempt
@api_view(['GET'])
def postView(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

#  CRUD - Create function
@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def postCreate(request, format=None):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('Post created successfully', status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

#  CRUD - Update function
@csrf_exempt
@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser])
def postEdit(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('Post updated successfully', status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


# class PostEdit(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def put(self, request, pk):
#         post = Post.objects.get(id=pk)
#         serializer = PostSerializer(instance=post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response('Post updated successfully', status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

# class PostEdit(generics.RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     parser_classes = (MultiPartParser, FormParser)
#     def put(self, request, pk):
#         post = Post.objects.get(id=pk)
#         serializer = self.serializer_class(instance=post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response('Post updated successfully', status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


#  CRUD - Delete function
@csrf_exempt
@api_view(['DELETE'])
def postDelete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response('Post deleted successfully!', status=status.HTTP_202_ACCEPTED)
