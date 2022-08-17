from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class CarClass(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(primary_key=True, max_length=100, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def save(self, *args, **kwargs):
        self.slug = self.title.lower()
        super(CarClass, self).save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.slug}'
        else:
            return self.slug



class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    car_class = models.ForeignKey(CarClass, on_delete=models.CASCADE, related_name='cars')
    capacity = models.PositiveIntegerField()
    data = models.DateField()

    def __str__(self):
        return self.name


class Travel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    travel_to = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    car_class = models.ForeignKey(CarClass, on_delete=models.CASCADE, related_name='clients')
    number_of_passengers = models.PositiveIntegerField()
    data = models.DateField()
    amount_of_days = models.PositiveIntegerField()

    def __str__(self):
        return self.travel_to


class Image(models.Model):
    image = models.ImageField(upload_to='cars')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name='Владелец рейтинга')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ratings', verbose_name='Машина')
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ], default=1)

    def __str__(self):
        return f'{self.car} - {self.rating}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Владелец лайка')
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='likes', verbose_name='транспорт')
    like = models.BooleanField('лайк', default=False)

    def __str__(self):
        return f'{self.travel} {self.like}'


class Favorite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorits', verbose_name='Владелец избранного')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorits', verbose_name='транспорт')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.car} {self.favorite}'
