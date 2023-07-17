from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Room
from django.http import JsonResponse

@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    Room.objects.create(uuid=uuid, client=name, url=url)
    return JsonResponse({'message': 'room created'})


@login_required
def admin(request):
    pass
@login_required
def room(request, uuid):
    pass
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
