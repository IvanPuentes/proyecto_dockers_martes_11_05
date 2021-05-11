from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Post,DescripLib,Manga,Autores,Comentario
from .forms import UsuarioPersCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied




#vista de la pagina principal 
class HomePageView(ListView):
    template_name = 'home.html'
    model = Post
    context_object_name='Listado'
#vista de la pagina para registar nuevos usarios
class RegistrarView(CreateView):
   form_class = UsuarioPersCreationForm
   success_url = reverse_lazy('login')
   template_name = 'registrar.html'  

#vista de la pagina principal de mangas
class MangaPageView(ListView):
    template_name = 'mangas.html'
    model = Manga
    context_object_name='Listado1'

#vista de la pagina principal de revistas 
class RevistaPageView(ListView):
    template_name = 'revistas.html'
    model = Post
    context_object_name='Listado'
#vista de la pagina principal de los autores
class AutoresPageView(ListView):
    template_name = 'Autores.html'
    model = Autores
    context_object_name='Listado1'

#vista de la pagina de descripciones de los libros
class Descrip_libPageView(ListView):
    template_name = 'descrip_lib.html'
    model = Post
    context_object_name='Listado1'
#vista de la pagina de descripcion de los libros 
class DetallePageView(DetailView):
    template_name = 'descAutores.html'
    model = Autores
    context_object_name='Blogs'
#vista de la pagina para la creacion de autroes
class CrearPageView(LoginRequiredMixin,CreateView):
    template_name = 'CrearAutores.html'
    model = Autores
    success_url = reverse_lazy('home')
    fields = 'Nombre','Descripcion','img','Nacionalidad','F_Muerte',
    login_url = 'login'
#validacion para restringir la vista si no eres un usario registrado
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    
#vista de la pagina de editar autores 
class UpdatePageView(LoginRequiredMixin,UpdateView):
    template_name = 'editarAutores.html'
    model = Autores
    success_url = reverse_lazy('home')
    fields = 'Nombre','Descripcion','img','Nacionalidad','F_Muerte',
    login_url = 'login'
#vista para restringir la vista si no eres un usuario restringido
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
#validacion para restringir la accion si no eres el usario que registro la creacion 
    def dispatch(self, request, *args,**kwargs):
        obj = self.get_object()
        if obj.autor != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

#vista de la pagina de la eliminacion de los autores 
class DeletePageView(LoginRequiredMixin,DeleteView):
    template_name = 'eliminarAutores.html'
    model = Autores
    success_url = reverse_lazy('home')
    context_object_name='Autores'
    login_url = 'login'
#validacion para restringir la accion si no eres el usario que registro la creacion 
    def dispatch(self, request, *args,**kwargs):
        obj = self.get_object()
        if obj.autor != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


#vista de la pagina de la creacion de comentarios
class ComentarioCreateView(LoginRequiredMixin,CreateView):
    model = Comentario
    template_name = "comentarioNuevo.html"
    fields = ('comentario',)
    login_url='login'
    success_url = reverse_lazy('home')
    context_object_name='Listado1'
#validacion para restringir la accion si no eres el usario que registro la creacion 
    def form_valid(self,form):
        form.instance.autor = self.request.user
        form.instance.autores = Autores.objects.get(pk=self.kwargs.get('libroComent'))
        return super().form_valid(form)