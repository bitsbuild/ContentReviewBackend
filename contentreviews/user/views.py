from user.serializers import UserSerializer
from rest_framework.decorators import api_view,throttle_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import AllowAny,IsAuthenticated
@api_view(['POST'])
@throttle_classes([UserRateThrottle])
@permission_classes([AllowAny])
def create_account(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_token_search = serializer.instance
            token,collect = Token.objects.get_or_create(user=user_token_search)
            return Response({
                "status":"Account Created Successfully",
                "token":str(token.key)
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "status":"Account Creation Failed",
                "error":str(serializer.errors)
            },status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@throttle_classes([UserRateThrottle])
@permission_classes([IsAuthenticated])
def delete_account(request):
    try:    
        request.user.delete()
        return Response({
            "status":"Account Deletion Successful"
        },status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "status":"Account Deletion Failed",
            "error":str(e)
        },status=status.HTTP_400_BAD_REQUEST)