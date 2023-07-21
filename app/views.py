from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Room
from account.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from account.forms import EditUserForm


@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    Room.objects.create(uuid=uuid, client=name, url=url)
    return JsonResponse({'message': 'room created'})


@login_required
def admin(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff = True)

    return render(request,'app/admin.html', {
        'rooms': rooms,
        'users': users
    })


@login_required
def room(request, uuid):
    room = Room.objects.get(uuid=uuid)
    if room.status != Room.ACTIVE:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()
    return render(request, 'app/room.html', {
        'room':room
    })

@login_required
def delete_room(request, uuid):
    if request.user.has_perm('room.delete_room'):
        room = Room.objects.get(uuid=uuid)
        room.delete()
                
        messages.success(request, 'The room was deleted!')

        return redirect('/app-admin/')
    else:
        messages.error(request, 'You don\'t have access to delete rooms!')

        return redirect('/app-admin/')
@login_required
def user_detail(request, uuid):
    user = User.objects.get(pk=uuid)
    rooms = user.rooms.all()

    return render(request, 'app/user_detail.html', {
        'user': user,
        'rooms': rooms
    })
@login_required
def edit_user(request, uuid):
    if request.user.has_perm('user.edit_user'):
        user = User.objects.get(pk=uuid)

        if request.method == 'POST':
            form = EditUserForm(request.POST, instance=user)

            if form.is_valid():
                form.save()
                
                messages.success(request, 'The changes was saved!')

                return redirect('/chat-admin/')
        else:
            form = EditUserForm(instance=user)

        return render(request, 'chat/edit_user.html', {
            'user': user,
            'form': form
        })
    else:
        messages.error(request, 'You don\'t have access to edit users!')

        return redirect('/chat-admin/')
@login_required
def add_user(request):
    pass
