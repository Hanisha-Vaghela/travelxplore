from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Traveler, ContactMessage, UserProfile, Destination
from .forms import TravelerForm, ContactForm, UserRegistrationForm, UserProfileForm, DestinationForm

# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    # Get featured destinations for slider
    featured_destinations = Destination.objects.filter(is_featured=True)[:8]
    
    context = {
        'title': 'Welcome to TravelXplore',
        'featured_destinations': featured_destinations,
    }
    return render(request, 'home.html', context)

def about(request):
    context = {
        'title': 'About Us',
        'details': 'We are a small company providing excellent services.'
    }
    return render(request, 'about.html', context)

def gallery(request):
    # Get all destinations for gallery
    destinations = Destination.objects.all()
    
    context = {
        'title': 'Gallery',
        'destinations': destinations,
    }
    return render(request, 'gallery.html', context)

# ============ AUTHENTICATION VIEWS ============

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone', '')
            )
            
            # IMPORTANT: Automatically log in the user after registration
            login(request, user)
            
            messages.success(request, f'🎉 Welcome {username}! Your account has been created successfully!')
            return redirect('profile')  # Redirect to profile instead of login
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'✅ Welcome back, {user.username}!')
            
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, '❌ Invalid username or password!')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, '👋 You have been logged out successfully!')
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form, 'profile': profile})

# ============ CONTACT VIEW ============

@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.user = request.user
            contact_message.save()
            messages.success(request, '✅ Thank you! Your message has been sent successfully!')
            return redirect('contact')
    else:
        initial_data = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        if hasattr(request.user, 'userprofile'):
            initial_data['phone'] = request.user.userprofile.phone
        
        form = ContactForm(initial=initial_data)
    
    context = {
        'title': 'Contact Us',
        'form': form,
    }
    return render(request, 'contact.html', context)

# ============ TRAVELER CRUD ============

@login_required(login_url='login')
def traveler_list(request):
    travelers = Traveler.objects.filter(user=request.user)
    return render(request, 'traveler_list.html', {'travelers': travelers})

@login_required(login_url='login')
def traveler_create(request):
    if request.method == 'POST':
        form = TravelerForm(request.POST)
        if form.is_valid():
            traveler = form.save(commit=False)
            traveler.user = request.user
            traveler.save()
            messages.success(request, '✅ Traveler added successfully!')
            return redirect('traveler_list')
    else:
        form = TravelerForm()

    return render(request, 'traveler_form.html', {'form': form})

@login_required(login_url='login')
def traveler_update(request, id):
    traveler = get_object_or_404(Traveler, id=id, user=request.user)
    form = TravelerForm(request.POST or None, instance=traveler)

    if form.is_valid():
        form.save()
        messages.success(request, '✅ Traveler updated successfully!')
        return redirect('traveler_list')

    return render(request, 'traveler_form.html', {'form': form})

@login_required(login_url='login')
def traveler_delete(request, id):
    traveler = get_object_or_404(Traveler, id=id, user=request.user)

    if request.method == 'POST':
        traveler.delete()
        messages.success(request, '✅ Traveler deleted successfully!')
        return redirect('traveler_list')

    return render(request, 'traveler_confirm_delete.html', {'traveler': traveler})

# ============ MESSAGE VIEWS ============

@login_required(login_url='login')
def message_list(request):
    if request.user.is_staff:
        messages_all = ContactMessage.objects.all()
    else:
        messages_all = ContactMessage.objects.filter(user=request.user)
    
    return render(request, 'message_list.html', {'messages': messages_all})

@login_required(login_url='login')
def message_detail(request, id):
    if request.user.is_staff:
        message = get_object_or_404(ContactMessage, id=id)
    else:
        message = get_object_or_404(ContactMessage, id=id, user=request.user)
    
    message.is_read = True
    message.save()
    return render(request, 'message_detail.html', {'message': message})

@login_required(login_url='login')
def message_delete(request, id):
    if request.user.is_staff:
        message = get_object_or_404(ContactMessage, id=id)
    else:
        message = get_object_or_404(ContactMessage, id=id, user=request.user)
    
    if request.method == 'POST':
        message.delete()
        messages.success(request, '✅ Message deleted successfully!')
        return redirect('message_list')
    
    return render(request, 'message_confirm_delete.html', {'message': message})

# ============ DESTINATION VIEWS (Admin Only) ============

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.created_by = request.user
            destination.save()
            messages.success(request, '✅ Destination added successfully!')
            return redirect('destination_list')
    else:
        form = DestinationForm()
    
    return render(request, 'destination_form.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def destination_update(request, id):
    destination = get_object_or_404(Destination, id=id)
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Destination updated successfully!')
            return redirect('destination_list')
    else:
        form = DestinationForm(instance=destination)
    
    return render(request, 'destination_form.html', {'form': form, 'destination': destination})

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def destination_delete(request, id):
    destination = get_object_or_404(Destination, id=id)
    
    if request.method == 'POST':
        destination.delete()
        messages.success(request, '✅ Destination deleted successfully!')
        return redirect('destination_list')
    
    return render(request, 'destination_confirm_delete.html', {'destination': destination})

# Public destination detail view (everyone can see)
def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    return render(request, 'destination_detail.html', {'destination': destination})