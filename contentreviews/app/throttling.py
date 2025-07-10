from rest_framework.throttling import UserRateThrottle
class ContentThrottle(UserRateThrottle):
    scope = 'content_throttle'
class PlatformThrottle(UserRateThrottle):
    scope = 'platform_throttle'
class ArtistThrottle(UserRateThrottle):
    scope = 'artist_throttle'
class ReviewThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        action = getattr(view, 'action', None)
        if action == 'list':
            self.scope = 'review_list'
        else:
            self.scope = 'review_other'
        return super().allow_request(request, view)