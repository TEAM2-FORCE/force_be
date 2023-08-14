# Generated by Django 4.2.3 on 2023-08-14 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('ingredients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='ingredient_products', through='ingredients.IngredientProduct', to='products.product', verbose_name='성분을 포함하는 상품들'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='igd',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ingredients.ingredient'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bm_igd_id', to=settings.AUTH_USER_MODEL),
        ),
    ]