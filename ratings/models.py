from django.db import models
from shop.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.shortcuts import get_object_or_404

# Create your models here.


class Rating(models.Model):
    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = [
            'user',
            'product']

    title = models.CharField(max_length=200, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product')
    rating = models.IntegerField(default=0,
                                 validators=[
                                     MaxValueValidator(5),
                                     MinValueValidator(0),
                                 ])
    review = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.email}"

    def get_all_ratings(product):
        ratings = Rating.objects.filter(product=product)
        all_ratings = []
        for rating in ratings:
            rating_data = {
                "title": rating.title,
                "user": rating.user.first_name,
                "rating": rating.rating,
                "review": rating.review,
            }
            all_ratings.append(rating_data)
        return all_ratings

    def get_average_rating(product):
        ratings = Rating.objects.filter(product=product)
        if len(ratings) > 0:
            total = 0
            for rating in ratings:
                total += rating.rating
            average_rating = round((total / len(ratings)), 1)
        else:
            average_rating = 0

        return average_rating

    def get_ratings_count(product):
        ratings = Rating.objects.filter(product=product)
        count = len(ratings)
        return count
