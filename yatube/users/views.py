from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm

class SignUp(CreateView):  # TODO: Сделать странички по этой задачке - https://practicum.yandex.ru/learn/python-developer-plus/courses/88539ae3-edac-4f22-b93b-c1646ce4cd3c/sprints/88777/topics/546bbd95-67d8-4e2d-9d3d-8a9623844250/lessons/5d9696be-88ed-496e-9f86-9c6876ab8b3b/
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'