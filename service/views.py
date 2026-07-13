from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm, LoginForm,ProviderForm,BookingForm
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Provider, Category,ProviderWork,ProviderBlockedDate,Booking
from django.db.models import Q, Sum, Count



# Create your views here.
def register_view(request):
    """
    User Registration.
    GET: show empty form | POST: validate + save user.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to FixNest, {user.first_name}!')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form, 'page_title': 'Register'})


def login_view(request):
    """
    User Login — authenticate credentials, start session.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, "provider") and user.provider.is_blocked:
                messages.error(request, "Your account has been blocked by admin.")
                return redirect("login")
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!❤')
            if hasattr(user, "provider"):
                return redirect("provider_dashboard")
            else:
                 return redirect("customer_dashboard")
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'page_title': 'Login'})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out. Visit again! ')
    return redirect('home')
def is_admin(user):
    return user.is_staff or user.is_superuser




@login_required
def book_service(request, slug):

    provider = get_object_or_404(Provider, slug=slug)

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.customer = request.user

            booking.provider = provider

            booking.save()

            messages.success(request, "Booking request sent successfully!")

            return redirect("provider_detail", slug=provider.slug)

    else:

        form = BookingForm()

    return render(
        request,
        "booking.html",
        {
            "provider": provider,
            "form": form,
        },
    )


# ─── HOME VIEW ────────────────────────────────────────────────────────────────
def home(request):
    """
    Home page — shows featured providers, categories, bestsellers.
    GET request → fetch data → render template.
    """
    categories = Category.objects.all()
    featured_providers = Provider.objects.filter(is_featured=True, availability='available')[:6]
    bestsellers = Provider.objects.filter(is_bestworker=True)[:4]
    all_providers = Provider.objects.filter(availability='available')[:12]

    context = {
        'categories': categories,
        'featured_providers': featured_providers,
        'bestsellers': bestsellers,
        'all_providers': all_providers,
        'page_title': 'Home',
    }
    return render(request, 'home.html', context)

def gallery(request):

    providers = Provider.objects.filter(
        availability='available',
        is_approved=True
    )

    categories = Category.objects.all()

    category_slug = request.GET.get('category', '')
    if category_slug:
        providers = providers.filter(category__slug=category_slug)

    search_query = request.GET.get('q', '')
    if search_query:
        providers = providers.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    sort_by = request.GET.get('sort', '-created_at')

    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'newest': '-created_at',
        'rating': '-rating',
    }

    providers = providers.order_by(sort_options.get(sort_by, '-created_at'))

    context = {
        'providers': providers,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
        'page_title': 'Provider Gallery',
    }

    return render(request, 'gallery.html', context)



def provider_register(request):

    if request.method == "POST":

        form = ProviderForm(request.POST, request.FILES)

        if form.is_valid():

            if form.cleaned_data["password"] != form.cleaned_data["confirm_password"]:
                messages.error(request, "Passwords do not match.")
                return render(request, "provider_register.html", {"form": form})

            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                messages.error(request, "Username already exists.")
                return render(request, "provider_register.html", {"form": form})

            # Create Login Account
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            # Create Provider
            provider = form.save(commit=False)
            provider.user = user
            if not provider.slug:
                provider.slug = slugify(provider.name)
            provider.save()

            # Save Recent Completed Work
            ProviderWork.objects.create(
                provider=provider,
                work_title=form.cleaned_data["work_title"],
                work_image=form.cleaned_data["work_image"],
                customer_name=form.cleaned_data["customer_name"],
                customer_phone=form.cleaned_data["customer_phone"],
                work_address=form.cleaned_data["work_address"],
                completed_date=form.cleaned_data["completed_date"],
            )

            messages.success(request, "Provider Registered Successfully.")

            return redirect("gallery")

    else:
        form = ProviderForm()

    return render(
        request,
        "provider_register.html",
        {"form": form},
    )

def provider_detail(request, slug):

    provider = get_object_or_404(Provider, slug=slug)

    today = timezone.now().date()

    related = Provider.objects.filter(
        category=provider.category
    ).exclude(id=provider.id)[:4]

    recent_works = ProviderWork.objects.filter(provider=provider)

    blocked = ProviderBlockedDate.objects.filter(
        provider=provider,
        start_time__lte=today,
        end_time__gte=today
    ).first()

    context = {
        "provider": provider,
        "related": related,
        "recent_works": recent_works,
        "blocked": blocked,
    }

    return render(request, "provider_detail.html", context)



@login_required
def provider_dashboard(request):

    provider = get_object_or_404(
        Provider,
        user=request.user
    )

    bookings = Booking.objects.filter(
        provider=provider
    ).order_by("-booking_date", "-booking_time")

    return render(
        request,
        "provider_dashboard.html",
        {
            "provider": provider,
            "bookings": bookings,
        },
    )

@login_required
def accept_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        provider__user=request.user
    )

    booking.status = "Accepted"
    booking.save()

    messages.success(request, "Booking Accepted.")

    return redirect("provider_dashboard")

@login_required
def reject_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        provider__user=request.user
    )

    booking.status = "Rejected"
    booking.save()

    messages.success(request, "Booking Rejected.")

    return redirect("provider_dashboard")
@login_required
def complete_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        provider__user=request.user
    )

    booking.status = "Completed"
    booking.save()

    messages.success(request, "Booking marked as Completed.")

    return redirect("provider_dashboard")


@login_required
def customer_dashboard(request):

    bookings = Booking.objects.filter(
        customer=request.user
    ).order_by("-booking_date", "-booking_time")

    return render(
        request,
        "customer_dashboard.html",
        {
            "bookings": bookings,
        },
    )