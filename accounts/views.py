from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    # Adding picture file to user
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            if "picture" in request.FILES:
                user.picture = request.FILES["picture"]
            user.save()
            return self.form_valid(form)
        return self.form_invalid(form)
