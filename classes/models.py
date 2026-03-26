# classes/models.py

from django.db import models
from django.conf import settings


class Class(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='classes'
    )
    name = models.CharField(max_length=100)        # e.g. "Mathematics"
    code = models.CharField(max_length=20, unique=True)  # e.g. "MATH101"
    year = models.PositiveIntegerField()            # e.g. 2024
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)  # roll number
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class Enrollment(models.Model):
    """
    Explicit join table between Student and Class.
    A student can be enrolled in many classes.
    A class can have many students.
    """
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='enrollments')
    class_enrolled = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # no duplicate enrollments
        unique_together = ['student', 'class_enrolled']

    def __str__(self):
        return f"{self.student} → {self.class_enrolled}"
