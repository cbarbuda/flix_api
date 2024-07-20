from django.db.models import Avg
from rest_framework import serializers
from actors.serializers import ActorSerializer
from genres.serializers import GenreSerializer
from movies.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'

     #   reviews = obj.reviews.all()

      #  if reviews:
      #      sum_reviews = 0

      #      for review in reviews:
      #          sum_reviews += review.stars
      #      reviews_count = reviews.count()
      #      return round(sum_reviews / reviews_count,2)
      #  return 
    
    def validate_release_data(self,value):
        if value.year < 2000:
            raise serializers.ValidationError('A data não pode ser menor que 1900')
        return value 
    def validate_resume(self,value):
       if len(value) > 20:
            raise serializers.ValidationError('numero de caracteres maior que o permitido')
       return value       

class MovieListDetailSerializer(serializers.ModelSerializer):
       genre = GenreSerializer()
       actors =ActorSerializer(many = True) 
      
       rate = serializers.SerializerMethodField(read_only=True)
   
       class Meta:
          model = Movie
         # fields = '__all__'
          fields = ['id', 'title', 'genre', 'actors', 'release_data', 'rate', 'resume']

       def get_rate(self,obj):
           rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']
           if rate:
              return round(rate,2)
           return None



class MovieStatsSerializer(serializers.Serializer):
        total_movies = serializers.IntegerField()
        movies_by_genre= serializers.ListField()
        total_reviews = serializers.IntegerField()
        average_stars = serializers.FloatField()      


        