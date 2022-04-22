from rest_framework import serializers
from .review import ReviewListSerializer
from ..models import Movie, Actor


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'overview',)


class MovieSerializer(serializers.ModelSerializer):
    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name',)

    actors = ActorSerializer(many=True, read_only=True)
    review_set = ReviewListSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'