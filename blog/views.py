from rest_framework import viewsets, permissions, throttling
from .models import Blog
from .serializers import BlogSerializer


# Create your views here.
class BlogView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    throttle_classes = [throttling.AnonRateThrottle, throttling.UserRateThrottle]
    ordering_fields = ["title", "created_on"]
    search_fields = ["author", "title"]

    # restrict access to create, edit, and delete blog post by authenticated users only
    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
