# Generated by Django 4.2.3 on 2023-08-11 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pd_id', models.AutoField(primary_key=True, serialize=False)),
                ('pd_name', models.TextField(verbose_name='상품 이름')),
                ('pd_price', models.IntegerField(verbose_name='상품 가격')),
                ('pd_brand', models.CharField(max_length=20, verbose_name='상품 브랜드명')),
                ('pd_purpose', models.CharField(max_length=500, verbose_name='상품 사용 목적')),
                ('pd_usage', models.CharField(max_length=500, verbose_name='상품 사용법')),
                ('pd_like_cnt', models.IntegerField(verbose_name='찜 개수')),
                ('pd_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='상품 대표 사진')),
                ('cg_id', models.IntegerField(choices=[('1', 'makeup'), ('2', 'skincare'), ('3', 'mask'), ('4', 'suncare')])),
                ('ingredients', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_ingredients', to='ingredients.ingredient', verbose_name='상품이 포함하는 성분들')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('wish_id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_product_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vegan',
            fields=[
                ('vg_id', models.AutoField(primary_key=True, serialize=False)),
                ('vg_company', models.CharField(choices=[('Korea agency of Vegan Certification and Services', '한국비건인증원'), ('Expertise Vegan Europe', '프랑스이브비건'), ('V Label Italia srl', '이탈리아브이라벨'), ('The Vegan Society', '영국비건소사이어티'), ('PETA Beauty without bunny - global animal test-free', 'PETA1'), ('PETA Beauty without bunny - global animal test-free and vegan', 'PETA2'), ('Biorius', '벨기에 바이오리우스')], max_length=70, verbose_name='비건 인증처명')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_products', to='ingredients.ingredient')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_ingredients', to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('mk_id', models.AutoField(primary_key=True, serialize=False)),
                ('mk_name', models.CharField(max_length=20, verbose_name='구매처 이름')),
                ('mk_link', models.URLField(max_length=500)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
