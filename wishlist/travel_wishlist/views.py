from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required
def place_list(request):
    if request.method == 'POST':
        # Create new place
        form = NewPlaceForm(request.POST)  # create a form the data in the request
        place = form.save(commit=False) # create a model object from form
        place.user = request.user
        if form.is_valid(): # validation against DB constraints
            place.save() #saves place to db
            return redirect('place_list') #reloads home page.

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create html
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user, visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # creates an object using the model data the position of the primary key
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    return redirect('place_list')

@login_required
def place_details(request, place_pk): # takes user request data and place_pk from urls.py as parameters
    place = get_object_or_404(Place, pk=place_pk) # assigns the model object at the pk position of place_pk

    if place.user != request.user: # verify that the place belongs to the user requesting it
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form  = TripReviewForm(request.POST, request.FILES, instance = place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated')
        else:
            messages.error(request, form.errors) # can be refined later

        return redirect('place_details', place_pk=place_pk)
    
    else:
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


def about(request):
    author='Lucas'
    about= 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
