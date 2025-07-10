from app import models
from app.models import ContentDetails,StreamingPlatform,Artists,ContentReviews
from rest_framework import serializers
class ContentReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    review_movie = serializers.PrimaryKeyRelatedField(queryset=ContentDetails.objects.all())
    review_movie_name = serializers.CharField(source='review_movie.content_name',read_only=True) 
    class Meta:
        model = ContentReviews
        fields = '__all__'
class ContentSerializer(serializers.ModelSerializer):
    reviews = ContentReviewSerializer(many=True,read_only=True)
    content_platform = serializers.CharField(source='content_platform.platform_name',read_only=True)
    artists = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='artist_name'
    )
    class Meta:
        model = ContentDetails
        fields = '__all__'
class StreamingPlatformSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True,read_only=True)
    class Meta:
        model = StreamingPlatform
        fields = '__all__'
class ArtistsSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True,read_only=True)
    class Meta:
        model = Artists
        fields = '__all__'