from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Booking, Customer

# def room_list(request):
#     rooms = Room.objects.all()
#     return render(request, 'booking/rooms.html', {'rooms':rooms})


from .forms import BookingForm, AvailabilityForm
from django.contrib import messages
from datetime import timedelta


def room_list(request):
    rooms = Room.objects.all()
    form = AvailabilityForm(request.GET or None)

    if form.is_valid():
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']

        booked_rooms = Booking.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)

        rooms = Room.objects.exclude(id__in=booked_rooms)

    return render(request, 'booking/rooms.html', {
        'rooms': rooms,
        'form': form
    })


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    # form = BookingForm(request.POST or None)

    # Auto initial dates
    initial_data = {
    'check_in': request.GET.get('check_in'),
    'check_out': request.GET.get('check_out'),
    }

    form = BookingForm(request.POST or None, initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            
             # ✅ DATE VALIDATION (ADD HERE)
            if check_out <= check_in:
                messages.error(request, "Check-out must be after check-in")
                return redirect('book_room', room_id=room.id)


            # 🔥 Overlapping booking check
            overlapping = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in
            ).exists()

            if overlapping:
                messages.error(request, "Room already booked for selected dates!")
                return redirect('book_room', room_id=room.id)
            else:
                # Customer create
                customer = Customer.objects.create(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                )

                # Total days calculate
                days = (check_out - check_in).days
                total_price = days * room.price

                # Booking save
                booking = Booking.objects.create(
                    room=room,
                    customer=customer,
                    check_in=check_in,
                    check_out=check_out,
                    total_price=total_price
                )

                messages.success(request, "Booking Successful!")
                return redirect('booking_success', booking_id=booking.id)

    return render(request, 'booking/book_room.html', {'form': form, 'room': room})

# For Booking success page for voucher
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking/booking_success.html', {'booking': booking})

def booking_voucher(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking/booking_voucher.html', {'booking': booking})
