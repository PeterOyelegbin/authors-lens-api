from rest_framework import viewsets, permissions, throttling
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Blog
from .serializers import BlogSerializer


# Create your views here.
class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    throttle_classes = [throttling.AnonRateThrottle, throttling.UserRateThrottle]
    ordering_fields = ["title", "created_on"]
    search_fields = ["author", "title"]

    # restrict access for create, edit, and delete to authenticated users only
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    # update blog owned by current authenticated user
    @method_decorator(csrf_exempt)
    def update(self, request, *args, **kwargs):
        if self.queryset.filter(author=self.request.user):
            return super().update(request, *args, **kwargs)
        else:
            return Response({"Message": "Permission required."}, 401)

    # delete blog owned by current authenticated user
    def destroy(self, request, *args, **kwargs):
        if self.queryset.filter(author=self.request.user):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({"Message": "Permission required."}, 401)
