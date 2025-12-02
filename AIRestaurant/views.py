from django.shortcuts import render
from django.http import JsonResponse
from subprocess import run as shell
from urllib.parse import unquote
from django.shortcuts import get_object_or_404
from .data.users import User as DataUser
from .data.customer import Customer, DishRating
from .data.chef import Chef
from .data.deliverer import Deliverer
from .data.manager import Manager
from .data.message import Compliment, Complaint
from django.db.models import Avg

def home(request):
    return render(request, 'index.html')

def add_to_cart(request):
    return render(request, 'cart.html')

def ai_chat(request):
    AI_PATH = "/home/SapphireBrick613/AI"
    question = unquote(request.POST.get('query'))
    result = shell(
        [f'{AI_PATH}/llama-run', f'{AI_PATH}/tinyllama-1.1b-chat-v1.0.Q4_0.gguf'],
        capture_output=True,
        input=question,
        encoding='utf-8')
    response = result.stdout.replace("\x1b[0m", "") if result.returncode == 0 else "<AI failed>"

    return JsonResponse({
        "answer": response,
        "rating_id": 0,
        "source": "AI",
    })


def profile_view(request, user_id):
    """Render combined dashboard + public profile for the given user id.

    Chooses template based on the target user's type: customer/chef/deliverer/manager.
    This view provides `target`, `profile`, `compliments`, `complaints`,
    `avg_dish_rating` (when relevant), and `can_view_private` in the context.
    """
    target = get_object_or_404(DataUser, pk=user_id)

    # viewer is the Django request.user (project templates already reference `user`)
    viewer = request.user

    # default context values
    context = {
        'target': target,
        'user': viewer,  # keep same variable name templates expect
        'viewer': viewer,
        'profile': None,
        'compliments': [],
        'complaints': [],
        'avg_dish_rating': None,
        'can_view_private': False,
    }

    # load profile model instance if present
    if target.type == 'CU':
        context['profile'] = Customer.objects.filter(login=target).first()
    elif target.type == 'CH':
        context['profile'] = Chef.objects.filter(login=target).first()
    elif target.type == 'DL':
        context['profile'] = Deliverer.objects.filter(login=target).first()
    elif target.type == 'MN':
        context['profile'] = Manager.objects.filter(login=target).first()

    # compliments and complaints (show latest first)
    context['compliments'] = list(Compliment.objects.filter(to=target).select_related('sender', 'message').order_by('-id')[:50])
    context['complaints'] = list(Complaint.objects.filter(to=target).select_related('sender', 'message').order_by('-id')[:50])

    # compute average dish rating for chefs
    if target.type == 'CH':
        try:
            avg = DishRating.objects.filter(dish__chef__login=target).aggregate(avg=Avg('rating'))['avg']
            if avg is not None:
                context['avg_dish_rating'] = round(avg, 2)
        except Exception:
            context['avg_dish_rating'] = None

    # permission: allow manager (staff/superuser) or owner to view private fields
    is_manager_viewer = getattr(viewer, 'is_staff', False) or getattr(viewer, 'is_superuser', False)
    is_owner = getattr(viewer, 'id', None) == getattr(target, 'id', None)
    context['can_view_private'] = is_manager_viewer or is_owner

    # pick template by target type
    tpl_map = {'CU': 'customer.html', 'CH': 'chef.html', 'DL': 'deliverer.html', 'MN': 'manager.html'}
    tpl = tpl_map.get(target.type, 'customer.html')

    return render(request, tpl, context)