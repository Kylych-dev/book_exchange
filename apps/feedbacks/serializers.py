
from rest_framework import serializers
from . import models




class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ['id', 'rating', 'content']

    def create(self, validated_data):
        product_id = self.context['product_id']
        user_id = self.context['user_id']
        rating = models.Rating.objects.create(product_id=product_id,
                                              user_id=user_id,
                                              **self.validated_data)
        return rating