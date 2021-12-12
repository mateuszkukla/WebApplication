from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#
#
# class Question(models.Model):
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#
# class Choice(models.Model):
#     def __str__(self):
#         return self.choice_text
#
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#
class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_food = models.OneToOneField('Meal', models.DO_NOTHING, db_column='ID_food', primary_key=True)  # Field name made lowercase.
    kcal = models.SmallIntegerField(db_column='Kcal')  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=6, decimal_places=2)  # Field name made lowercase.
    carbohydrates = models.DecimalField(db_column='Carbohydrates', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fats = models.DecimalField(db_column='Fats', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Food'


class Meal(models.Model):
    id_meal = models.OneToOneField(User, models.DO_NOTHING, db_column='ID_meal', primary_key=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Meal'


class user_properties(models.Model):
    id_user = models.AutoField(db_column='ID_user', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age')  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=3, decimal_places=2)  # Field name made lowercase.
    sex = models.BooleanField(db_column='Sex')  # Field name made lowercase. This field type is a guess.
    height = models.DecimalField(db_column='Height', max_digits=3, decimal_places=1)  # Field name made lowercase.
    goal = models.DecimalField(db_column='Goal', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_properties'
