from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from bbq_organizer.models import Event
from bbq_organizer import forms


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def create_event(request):
    if request.method == 'POST':
        form = forms.EventForm(request.POST)
        if form.is_valid():
            intermediate_form = form.save(commit=False)
            intermediate_form.author = request.user
            slug = intermediate_form.save()
            return redirect(f"/events/admin/{slug}")
    else:
        form = forms.EventForm()

    return render(request, "create_event.html", {"form": form})


@login_required
def admin_event(request, slug):
    event = Event.objects.filter(slug=slug)
    if event:
        return render(request, "admin_event.html")
    else:
        return redirect("/")


@login_required
def events_list(request):
    events = Event.objects.filter(author__pk=request.user.id)
    print(events)
    return render(request, "events_list.html", {"events": events})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.add_message(
                request, messages.INFO, f"{username} signed up successfully"
            )
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})
