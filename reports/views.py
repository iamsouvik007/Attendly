from django.views import View
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

        records = AttendanceRecord.objects.filter(student=student)

        total = records.count()
        present = records.filter(status='present').count()
        absent = records.filter(status='absent').count()
        late = records.filter(status='late').count()

        percentage = (present / total * 100) if total > 0 else 0

        return render(request, 'reports/student.html', {
            'student': student,
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'percentage': round(percentage, 2),
        })


class ClassReportView(LoginRequiredMixin, View):

    def get(self, request, class_pk):
        cls = get_object_or_404(Class, pk=class_pk, teacher=request.user)

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

        return render(request, 'reports/class.html', {
            'class': cls,
            'report_data': report_data
        })
