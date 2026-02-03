from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth.decorators import login_required




def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
    # Respect the 'next' redirect field if present in GET or POST
        redirect_to = (
            self.request.POST.get(self.redirect_field_name)
            or self.request.GET.get(self.redirect_field_name)
        )
        if redirect_to:
            return redirect_to
        # Fallback to a named URL for the dashboard
        return reverse_lazy("dashboard")


