from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.utils import timezone

from classes.models import Class
from .models import AttendanceSession, AttendanceRecord


class StartSessionView(LoginRequiredMixin, View):

    def get(self, request, class_pk):
        cls = get_object_or_404(Class, pk=class_pk, teacher=request.user)

        return render(request, 'attendance/start.html', {
            'class': cls,
            'today': timezone.now().date()
        })

    def post(self, request, class_pk):
        cls = get_object_or_404(Class, pk=class_pk, teacher=request.user)
        date = request.POST.get('date')

        session, created = AttendanceSession.objects.get_or_create(
            class_ref=cls,
            date=date,
            defaults={'created_by': request.user}
        )

        # If new session → create records
        if created:
            enrollments = cls.enrollments.select_related('student')

            AttendanceRecord.objects.bulk_create([
                AttendanceRecord(
                    session=session,
                    student=e.student,
                    status='absent'
                )
                for e in enrollments
            ])

            cache.delete(f'dashboard_stats:{request.user.pk}')
            cache.delete(f'class_report:{request.user.pk}:{cls.pk}')

        return redirect('attendance:mark', session_pk=session.pk)


class MarkAttendanceView(LoginRequiredMixin, View):

    def get(self, request, session_pk):
        session = get_object_or_404(
            AttendanceSession,
            pk=session_pk,
            class_ref__teacher=request.user
        )

        records = session.records.select_related('student')

        return render(request, 'attendance/mark.html', {
            'session': session,
            'records': records
        })

    def post(self, request, session_pk):
        session = get_object_or_404(
            AttendanceSession,
            pk=session_pk,
            class_ref__teacher=request.user
        )

        records = session.records.select_related('student')
        allowed_statuses = {'present', 'absent', 'late'}

        for record in records:
            status = request.POST.get(f'status_{record.pk}', 'absent')
            if status not in allowed_statuses:
                status = 'absent'
            note = request.POST.get(f'note_{record.pk}', '')

            record.status = status
            record.note = note
            record.save()

            cache.delete(
                f'student_report:{request.user.pk}:{record.student.pk}')

        cache.delete(f'dashboard_stats:{request.user.pk}')
        cache.delete(f'class_report:{request.user.pk}:{session.class_ref.pk}')

        messages.success(request, 'Attendance saved!')
        return redirect('attendance:mark', session_pk=session.pk)
