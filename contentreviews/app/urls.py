from django.urls import path,include
from rest_framework.routers import DefaultRouter
from app.views import ContentViewSet,PlatformViewSet,ArtistViewSet,ReviewViewSet
router = DefaultRouter()
router.register(r'contents',ContentViewSet,basename='contents')
router.register(r'platforms',PlatformViewSet,basename='platforms')
router.register(r'artists',ArtistViewSet,basename='artists')
router.register(r'reviews',ReviewViewSet,basename='reviews')
urlpatterns = router.urls