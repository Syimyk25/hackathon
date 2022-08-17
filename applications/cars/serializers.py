from rest_framework import serializers

from applications.cars.models import CarClass, Car, Travel, Image, Comment, Favorite
from applications.cars.tasks import send_new_client


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation['favorite'] == False:
            representation.clear()
        return representation


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class TravelSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Travel
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        travel = Travel.objects.create(**validated_data)
        class_ = travel.car_class.slug

        if str(class_) == 'внедорожники':
            send_new_client.delay()
        return travel

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.filter(like=True).count()

        return representation


class CarClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarClass
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    images = ImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        car = Car.objects.create(**validated_data)

        for image in images.getlist('images'):
            Image.objects.create(car=car, image=image)

        return car

    class Meta:
        model = Car
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_result = 0
        for rating in instance.ratings.all():
            rating_result += int(rating.rating)
        try:
            representation['rating'] = rating_result / instance.ratings.all().count()
        except ZeroDivisionError:
            pass
        return representation


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=10)
