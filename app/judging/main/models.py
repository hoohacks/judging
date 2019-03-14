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


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    organizers = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    table = models.CharField(max_length=15, blank=True)
    members = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    is_anchor = models.BooleanField(default=False)

    def __str__(self):
        return 'Table {} - {}'.format(self.table, self.name)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    number_winners = models.IntegerField(default=1)
    min_judges = models.IntegerField(
        default=1, help_text="The minimum number of judges a team should be seen by for this category")
    is_opt_in = models.BooleanField(default=False)
    can_anyone_judge = models.BooleanField(default=False)
    submissions = models.ManyToManyField(
        Team, related_name='categories', blank=True)

    def __str__(self):
        return '[{}] {}'.format(self.organization.name, self.name)

    class Meta:
        verbose_name_plural = "categories"


class User(AbstractUser):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True)

    def is_profile_complete(self):
        if self.is_staff or self.is_superuser:
            return True
        return all([bool(self.organization),
                    bool(self.username),
                    bool(self.first_name),
                    bool(self.last_name)])

    def __str__(self):
        org_name = 'None'
        if self.organization:
            org_name = self.organization.name
        return '{} {} <{}>'.format(self.first_name, self.last_name, org_name)


class Criteria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    min_score = models.IntegerField(default=1)
    max_score = models.IntegerField(default=5)
    weight = models.DecimalField(default=1, decimal_places=2, max_digits=4)

    def __str__(self):
        return self.name


class CriteriaLabel(models.Model):
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    score = models.IntegerField()
    label = models.CharField(max_length=255)

    def __str__(self):
        return '[{} - {}] {}'.format(self.criteria.name, self.score, self.label)


class Demo(models.Model):
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    @property
    def is_for_judge_category(self):
        for category in self.team.categories.all():
            if category.organization.id == self.judge.organization.id:
                return True
        return False

    def __str__(self):
        return '{} - {}'.format(self.judge, self.team.name)


class DemoScore(models.Model):
    demo = models.ForeignKey(Demo, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return '{} = {} - {}'.format(self.demo, self.criteria.name, self.value)
