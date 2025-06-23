from rest_framework.throttling import UserRateThrottle
class ContentThrottle(UserRateThrottle):
    scope = 'content_throttle'
class PlatformThrottle(UserRateThrottle):
    scope = 'platform_throttle'
class ArtistThrottle(UserRateThrottle):
    scope = 'artist_throttle'
class ReviewThrottle(UserRateThrottle):
    def get_rate(self):
        action = getattr(self.view,'action',None)
        if action == 'list':
            return '60/min'
        else:
            return '10/hour'