from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView
from classes.models import Class, Enrollment
from attendance.models import AttendanceSession
from accounts.models import TeacherProfile


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def dispatch(self, request, *args, **kwargs):
        profile, _ = TeacherProfile.objects.get_or_create(
            teacher=request.user,
            defaults={
                'full_name': f'{request.user.first_name} {request.user.last_name}'.strip(),
                'mobile_no': (request.user.phone or '').strip(),
            },
        )
        if not profile.is_complete:
            return redirect('accounts:profile')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = self.request.user
        cache_key = f'dashboard_stats:{teacher.pk}'
        cached_context = cache.get(cache_key)
        selected_date = self.request.GET.get(
            'date') or timezone.now().date().isoformat()

        if cached_context is None:
            my_classes = Class.objects.filter(teacher=teacher)
            cached_context = {
                'total_classes': my_classes.count(),
                'total_students': Enrollment.objects.filter(
                    class_enrolled__teacher=teacher
                ).values('student_id').distinct().count(),
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

        classes_for_chart = (
            Class.objects.filter(teacher=teacher)
            .annotate(
                total_students=Count('enrollments__student', distinct=True),
                present_students=Count(
                    'sessions__records__student',
                    filter=Q(
                        sessions__date=selected_date,
                        sessions__records__status='present',
                    ),
                    distinct=True,
                ),
            )
            .values('pk', 'name', 'code', 'total_students', 'present_students')
            .order_by('name')
        )

        chart_rows = []
        for row in classes_for_chart:
            total = row['total_students'] or 0
            present = row['present_students'] or 0
            percent = int((present / total) * 100) if total else 0
            chart_rows.append({
                'name': row['name'],
                'code': row['code'],
                'total': total,
                'present': present,
                'percent': percent,
            })

        context.update(cached_context)
        context['selected_date'] = selected_date
        context['chart_rows'] = chart_rows
        profile = getattr(teacher, 'profile', None)
        if profile and profile.full_name.strip():
            context['welcome_name'] = profile.full_name.strip().split()[0]
        elif teacher.first_name.strip():
            context['welcome_name'] = teacher.first_name.strip().split()[0]
        else:
            context['welcome_name'] = teacher.email

        return context
