# cgpa_app/models.py
from django.db import models
from users.models import User

class Semester(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Fall 2024"
    year = models.IntegerField()
    def __str__(self):
        return f"{self.name} ({self.year})"

class Grade(models.Model):
    letter = models.CharField(max_length=2)  # e.g., "A", "B+"
    points = models.DecimalField(max_digits=4, decimal_places=2)  # e.g., 5.00 for A
    def __str__(self):
        return self.letter

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this line
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    credits = models.PositiveIntegerField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    def __str__(self):
        return self.name