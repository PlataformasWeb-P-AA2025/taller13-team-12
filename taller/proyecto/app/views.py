from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# ejemplo de uso django-rest_framework
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from app.serializers import UserSerializer, GroupSerializer, \
EdificioSerializer, DepartamentoSerializer

# importar las clases de models.py
from app.models import *

# importar los formularios de forms.py
from app.forms import *

@login_required(login_url='/entrando/login/')
@permission_required('app.view_edificio', login_url="/entrando/login/")
def index(request):

    edificios = Edificio.objects.all()

    informacion_template = {'edificios': edificios, 'numero_edificios': len(edificios)}
    return render(request, 'index.html', informacion_template)

def ingreso(request):

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.data.get("username")
            raw_password = form.data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect(index)
    else:
        form = AuthenticationForm()

    informacion_template = {'form': form}
    return render(request, 'registration/login.html', informacion_template)

def logout_view(request):
    logout(request)
    messages.info(request, "Has salido del sistema")
    return redirect(index)

def obtener_edificio(request, id):

    edificio = Edificio.objects.get(pk=id)

    informacion_template = {'edificio': edificio}
    return render(request, 'obtenerEdificio.html', informacion_template)

@login_required(login_url='/entrando/login/')
@permission_required('app.add_edificio', login_url="/entrando/login/")
def crear_edificio(request):
    
    if request.method=='POST':
        formulario = EdificioForm(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save() 
            return redirect(index)
    else:
        formulario = EdificioForm()
    diccionario = {'formulario': formulario}

    return render(request, 'crearEdificio.html', diccionario)


@login_required(login_url='/entrando/login/')
def editar_edificio(request, id):
    
    edificio = Edificio.objects.get(pk=id)
    if request.method=='POST':
        formulario = EdificioForm(request.POST, instance=edificio)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = EdificioForm(instance=edificio)
    diccionario = {'formulario': formulario}

    return render(request, 'editarEdificio.html', diccionario)

@login_required(login_url='/entrando/login/')
@permission_required('app.delete_edificio', login_url="/entrando/login/")
def eliminar_edificio(request, id):
    
    edificio = Edificio.objects.get(pk=id)
    edificio.delete()
    return redirect(index)


@login_required(login_url='/entrando/login/')
@permission_required('app.add_departamento', login_url="/entrando/login/")
def crear_departamento(request):
    
    if request.method=='POST':
        formulario = DepartamentoForm(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = DepartamentoForm()
    diccionario = {'formulario': formulario}

    return render(request, 'crearDepartamento.html', diccionario)

@login_required(login_url='/entrando/login/')
@permission_required('app.change_edificio', login_url="/entrando/login/")
def editar_departamento(request, id):
    
    departamento = Departamento.objects.get(pk=id)
    if request.method=='POST':
        formulario = DepartamentoForm(request.POST, instance=departamento)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = DepartamentoForm(instance=departamento)
    diccionario = {'formulario': formulario}

    return render(request, 'crearDepartamento.html', diccionario)

@login_required(login_url='/entrando/login/')
@permission_required('app.add_departamento', login_url="/entrando/login/")
def crear_departamento_edificio(request, id):
 
    edificio = Edificio.objects.get(pk=id)
    if request.method=='POST':
        formulario = DepartamentoEdificioForm(edificio, request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = DepartamentoEdificioForm(edificio)
    diccionario = {'formulario': formulario, 'edificio': edificio}

    return render(request, 'crearDepartamentoEdificio.html', diccionario)

# crear vistas a través de viewsets
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class EdificioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartamentoViewSet(viewsets.ModelViewSet):
# class NumeroTelefonicoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    # permission_classes = [permissions.IsAuthenticated]
