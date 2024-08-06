import json

from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import MyTokenObtainPairSerializer,Registerserializer,Userserializer,MoviedetailSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import generics,status,viewsets
from Movieapp.models import Movies,Genre,Reviews
from .serializers import Genreserializer,MovieReadSerializer,MovieWriteSerializer,MoviedetailSerializer,ReviewsWriteSerializer,ReviewReadserializer,ProfileSerializer
from .pagination import StandardResultsSetPagination

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class Registeruser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = Registerserializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_data = {
            'message':'User Registered successfully',
            'user':{
                'id':user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
            }
        }

        return Response(response_data,status=status.HTTP_201_CREATED)


class Usersupdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def update(self,request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data,partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()

        response_data = {
            'message': 'User Updated successfully',
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
            }
        }

        return Response(response_data,status=status.HTTP_200_OK)

class Userdetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializer
    permission_classes = [IsAuthenticated]


class Userlogout(APIView):
    permission_classes = (IsAuthenticated,)


    def post(self,request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class Genrelist(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = Genreserializer
    permission_classes = [AllowAny]

class Genredetails(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = Genreserializer


class MoviesCreate(generics.ListCreateAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieWriteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields =['title']
    permission_classes = [IsAuthenticated]

class Movieslistuserwise(generics.ListAPIView):
    serializer_class = MovieReadSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Movies.objects.all()
        user_id = self.request.query_params.get('users', None)
        if user_id:
            queryset = queryset.filter(users_id=user_id)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class MovieDetails(generics.RetrieveAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviedetailSerializer

class Moviedetailslist(generics.RetrieveAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviedetailSerializer

class ApprovedMovielist(generics.ListAPIView):
    serializer_class = MovieReadSerializer

    def get_queryset(self):
        return Movies.objects.filter(approval_status=1)


class MoviesUpdate(generics.RetrieveUpdateAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieWriteSerializer

class MoviesDelete(generics.DestroyAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviedetailSerializer


class ReviewsListCreate(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsWriteSerializer


    def perform_create(self,serializer):
        movie_id = self.kwargs.get('movie_id')
        user_id = self.kwargs.get('user_id')


        try:
            movie = Movies.objects.get(id=movie_id)
        except Movies.DoesNotExist:
            raise NotFound(detail="Movie not found.")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound(detail=user_id)

        serializer.save(MovieId=movie,UserId=user)
class ReviewsList(generics.ListAPIView):
    serializer_class = ReviewReadserializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        queryset = Reviews.objects.all()
        movie_id = self.request.query_params.get('movie', None)
        if movie_id:
            queryset = queryset.filter(MovieId=movie_id)
        queryset = queryset.filter(active=1)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)














