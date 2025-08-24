from rest_framework import generics, permissions
from rest_framework.response import Response, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, LightweightUserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)  # token already created in serializer
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.following.filter(id=target.id).exists():
            return Response({"detail": "Already following."}, status=status.HTTP_200_OK)

        # Either of these is fine; they’re equivalent because of related_name
        # request.user.following.add(target)
        target.followers.add(request.user)

        return Response(
            {
                "detail": f"Now following {target.username}.",
                "following_count": request.user.following.count(),
                "followers_count_of_target": target.followers.count(),
            },
            status=status.HTTP_201_CREATED,
        )


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        if not request.user.following.filter(id=target.id).exists():
            return Response({"detail": "You are not following this user."}, status=status.HTTP_200_OK)

        # request.user.following.remove(target)
        target.followers.remove(request.user)

        return Response(
            {
                "detail": f"Unfollowed {target.username}.",
                "following_count": request.user.following.count(),
                "followers_count_of_target": target.followers.count(),
            },
            status=status.HTTP_200_OK,
        )


class FollowersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LightweightUserSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        return user.followers.all().order_by("username")


class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LightweightUserSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        return user.following.all().order_by("username")
