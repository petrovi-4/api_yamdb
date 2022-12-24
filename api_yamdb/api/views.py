from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from seriaizers import CommentSerializer, ReviewSerializer

from users.permissions import IsAuthorOrModeratorOrAdmin

from .models import Review, Comment


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrModeratorOrAdmin,)
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrModeratorOrAdmin,)
    pagination_class = LimitOffsetPagination
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_queryset = Review.objects.filter(title=title_id)
        return review_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)
