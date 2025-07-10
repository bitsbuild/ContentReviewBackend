from rest_framework import viewsets,permissions,filters
from django_filters.rest_framework import DjangoFilterBackend
from app.models import ContentDetails, ContentReviews, Artists, StreamingPlatform
from app.pagination import ContentsCPagination
from app.serializers import ContentSerializer,ContentReviewSerializer,ArtistsSerializer,StreamingPlatformSerializer
from app.permissions import AdminOrReadOnly,ReviewPermissions 
from app.throttling import ContentThrottle,PlatformThrottle,ArtistThrottle,ReviewThrottle
import statistics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
class ContentViewSet(viewsets.ModelViewSet):
    queryset = ContentDetails.objects.all()
    serializer_class = ContentSerializer
    permission_classes=[permissions.IsAuthenticated,AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['artists','content_platform','content_released']
    search_fields = ['artists__artist_name','content_platform__platform_name']
    throttle_classes = [ContentThrottle]
    pagination_class = ContentsCPagination
    # TO HAVE DIFFERENT SEARCH METHODS ADD THE SPECIAL CHARACTER AS PREFIX AS FIRST CHARACTER OF SEARCH FIELD STRING
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artists.objects.all()
    serializer_class = ArtistsSerializer
    permission_classes=[permissions.IsAuthenticated,AdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['artist_name','artist_about']
    throttle_classes = [ArtistThrottle]
class PlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer
    permission_classes=[permissions.IsAuthenticated,AdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['platform_name','platform_about','platform_url']
    throttle_classes = [PlatformThrottle]
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = ContentReviews.objects.all()
    serializer_class = ContentReviewSerializer
    permission_classes = [permissions.IsAuthenticated,ReviewPermissions]
    filter_backends=[DjangoFilterBackend,filters.SearchFilter]
    filterset_fields=['review_movie','review_stars','review_user']
    search_fields = ['review_movie__content_name']
    throttle_classes = [ReviewThrottle]
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            movie = request.data['review_movie']
            ratings = list(ContentReviews.objects.filter(review_movie=movie).values_list('review_stars',flat=True))
            movie_stars = statistics.mean(ratings)
            content = ContentDetails.objects.get(pk=movie)
            content.content_rating = movie_stars
            content.save()
            return Response({"Status":"Success"},status=HTTP_200_OK)
        except Exception as e:
            return Response({"Status":"Failed","Error":str(e)},status=HTTP_400_BAD_REQUEST)
    def perform_create(self, serializer):
        serializer.save(review_user=self.request.user)