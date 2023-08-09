from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='작성일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일시')),
                ('pd_id', models.AutoField(primary_key=True, serialize=False)),
                ('pd_name', models.TextField(verbose_name='제품 이름')),
                ('pd_price', models.IntegerField(verbose_name='제품 가격')),
                ('pd_brand', models.CharField(max_length=20, verbose_name='제품 브랜드명')),
                ('pd_purpose', models.CharField(max_length=500, verbose_name='제품 사용 목적')),
                ('pd_usage', models.CharField(max_length=500, verbose_name='제품 사용법')),
                ('pd_like_cnt', models.IntegerField(verbose_name='찜 개수')),
                ('pd_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='제품 대표 사진')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
