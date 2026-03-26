from django.views import View
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from classes.models import Class, Student
from attendance.models import AttendanceRecord


class StudentReportView(LoginRequiredMixin, View):

    def get(self, request, student_pk):
        student = get_object_or_404(
            Student.objects.filter(
                enrollments__class_enrolled__teacher=request.user).distinct(),
            pk=student_pk
        )

        cache_key = f'student_report:{request.user.pk}:{student_pk}'
        cached_data = cache.get(cache_key)

        if cached_data is None:
            records = AttendanceRecord.objects.filter(student=student)
            total = records.count()
            present = records.filter(status='present').count()
            absent = records.filter(status='absent').count()
            late = records.filter(status='late').count()
            percentage = (present / total * 100) if total > 0 else 0

            cached_data = {
                'total': total,
                'present': present,
                'absent': absent,
                'late': late,
                'percentage': round(percentage, 2),
            }
            cache.set(cache_key, cached_data, 300)

        return render(request, 'reports/student.html', {
            'student': student,
            **cached_data,
        })


class ClassReportView(LoginRequiredMixin, View):

    def get(self, request, class_pk):
        cls = get_object_or_404(Class, pk=class_pk, teacher=request.user)
        sessions = cls.sessions.order_by('-date')
        cache_key = f'class_report:{request.user.pk}:{class_pk}'
        report_data = cache.get(cache_key)

        if report_data is None:
            enrollments = cls.enrollments.select_related('student')
            report_data = []

            for enrollment in enrollments:
                student = enrollment.student

                records = AttendanceRecord.objects.filter(
                    student=student,
                    session__class_ref=cls
                )

                total = records.count()
                present = records.filter(status='present').count()
                percentage = (present / total * 100) if total > 0 else 0

                report_data.append({
                    'student': student,
                    'total': total,
                    'present': present,
                    'percentage': round(percentage, 2)
                })

            cache.set(cache_key, report_data, 300)

        return render(request, 'reports/class.html', {
            'class': cls,
            'report_data': report_data,
            'sessions': sessions,
        })
