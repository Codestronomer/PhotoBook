from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, FormView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Category, Photo


class RegistrationView(FormView):
    form_class = UserCreationForm
    template_name = 'auth/registration.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('gallery')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegistrationView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('gallery')
        return super(RegistrationView, self).get(*args, **kwargs)


class GalleryLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    fields = '__all__'
    success_url = reverse_lazy('gallery')

    def get_success_url(self):
        return reverse_lazy('gallery')


def gallery(request):
    categories = Category.objects.all()
    photos = Photo.objects.all()
    return render(request, 'gallery.html', {'categories': categories, 'photos': photos})


def photoDetail(request, pk):
    photos = Photo.objects.all()
    photo = Photo.objects.get(id=pk)
    return render(request, 'photo_detail.html', {'photos': photos, 'photo': photo})


class AddPhotoView(CreateView):
    model = Photo
    template_name = 'add.html'
    fields = ['title', 'description', 'category', 'image']
    success_url = reverse_lazy('gallery')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.method == 'POST':
            data = self.request.POST
            image = self.request.FILES.get('image')

            if data['category'] != 'none':
                category = Category.objects.get(id=data['category'])
            elif data['new_category'] != '':
                category, created = Category.objects.get_or_create(name=data['category_new'])
            else:
                category = None

            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                title=data['title'],
                image=image
            )
        return super(AddPhotoView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

