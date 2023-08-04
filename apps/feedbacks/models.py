from django.db import models
from ..products.models import Product
from ..accounts.models import UserModel
from ..utils import choicess

nb = dict(null=True, blank=True)


class Rating(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='rating')
    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE)
    content = models.TextField(**nb)
    rating = models.PositiveIntegerField(choices=choicess.STARS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user}\'s {self.rating}-star rating for {self.product}'


