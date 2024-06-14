from django.views.generic.base import TemplateView

from .mixins import ReactMixin


class ReactView(ReactMixin, TemplateView):
    template_name = 'py_react_django/react.html'
    app_root = 'py_react_django/components/app.jsx'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_root'] = self.app_root
        return context
