from django.shortcuts import render,redirect
from .models import Tasks
from .forms import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from django.urls import reverse_lazy
# Create your views here.

class TaskListView(ListView):
    model = Tasks
    template_name = 'todo_app/index.html'
    context_object_name = 'task_list'

class TaskDetailView(DetailView):
    model = Tasks
    template_name = 'todo_app/detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Tasks
    template_name = 'todo_app/update.html'
    context_object_name = 'task'
    fields = {'name','priority','date'}

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})


class TaskDeleteView(DeleteView):
    model = Tasks
    template_name = 'todo_app/delete.html'
    success_url = reverse_lazy('cbv')

    
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        priority = request.POST.get('priority','')
        tasks = Tasks(name=name,priority=priority)
        tasks.save()
        return redirect('/')

    return render(request,'todo_app/add.html')

def index(request):
    task_list = Tasks.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name','')
        priority = request.POST.get('priority','')
        date = request.POST.get('date','')
        tasks = Tasks(name=name,priority=priority,date=date)
        tasks.save()
        return redirect('/')
    return render(request,'todo_app/index.html',{'task_list':task_list})

def delete(request,taskid):
    task = Tasks.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'todo_app/delete.html',{'task':task})

def update(request,id):
    task =Tasks.objects.get(id=id)
    form = TodoForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    
    return render(request,'todo_app/edit.html',{'form':form, 'task':task})