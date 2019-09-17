import json

from collections import defaultdict

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotFound
)
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from bbq_organizer.models import Event
from bbq_organizer.models import MeatType
from bbq_organizer.models import MeatOption
from bbq_organizer.models import MeatChoice
from bbq_organizer.models import SignUp

from bbq_organizer import forms


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def create_event(request):
    meats = MeatType.objects.all().order_by("name")

    if request.method == "POST":
        form = forms.EventForm(request.POST)
        if form.is_valid():
            intermediate_form = form.save(commit=False)
            intermediate_form.author = request.user
            event = intermediate_form.save()
            slug = event.slug

            meats = json.loads(request.POST["meats"])
            for key, value in meats.items():
                if value:
                    option = MeatOption(event=event, meat_id=key)
                    option.save()
            return redirect("/events/admin/{}".format(slug))
    else:
        form = forms.EventForm()

    meats_chosen = {}
    meats_chosen_string = request.POST.get("meats")
    if meats_chosen_string:
        meats_chosen = json.loads(meats_chosen_string)

    keys = list(meats_chosen.keys())
    for key in keys:
        if meats_chosen[key]["selected"] is False:
            del meats_chosen[key]
    return render(
        request,
        "create_event.html",
        {"form": form, "meats": meats, "meats_chosen": meats_chosen},
    )


@login_required
def admin_event(request, slug):
    event = Event.objects.filter(slug=slug).first()
    if event is None:
        return redirect("/")
    host = request.get_host()

    signups = SignUp.objects.filter(event__pk=event.id)
    meatchoices = []

    total = 0
    for signup in signups:
        meatchoices.extend(MeatChoice.objects.filter(signup__pk=signup.id))
        total += signup.extras + 1

    meat_count = defaultdict(int)
    for meatchoice in meatchoices:
        meat_count[meatchoice.meat.name] += 1

    if event:
        return render(
            request,
            "admin_event.html",
            {
                "event": event,
                "host": host,
                "meats": dict(meat_count),
                "signups": signups,
                "total": total,
            },
        )
    else:
        return redirect("/")


def invite_event(request, slug):
    value = request.COOKIES.get("registered")
    if value != slug:
        event = Event.objects.filter(slug=slug).first()
        if event:
            meats = MeatOption.objects.filter(event__pk=event.id)
            return render(
                request, "invite_event.html", {"event": event, "meats": meats}
            )
        else:
            return render(request, "does_not_exist.html")
    return render(request, "already_registered.html")


@csrf_exempt
@login_required
def register_event(request, slug):
    if request.method == "POST":
        value = request.COOKIES.get("registered")
        if value != slug:
            data = json.loads(request.body)
            extras = data["extras"]
            name = data["name"]
            event = Event.objects.filter(slug=slug).first()
            if event is None:
                return HttpResponseNotFound()
            try:
                extras = int(extras)
            except ValueError:
                return HttpResponseBadRequest()
            signup = SignUp(event=event, extras=extras, name=name)
            signup = signup.save()

            for meat in data["meats"]:
                meat_id = int(meat)
                meat_choice = MeatChoice(signup=signup, meat_id=meat_id)
                meat_choice.save()

            response = HttpResponse()
            response.set_cookie("registered", slug)
            return response
        else:
            return HttpResponseForbidden()
    else:
        return render(request, "already_registered.html")


@login_required
def events_list(request):
    events = Event.objects.filter(author__pk=request.user.id)
    return render(request, "events_list.html", {"events": events})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.add_message(
                request, messages.INFO, "{} signed up successfully".format(username)
            )
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


@login_required
@csrf_exempt
def delete_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            Event.objects.get(slug=data["slug"]).delete()
        except Event.DoesNotExist:
            pass

        return HttpResponse("")


def view_404(request, exception):
    return redirect("/")
