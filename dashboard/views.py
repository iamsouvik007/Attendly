from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from classes.models import Class
from attendance.models import AttendanceSession


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = self.request.user
        my_classes = Class.objects.filter(teacher=teacher)

        context['total_classes'] = my_classes.count()
        context['recent_sessions'] = AttendanceSession.objects.filter(
            class_ref__teacher=teacher
        )[:5]
        context['my_classes'] = my_classes

        return context