import logging
from uuid import UUID

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .filters import ArticleFilter
from .models import Article, ArticleView, Clap
from .pagination import ArticlePagination
from .permissions import IsOwnerOrReadOnly
from .serializers import ArticleSerializer, ClapSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ArticlePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ArticleFilter
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        # Set the author to the currently authenticated user
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            # Wrap the response in the desired format
            response_data = {
                "status": "success",
                "message": "Article created successfully.",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error creating article: {str(e)}", exc_info=True)
            return Response({
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}",
                "data": None,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                response_data = {
                    "status": "success",
                    "message": "Articles retrieved successfully.",
                    "data": self.get_paginated_response(serializer.data).data,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            serializer = self.get_serializer(queryset, many=True)
            response_data = {
                "status": "success",
                "message": "Articles retrieved successfully.",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving articles: {str(e)}", exc_info=True)
            return Response({
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}",
                "data": None,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)
        if "banner_image" in self.request.FILES:
            if (
                instance.banner_image
                and instance.banner_image.name != "/profile_default.png"
            ):
                default_storage.delete(instance.banner_image.path)
            instance.banner_image = self.request.FILES["banner_image"]
            instance.save()

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({
                "status": "success",
                "message": "Article updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error updating article: {str(e)}", exc_info=True)
            return Response({
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ... keep your existing retrieve and destroy methods ...
class ArticleBulkDeleteView(generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        ids = request.data.get("ids", [])
        if not ids:
            return Response({
                "status": "error",
                "message": "No IDs provided."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            uuids = [UUID(id) for id in ids]
            articles = Article.objects.filter(id__in=uuids)
            articles_deleted = articles.count()
            articles.delete()
            return Response({
                "status": "success",
                "message": f"{articles_deleted} articles deleted successfully.",
                "data": {}
            }, status=status.HTTP_200_OK)
        except ValidationError as ve:
            logger.error(f"Validation error: {str(ve)}", exc_info=True)
            return Response({
                "status": "error",
                "message": f"Validation error: {str(ve)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Article.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Some articles do not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting articles: {str(e)}", exc_info=True)
            return Response({
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClapArticleView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Clap.objects.all()
    serializer_class = ClapSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        if Clap.objects.filter(user=user, article=article).exists():
            return Response({
                "status": "error",
                "message": "You have already clapped on this article."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            clap = Clap.objects.create(user=user, article=article)
            clap.save()
            return Response({
                "status": "success",
                "message": "Clap added to article.",
                "data": {}
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error adding clap: {str(e)}", exc_info=True)
            return Response({
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)

        try:
            clap = get_object_or_404(Clap, user=user, article=article)
            clap.delete()
            return Response({
                "status": "success",
                "message": "Clap removed from article.",
                "data": {}
            }, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({
                "status": "error",
                "message": "Clap not found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error removing clap: {str(e)}", exc_info=True)
            return Response({
                "status": "error",
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)