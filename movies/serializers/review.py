from rest_framework import serializers
from ..models import Review, Movie


class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('title', 'content',)


class ReviewSerializer(serializers.ModelSerializer):
    class MovieListSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('title',)
    movie = MovieListSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        # read_only_fields = ('movie',)