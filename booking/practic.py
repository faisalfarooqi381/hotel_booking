from django.shortcuts import redirect,render,get_object_or_404
from django.contrib import messages
from .models import Room, Booking, Customer
from  .forms import BookingForm

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/rooms.html', {'rooms': rooms})

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    form = BookingForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            # date validation
            if check_out <= check_in:
                messages.error(request, 'Checkout date is after Check_in date')
                return redirect('book_room', room_id=room.id)
            
            # Overlapping
            overlapping = Booking.objects.filter(
                room=room,
                check_In__lt = check_out,
                check_out__gt = check_in
            ).exists()

            if overlapping:
                messages.error(request, 'Room is already booked in dates')
                return redirect('book_room', room_id=room.id)
            
            else: # customer create
                customer = Customer.objects.create(
                    name = form.cleaned_data['name'],
                    email = form.cleaned_data['email'],
                    phone = form.cleaned_data['phone'],
                )

                # total days create
                days = (check_out - check_in).days
        




