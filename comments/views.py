from rest_framework import generics, permissions
from pudrf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer


