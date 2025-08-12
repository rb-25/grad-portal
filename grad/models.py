from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=255)
    reg_num = models.CharField(max_length=12, unique=True)
    session = models.CharField(max_length=15)
    reg_counter = models.CharField(max_length=15)
    seat = models.CharField(max_length=15)
    gender = models.CharField(max_length=15)
    program_group = models.CharField(max_length=100)
    program_name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=100)
    student_category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
