from xml.dom.minidom import parseString

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from syndicat.forms import CustomerForm, SubscriberForm
from syndicat.models import Subscriber

@login_required
def home(request):
    success = request.GET.get('success') == '1'
    success_edit = request.GET.get('success_edit') == '1'
    query = request.GET.get('query', '')
    subscribers = Subscriber.objects.all().order_by('name')

    if query:
        subscribers = subscribers.filter(
            Q(name__icontains=query) |
            Q(customer__first_name=query) |
            Q(customer__last_name=query)
        )

    paginator = Paginator(subscribers, 10)
    page = request.GET.get('page')
    subscribers = paginator.get_page(page)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/subscriber_table.html', {'page_obj': subscribers})
        pagination = render_to_string('partials/pagination.html', {'page_obj': subscribers})
        return JsonResponse({'html': html, 'pagination': pagination})

    return render(request, 'home.html', {'page_obj': subscribers, 'success': success, 'success_edit': success_edit})


def add_subscriber(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        subscriber_form = SubscriberForm(request.POST)

        if customer_form.is_valid() and subscriber_form.is_valid():
            customer = customer_form.save()
            subscriber = subscriber_form.save(commit=False)
            subscriber.customer = customer
            subscriber.save()

            if request.user.is_authenticated:
                return redirect(f"{reverse('home')}?success=1")
            else:
                return redirect(f"{reverse('login')}?success=1")
    else:
        customer_form = CustomerForm()
        subscriber_form = SubscriberForm()

    success = request.GET.get("success") == "1"

    return render(request, 'add_subscriber.html', {
        'customer_form': customer_form,
        'subscriber_form': subscriber_form,
        'success': success,
    })

@login_required
def edit_subscriber(request, subscriber_id):

    if not request.user.is_superuser:
        return redirect('home')

    subscriber = get_object_or_404(Subscriber, id=subscriber_id)
    customer = subscriber.customer

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, instance=customer)
        subscriber_form = SubscriberForm(request.POST, instance=subscriber)

        if customer_form.is_valid() and subscriber_form.is_valid():
            customer_form.save()
            subscriber_form.save()
            return redirect(f"{reverse('home')}?success_edit=1")
    else:
        customer_form = CustomerForm(instance=customer)
        subscriber_form = SubscriberForm(instance=subscriber)

    return render(request, 'edit_subscriber.html', {
        'customer_form': customer_form,
        'subscriber_form': subscriber_form,
        'subscriber_id': subscriber_id,
        'subscriber': subscriber
    })


@require_POST
@login_required
def delete_subscriber_ajax(request):

    if not request.user.is_superuser:
        return redirect('home')

    subscriber_id = request.POST.get('subscriber_id')
    try:
        subscriber = Subscriber.objects.get(pk=subscriber_id)
        subscriber.delete()
        return JsonResponse({'success': True})
    except Subscriber.DoesNotExist:
        return JsonResponse({'success': False, 'error': "L'adhérent n'existe pas"}, status=404)

@login_required
def call_webservice(request):
    return render(request, 'webservice.html')

def format_xml(raw_xml: str) -> str:
    dom = parseString(raw_xml)
    pretty = dom.toprettyxml(indent="    ")

    pretty_cleaned = "\n".join([line for line in pretty.split('\n') if line.strip()])

    return pretty_cleaned


@login_required
@csrf_exempt
def check_siret_ajax(request):
    if request.method == 'POST':
        siret = request.POST.get('siret', '').strip()
        if not siret:
            return JsonResponse({'success': False, 'xml': '<Response>False</Response>'})

        subscriber = Subscriber.objects.filter(siret=siret).first()

        if subscriber:
            raw_xml = f"""<WebService>
            <Entity>
            <Entreprise>{escape(subscriber.name)}</Entreprise>
            <RepresentantNom>{escape(subscriber.customer.first_name)}</RepresentantNom>
            <RepresentantPrenom>{escape(subscriber.customer.last_name)}</RepresentantPrenom>
            <Response>True</Response>
            </Entity>
            </WebService>"""

        else:
            raw_xml = """<WebService>
            <Entity>
            <Response>False</Response>
            </Entity>
            </WebService>"""

        xml_clean = format_xml(raw_xml)

        return JsonResponse({'success': True, 'xml': xml_clean})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Un compte avec cet email existe déjà')
        else:
            User.objects.create_user(username=email, email=email, password=password)
            return redirect('/?registered=1')

    return render(request, 'auth/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('/accueil?login=1')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except User.DoesNotExist:
            messages.error(request, "Aucun utilisateur trouvé avec cet e-mail.")

    return render(request, 'auth/login.html')
