from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.cache import cache
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from .models import Class, Student, Enrollment
from .forms import ClassForm, StudentForm


class ClassListView(LoginRequiredMixin, ListView):
    template_name = 'classes/list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.filter(teacher=self.request.user)


class ClassCreateView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'classes/form.html', {'form': ClassForm()})

    def post(self, request):
        form = ClassForm(request.POST)
        if form.is_valid():
            cls = form.save(commit=False)
            cls.teacher = request.user
            cls.save()
            cache.delete(f'dashboard_stats:{request.user.pk}')
            messages.success(request, 'Class created!')
            return redirect('classes:detail', pk=cls.pk)
        return render(request, 'classes/form.html', {'form': form})


class ClassDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        cls = get_object_or_404(Class, pk=pk, teacher=request.user)
        enrollments = cls.enrollments.select_related('student')
        return render(request, 'classes/detail.html', {
            'class': cls,
            'enrollments': enrollments,
            'student_form': StudentForm(),
        })


class AddStudentView(LoginRequiredMixin, View):

    def _invalidate_related_cache(self, teacher_pk, class_pk, student_pk):
        cache.delete(f'dashboard_stats:{teacher_pk}')
        cache.delete(f'class_report:{teacher_pk}:{class_pk}')
        cache.delete(f'student_report:{teacher_pk}:{student_pk}')

    def _render_class_detail(self, request, cls, student_form):
        enrollments = cls.enrollments.select_related('student')
        return render(request, 'classes/detail.html', {
            'class': cls,
            'enrollments': enrollments,
            'student_form': student_form,
        })

    def post(self, request, pk):
        cls = get_object_or_404(Class, pk=pk, teacher=request.user)

        form = StudentForm(request.POST)
        if not form.is_valid():
            messages.error(
                request, 'Please fill all fields correctly. Mobile No must be at least 10 digits.')
            return self._render_class_detail(request, cls, form)

        roll_no = form.cleaned_data['student_id']
        duplicate_in_class = Enrollment.objects.filter(
            class_enrolled=cls,
            student__student_id=roll_no,
        ).exists()

        if duplicate_in_class:
            form.add_error(
                'student_id', 'This Roll No is already added in this class.')
            messages.warning(
                request, 'This Roll No is already added in this class.')
            return self._render_class_detail(request, cls, form)

        student = form.save()
        Enrollment.objects.create(student=student, class_enrolled=cls)
        self._invalidate_related_cache(request.user.pk, cls.pk, student.pk)
        messages.success(request, f'{student} added.')
        return redirect('classes:detail', pk=pk)


class DeleteClassView(LoginRequiredMixin, View):

    def post(self, request, pk):
        cls = get_object_or_404(Class, pk=pk, teacher=request.user)

        student_ids = list(
            cls.enrollments.values_list('student_id', flat=True)
        )

        with transaction.atomic():
            cls.delete()

            # Remove orphan students not enrolled in any class.
            if student_ids:
                Student.objects.filter(
                    pk__in=student_ids,
                    enrollments__isnull=True,
                ).delete()

        cache.delete(f'dashboard_stats:{request.user.pk}')
        cache.delete(f'class_report:{request.user.pk}:{pk}')

        messages.success(request, 'Class deleted successfully.')
        return redirect('classes:list')


class DeleteStudentView(LoginRequiredMixin, View):

    def post(self, request, pk, student_pk):
        cls = get_object_or_404(Class, pk=pk, teacher=request.user)
        enrollment = get_object_or_404(
            Enrollment,
            class_enrolled=cls,
            student_id=student_pk,
        )

        student = enrollment.student
        enrollment.delete()

        # If this student is not linked to any class, delete full student record.
        if not Enrollment.objects.filter(student=student).exists():
            student.delete()

        cache.delete(f'dashboard_stats:{request.user.pk}')
        cache.delete(f'class_report:{request.user.pk}:{cls.pk}')
        cache.delete(f'student_report:{request.user.pk}:{student_pk}')

        messages.success(request, 'Student deleted successfully.')
        return redirect('classes:detail', pk=pk)
