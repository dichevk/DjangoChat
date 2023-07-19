from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Room
from account.models import User
from django.http import JsonResponse
from django.shortcuts import render

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
    pass
@login_required
def user_detail(request, uuid):
    pass
@login_required
def edit_user(request, uuid):
    pass
@login_required
def add_user(request):
    pass
