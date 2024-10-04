from django.shortcuts import render,redirect,reverse
from worker import models as wmodels
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from worker import forms as wforms
from consumer import models as cmodels
from consumer import forms as cforms

# Create your views here.


def home_view(request):
    return render(request,'owner/home.html')

def register_view(request):
    return render(request,'owner/register.html')

def login_view(request):
    return render(request,'owner/login.html')

def is_consumer(user):
    return user.groups.filter(name='CONSUMER').exists()

def is_worker(user):
    return user.groups.filter(name='WORKER').exists()


def afterlogin_view(request):
    if is_consumer(request.user):
        return redirect('consumer-dashboard')
    elif is_worker(request.user):
        account_approval = wmodels.Worker.objects.all().filter(user_id=request.user.id,status=True)
        if account_approval:
            return redirect('worker-dashboard')
        else:
            return render(request,'owner/waiting_for_approval.html')
        # return redirect('worker-dashboard')
    else:
        return redirect('admin-dashboard')
    
def admin_dashboard_view(request):
    return render(request,'owner/admin_dashboard.html')

def worker_request_view(request):
    worker = wmodels.Worker.objects.all()
    return render(request,'owner/worker_request.html',{'worker':worker})

def approve_worker_view(request,pk):
    worker =  wmodels.Worker.objects.get(id=pk)
    worker.status=True
    worker.save()
    return redirect(reverse('admin-approve-worker'))

def admin_approve_worker(request):
    worker = wmodels.Worker.objects.all()
    return render(request,'owner/worker_request.html',{'worker':worker})

def reject_worker_view(request,pk):
    worker = wmodels.Worker.objects.get(id=pk)
    user = User.objects.get(id=worker.user_id)
    worker.delete()
    user.delete()
    return redirect('worker-request')

def manage_worker_view(request):
    worker = wmodels.Worker.objects.all()
    return render(request,'owner/manage_worker.html',{'worker':worker})

def update_worker_view(request, pk):
    worker = get_object_or_404(wmodels.Worker, id=pk)
    user = get_object_or_404(User, id=worker.user_id)
    
    if request.method == 'POST':
        workerForm = wforms.WorkerForm(request.POST, request.FILES, instance=worker)
        userform = wforms.WorkerUserForm(request.POST, request.FILES, instance=user)  # Note: should use 'user' instead of 'consumer'

        if workerForm.is_valid() and userform.is_valid():
            user = userform.save()  # Save the user instance
            worker = workerForm.save(commit=False)
            worker.user = user  # Associate the user with the consumer
            worker.save()
            return redirect('manage-worker')
    else:
        userform = wforms.WorkerUserForm(instance=user)  # Initialize user form with user instance
        workerForm = wforms.WorkerForm(instance=worker)  # Initialize consumer form with consumer instance

    return render(request, 'owner/update_worker.html', {
        'workerform': workerForm, 
        'worker': worker, 
        'userform': userform
    })

def delete_worker_view(request,pk):
    worker=wmodels.Worker.objects.get(id=pk)
    user=User.objects.get(id=worker.user_id)
    worker.delete()
    user.delete()
    return redirect('manage-worker')

def manage_consumer_view(request):
    consumer = cmodels.Consumer.objects.all()
    return render(request,'owner/manage_consumer.html',{'consumer':consumer})

def update_consumer_view(request, pk):
    consumer = get_object_or_404(cmodels.Consumer, id=pk)
    user = get_object_or_404(User, id=consumer.user_id)
    
    if request.method == 'POST':
        consumerform = cforms.ConsumerForm(request.POST, request.FILES, instance=consumer)
        userform = cforms.ConsumerUserForm(request.POST, request.FILES, instance=user)  # Note: should use 'user' instead of 'consumer'

        if consumerform.is_valid() and userform.is_valid():
            user = userform.save()  # Save the user instance
            consumer = consumerform.save(commit=False)
            consumer.user = user  # Associate the user with the consumer
            consumer.save()
            return redirect('manage-consumer')
    else:
        userform = cforms.ConsumerUserForm(instance=user)  # Initialize user form with user instance
        consumerform = cforms.ConsumerForm(instance=consumer)  # Initialize consumer form with consumer instance

    return render(request, 'owner/update_consumer.html', {
        'consumerform': consumerform, 
        'consumer': consumer, 
        'userform': userform
    })

def delete_consumer_view(request,pk):
    is_consumer=cmodels.Consumer.objects.get(id=pk)
    user=User.objects.get(id=is_consumer.user_id)
    is_consumer.delete()
    user.delete()
    return redirect('manage-consumer')