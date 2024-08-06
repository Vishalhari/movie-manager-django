from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from Movieapp.models import Movies,Genre,Reviews


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super(MyTokenObtainPairSerializer,cls).get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add additional information to the response data
        data.update({'name': self.user.get_full_name(), 'id': self.user.id})
        return data

class Registerserializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']




class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

        def to_representation(self,instance):
            representation = super().to_representation(instance)
            return representation


class Genreserializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieWriteSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(required=False)
    class Meta:
        model = Movies
        fields = ['id', 'title', 'genre', 'users', 'description', 'releaseDate', 'actors', 'banner', 'imdbrating',
                  'trailerLink', 'approval_status']

        def update(self,instance, validated_data):
            file = validated_data.post('banner', None)

            if file is not None:
                instance.banner = file
            instance.title = validated_data.get("title", instance.title)
            instance.genre = validated_data.get("genre", instance.genre)
            instance.description = validated_data.get("description", instance.description)
            instance.releaseDate = validated_data.get("releaseDate", instance.releaseDate)
            instance.actors = validated_data.get("actors", instance.actors)
            instance.imdbrating = validated_data.get("imdbrating", instance.imdbrating)
            instance.trailerLink = validated_data.get("trailerLink", instance.trailerLink)
            instance.save()
            return instance


class MoviedetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'title', 'genre', 'users', 'description', 'releaseDate', 'actors', 'banner', 'imdbrating',
                  'trailerLink', 'approval_status']


class MovieReadSerializer(serializers.ModelSerializer):
    genre = Genreserializer()
    banner = serializers.SerializerMethodField()
    class Meta:
        model = Movies
        fields = ['id', 'title', 'genre', 'users', 'description', 'releaseDate', 'actors', 'banner', 'imdbrating', 'trailerLink', 'approval_status']


    def get_banner(self,obj):
        request = self.context.get('request')
        if obj.banner:
            return request.build_absolute_uri(obj.banner.url)
        return None

class MoviedetailSerializer(serializers.ModelSerializer):
    genre = Genreserializer()

    class Meta:
        model = Movies
        fields = ['id', 'title', 'genre', 'users', 'description', 'releaseDate', 'actors', 'banner', 'imdbrating', 'trailerLink', 'approval_status']


class ReviewsWriteSerializer(serializers.ModelSerializer):
    class Meta:
            model = Reviews
            fields = ['id', 'rating', 'review', 'MovieId', 'UserId', 'created']
            read_only_fields = ['MovieId', 'UserId', 'created']

class ReviewReadserializer(serializers.ModelSerializer):
    MovieId = MovieReadSerializer()
    UserId = Userserializer()

    class Meta:

        model = Reviews
        fields = ['id', 'rating', 'review', 'MovieId', 'UserId', 'created']








