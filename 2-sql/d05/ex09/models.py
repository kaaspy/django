from django.db import models

class Planets(models.Model):
    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
    )
    climate = models.CharField(
        null=True,
        blank=True,
    )
    diameter = models.IntegerField(
        null=True,
        blank=True,
    )
    orbital_period = models.FloatField(
        null=True,
        blank=True,
    )
    population = models.BigIntegerField(
        null=True,
        blank=True,
    )
    rotation_period = models.IntegerField(
        null=True,
        blank=True,
    )
    surface_water = models.FloatField(
        null=True,
        blank=True,
    )
    terrain = models.CharField(
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        null=False,
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        null=False,
        auto_now=True,
    )

    class Meta:
        db_table = "ex09_planets"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

class People(models.Model):
    name = models.CharField(
        max_length=64,
        null=False,
        unique=True,
    )
    birth_year = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    eye_color = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    hair_color = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    height = models.IntegerField(
        null=True,
        blank=True,
    )
    mass = models.FloatField(
        null=True,
        blank=True,
    )
    homeworld = models.ForeignKey(
        Planets,
        null=True,
        blank=True,
        db_column="homeworld",
        on_delete=models.SET_NULL,
    )
    created = models.DateTimeField(
        null=False,
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        null=False,
        auto_now=True,
    )

    class Meta:
        db_table = "ex09_people"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"