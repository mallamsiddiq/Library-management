# Generated by Django 3.0.5 on 2023-10-30 23:51

from django.db import migrations, models
import django.db.models.deletion
import library.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('isbn', models.PositiveIntegerField()),
                ('author', models.CharField(max_length=40)),
                ('category', models.CharField(choices=[('education', 'Education'), ('entertainment', 'Entertainment'), ('comics', 'Comics'), ('biography', 'Biography'), ('history', 'History'), ('novel', 'Novel'), ('fantasy', 'Fantasy'), ('thriller', 'Thriller'), ('romance', 'Romance'), ('scifi', 'Sci-Fi')], default='education', max_length=30)),
                ('total_stock', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BookIssuance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuedate', models.DateField(auto_now=True)),
                ('expirydate', models.DateField(default=library.models.get_expiry)),
                ('active', models.BooleanField(default=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issuance', to='library.Book')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_issuance', to='student.StudentExtra')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='readers',
            field=models.ManyToManyField(related_name='books', through='library.BookIssuance', to='student.StudentExtra'),
        ),
    ]
