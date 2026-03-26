from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.views.generic import TemplateView
from classes.models import Class
from attendance.models import AttendanceSession


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = self.request.user
        cache_key = f'dashboard_stats:{teacher.pk}'
        cached_context = cache.get(cache_key)

        if cached_context is None:
            my_classes = Class.objects.filter(teacher=teacher)
            cached_context = {
                'total_classes': my_classes.count(),
                'recent_sessions': list(
                    AttendanceSession.objects.filter(
                        class_ref__teacher=teacher)
                    .values('id', 'class_ref_id', 'date')[:5]
                ),
                'my_classes': list(
                    my_classes.values('pk', 'name', 'code', 'year')
                ),
            }
            cache.set(cache_key, cached_context, 180)

        context.update(cached_context)

        return context
