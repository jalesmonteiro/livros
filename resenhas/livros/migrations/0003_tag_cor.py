# Generated by Django 5.2.1 on 2025-05-22 00:21

import livros.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("livros", "0002_tag_alter_resenha_livro_livro_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="cor",
            field=models.CharField(
                default=livros.models.gerar_cor_hex, editable=False, max_length=7
            ),
        ),
    ]
