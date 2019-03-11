"""All models for judging project.

There is only one Event i.e. hackathon for each instance of this project.
There might be many Organizations (e.g. sponsors, partners) that will be
judging. Every User (e.g. judge, admin) must belong to an Organization,
and every Prize must belong to an Organization. Many Teams will submit a
project to be judged. A Demo is an instance where a Judge evaluates a Team.
For each Demo, the Judge will give DemoScores based on Criteria that you,
as the organizer, defines. The Criteria are restricted to integer ranges, so
you have the option to define CriteriaLabels for each value in the range.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class Event(models.Model):
    name = models.CharField(max_length=100)


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Team(models.Model):
    name = models.CharField(max_length=255)
    table = models.CharField(max_length=15)
    members = models.CharField(max_length=255)
    link = models.URLField()
    is_anchor = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    number_winners = models.IntegerField(default=1)
    submissions = models.ManyToManyField(Team, related_name='categories')


class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        org_name = 'None'
        if self.organization:
            org_name = self.organization.name
        return '{} {} <{}>'.format(self.first_name, self.last_name, org_name)


class Criteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    min_score = models.IntegerField(default=1)
    max_score = models.IntegerField(default=5)
    weight = models.DecimalField(default=1, decimal_places=2, max_digits=4)


class CriteriaLabel(models.Model):
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    score = models.IntegerField()
    label = models.CharField(max_length=255)


class Demo(models.Model):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class DemoScore(models.Model):
    demo = models.ForeignKey(Demo, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    value = models.IntegerField()
