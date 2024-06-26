# Generated by Django 4.2.11 on 2024-04-09 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Curso",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="poapasistencia",
            name="tabla_asistencia",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lista_alumnos",
                to="core.tablaasistencia",
            ),
        ),
        migrations.AddField(
            model_name="alumno",
            name="curso",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="core.curso"
            ),
        ),
    ]
