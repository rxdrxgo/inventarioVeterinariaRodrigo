from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserProfileForm
from django.contrib import messages


# Create your views here.
@login_required()
def verProfile(request):
    return render(request, 'profile.html')

@login_required()
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito')
            return redirect('profile')
        else:
            messages.error(request, 'Hubo un error al actualizar tu perfil. Intenta nuevamente.')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    success_message = "¡Usuario creado exitosamente!"

