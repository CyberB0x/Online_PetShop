from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, logout, login
from rest_framework.response import Response

@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "User registered successfully"})


@api_view(["POST"])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"})
    return Response({"error": "Invalid credentials"}, status=400)


@api_view(["POST"])
def user_logout(request):
    logout(request)
    return Response({"message": "Logged out"})
