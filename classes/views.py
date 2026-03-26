from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
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

    def post(self, request, pk):
        cls = get_object_or_404(Class, pk=pk, teacher=request.user)

        form = StudentForm(request.POST)
        if form.is_valid():
            student, created = Student.objects.get_or_create(
                student_id=form.cleaned_data['student_id'],
                defaults={
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'email': form.cleaned_data['email'],
                }
            )

            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                class_enrolled=cls
            )

            if created:
                messages.success(request, f'{student} added.')
            else:
                messages.warning(request, 'Already enrolled.')

        return redirect('classes:detail', pk=pk)