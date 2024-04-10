# Generated by Django 4.2.11 on 2024-04-09 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_curso_alter_poapasistencia_tabla_asistencia_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Asistencia",
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
                ("fecha", models.DateField(null=True)),
                (
                    "curso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.curso"
                    ),
                ),
            ],
            options={
                "permissions": [("tomar_asistencia", "Puede tomar asistencia")],
                "unique_together": {("fecha", "curso")},
            },
        ),
        migrations.AlterField(
            model_name="poapasistencia",
            name="tabla_asistencia",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lista_alumnos",
                to="core.asistencia",
            ),
        ),
        migrations.DeleteModel(
            name="TablaAsistencia",
        ),
    ]
