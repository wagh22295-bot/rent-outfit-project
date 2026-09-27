from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Category, Outfit, Booking, LateFee, User
from .forms import CustomUserCreationForm, BookingForm
from django.contrib import messages
from django.db.models import Q

def landing(request):
    return render(request, 'core/landing.html')

def home(request):
    featured_outfits = Outfit.objects.all()[:4]
    categories = Category.objects.all()
    return render(request, 'core/home.html', {
        'featured_outfits': featured_outfits,
        'categories': categories
    })

def shop(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')
    outfits = Outfit.objects.all()
    
    if query:
        outfits = outfits.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_slug:
        outfits = outfits.filter(category__slug=category_slug)
        
    categories = Category.objects.all()
    return render(request, 'core/shop.html', {
        'outfits': outfits,
        'categories': categories
    })

def outfit_detail(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.outfit = outfit
            
            # Simple validation: Check if outfit is available for these dates
            # (In a real app, this would be more complex)
            existing_bookings = Booking.objects.filter(
                outfit=outfit,
                status__in=['Confirmed', 'Rented'],
                start_date__lt=booking.end_date,
                end_date__gt=booking.start_date
            )
            
            if existing_bookings.exists():
                messages.error(request, "This outfit is already booked for the selected dates.")
            else:
                booking.save()
                messages.success(request, "Booking request sent successfully!")
                return redirect('my_bookings')
    else:
        form = BookingForm()
        
    return render(request, 'core/outfit_detail.html', {
        'outfit': outfit,
        'form': form
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/my_bookings.html', {'bookings': bookings})

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_outfits = Outfit.objects.count()
    total_bookings = Booking.objects.count()
    recent_bookings = Booking.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_outfits': total_outfits,
        'total_bookings': total_bookings,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'core/admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_booking_list(request):
    status_filter = request.GET.get('status')
    bookings = Booking.objects.all().order_by('-created_at')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
        
    return render(request, 'core/admin_booking_list.html', {'bookings': bookings})

@user_passes_test(lambda u: u.is_staff)
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)
    
    # Handle Late Fee if marking as Returned
    if status == 'Returned' and booking.status != 'Returned':
        from datetime import date
        from decimal import Decimal
        today = date.today()
        if today > booking.end_date:
            days_late = (today - booking.end_date).days
            # Late fee = days * price_per_day * 1.5 (50% penalty)
            fee = Decimal(days_late) * booking.outfit.price_per_day * Decimal('1.5')
            LateFee.objects.get_or_create(
                booking=booking,
                defaults={
                    'days_late': days_late,
                    'fee_amount': fee
                }
            )
            messages.warning(request, f"Late fee of ₹{fee} generated for {days_late} days delay.")

    booking.status = status
    booking.save()
    messages.success(request, f"Booking status updated to {status}")
    return redirect('admin_booking_list')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
