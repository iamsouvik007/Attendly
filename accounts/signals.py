from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Teacher, TeacherProfile


@receiver(post_save, sender=Teacher)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        full_name = f"{instance.first_name} {instance.last_name}".strip()
        TeacherProfile.objects.create(
            teacher=instance,
            full_name=full_name,
            mobile_no=(instance.phone or '').strip(),
        )
