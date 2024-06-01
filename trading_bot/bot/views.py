from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BotConfig, TradeLog, CoinEvaluation
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from .tasks import run_trading_bot  # Import the task

@login_required
def dashboard(request):
    trades = TradeLog.objects.all()
    evaluations = CoinEvaluation.objects.all()
    return render(request, 'bot/dashboard.html', {'trades': trades, 'evaluations': evaluations})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": LoginSerializer().get_token({"username": user.username})
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                run_trading_bot.delay()  # Run the bot after successful login
                return Response({"token": serializer.get_token({"username": username})}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
