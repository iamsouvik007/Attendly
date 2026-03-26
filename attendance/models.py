# attendance/models.py

from django.db import models
from django.conf import settings
from classes.models import Class, Student


class AttendanceSession(models.Model):
    """
    Represents one attendance-taking event.
    One session per class per date.
    """
    class_ref = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['class_ref', 'date']  # one session per class per day
        ordering = ['-date']

    def __str__(self):
        return f"{self.class_ref} — {self.date}"


class AttendanceRecord(models.Model):
    """
    One row per student per session.
    """
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent',  'Absent'),
        ('late',    'Late'),
    ]

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name='records'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='absent'
    )
    note = models.CharField(max_length=200, blank=True)  # optional teacher note

    class Meta:
        unique_together = ['session', 'student']  # one record per student per session

    def __str__(self):
        return f"{self.student} — {self.status} ({self.session.date})"