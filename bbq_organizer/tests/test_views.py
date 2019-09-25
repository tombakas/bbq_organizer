import json

from random import randint
from datetime import datetime as dt
from datetime import timedelta as td

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

import bbq_organizer.views as bbq_views

from bbq_organizer.models import Event
from bbq_organizer.models import SignUp
from bbq_organizer.models import MeatType
from bbq_organizer.models import MeatOption
from bbq_organizer.models import MeatChoice


class TestHomeView(TestCase):
    def setUp(self):
        self.password = "secret"
        self.user = User.objects.create_user(
            username="bbq_user", password=self.password
        )

    def test_url_resolves_to_view(self):
        found = resolve("/")
        self.assertEqual(found.func, bbq_views.home)

    def test_home_not_logged_in(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_home_logged_in(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class TestCreateEventView(TestCase):
    def setUp(self):
        self.password = "secret"
        self.user = User.objects.create_user(
            username="bbq_user", password=self.password
        )
        self.now = dt.now().strftime("%Y-%m-%d")
        self.yesterday = (dt.now() - td(days=1)).strftime("%Y-%m-%d")

        self.meat_1 = MeatType(name="Bacon")
        self.meat_1.save()
        self.meat_2 = MeatType(name="Chicken")
        self.meat_2.save()

    def test_url_resolves_to_view(self):
        found = resolve("/create_event/")
        self.assertEqual(found.func, bbq_views.create_event)

    def test_non_logged_in_request(self):
        response = self.client.get("/create_event/")
        self.assertEqual(response.status_code, 302)

    def test_logged_in_request(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get("/create_event/")
        self.assertEqual(response.status_code, 200)

    def test_create_event_without_meat(self):
        body = {"date": self.now}

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post("/create_event/", data=body)
        url = response.url.rsplit("/", 1)[0]

        self.assertEqual(response.status_code, 302)
        self.assertEqual(url, "/events/admin")

    def test_create_event_with_meat(self):
        body = {
            "date": self.now,
            "meats": json.dumps({self.meat_1.pk: True, self.meat_2.pk: True}),
        }

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post("/create_event/", data=body)
        url = response.url.rsplit("/", 1)[0]
        slug = response.url.split("/")[-1]

        event = Event.objects.get(slug=slug)
        meat_options = MeatOption.objects.filter(event__pk=event.pk)
        meat_options_ids = {meat.pk for meat in meat_options}
        meat_submited_ids = {self.meat_1.pk, self.meat_2.pk}

        self.assertEqual(len(meat_options), 2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(meat_options_ids, meat_submited_ids)
        self.assertEqual(url, "/events/admin")

    def test_create_event_with_malformed_meat(self):
        body = {"date": self.now, "meats": "this is not a json"}

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post("/create_event/", data=body)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")

    def test_meats_maintained_on_bad_date(self):
        original_meats = {str(self.meat_1.pk): True, str(self.meat_2.pk): True}

        body = {"date": self.yesterday, "meats": json.dumps(original_meats)}

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post("/create_event/", data=body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(original_meats, response.context["meats_chosen"])

    def test_handle_unselected_meats(self):
        original_meats = {str(self.meat_1.pk): True, str(self.meat_2.pk): True}

        original_meats["1000"] = False

        body = {"date": self.yesterday, "meats": json.dumps(original_meats)}

        del original_meats["1000"]

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post("/create_event/", data=body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(original_meats, response.context["meats_chosen"])

        with self.assertRaises(KeyError):
            response.context["meats_chosen"]["1000"]

    def test_malformed_meats_on_bad_date(self):
        body = {"date": self.yesterday, "meats": "this is not a json"}

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post("/create_event/", data=body)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")


class TestAdminEventView(TestCase):
    def setUp(self):
        self.password = "secret"
        self.user = User.objects.create_user(
            username="bbq_user", password=self.password
        )

        self.now = dt.now().strftime("%Y-%m-%d")

        self.meat_1 = MeatType(name="Bacon")
        self.meat_1.save()
        self.meat_2 = MeatType(name="Chicken")
        self.meat_2.save()

    def test_url_resolves_to_view(self):
        found = resolve("/events/admin/random_slug")
        self.assertEqual(found.func, bbq_views.admin_event)

    def test_non_existing_event(self):
        slug = "random_slug"

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get("/events/admin/{}".format(slug), {"slug": slug})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")

    def test_math(self):
        event = Event(author=self.user, date=self.now).save()

        signup_1_extras = randint(5, 10)
        signup_2_extras = randint(5, 10)

        total = signup_1_extras + signup_2_extras + 2  # counting the organizers

        signup_1 = SignUp(name="name_1", event=event, extras=signup_1_extras).save()
        signup_2 = SignUp(name="name_2", event=event, extras=signup_2_extras).save()

        meat_1_count = randint(10, 20)
        meat_2_count = randint(10, 20)

        for i in range(meat_1_count):
            MeatChoice(signup=signup_1, meat=self.meat_1).save()

        for i in range(meat_2_count):
            MeatChoice(signup=signup_2, meat=self.meat_2).save()

        self.client.login(username="bbq_user", password="secret")
        response = self.client.get(
            "/events/admin/{}".format(event.slug), {"slug": event.slug}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["meats"][self.meat_1.name], meat_1_count)
        self.assertEqual(response.context["meats"][self.meat_2.name], meat_2_count)
        self.assertEqual(response.context["total"], total)

    def test_signups(self):
        event = Event(author=self.user, date=self.now).save()

        signup_1 = SignUp(name="name_1", event=event, extras=0).save()
        signup_2 = SignUp(name="name_2", event=event, extras=0).save()

        original_signups = {signup_1, signup_2}

        self.client.login(username="bbq_user", password="secret")
        response = self.client.get(
            "/events/admin/{}".format(event.slug), {"slug": event.slug}
        )
        response_signups = {signup for signup in response.context["signups"]}
        self.assertEqual(original_signups, response_signups)

    def test_generated_url(self):
        event = Event(author=self.user, date=self.now).save()

        self.client.login(username="bbq_user", password="secret")
        response = self.client.get(
            "/events/admin/{}".format(event.slug), {"slug": event.slug}
        )
        self.assertEqual(response.status_code, 200)

        url = response.context["url"]
        url = (
            "/" + url.split("/", 1)[-1]
        )  # host in tests is "testserver", so take it out
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestInviteEventView(TestCase):
    def setUp(self):
        self.password = "secret"
        self.user = User.objects.create_user(
            username="bbq_user", password=self.password
        )
        self.now = dt.now().strftime("%Y-%m-%d")
        self.event = Event(date=self.now, author=self.user).save()

    def test_url_resolves_to_view(self):
        found = resolve("/events/invite/{}".format(self.event.slug))
        self.assertEqual(found.func, bbq_views.invite_event)

    def test_new_registration(self):
        self.client.login(username="bbq_user", password="secret")
        response = self.client.get(
            "/events/invite/{}".format(self.event.slug), {"slug": self.event.slug}
        )

        self.assertEqual(response.status_code, 200)

    def test_existing_registration(self):
        self.client.login(username="bbq_user", password="secret")
        self.client.cookies["registered"] = self.event.slug
        response = self.client.get(
            "/events/invite/{}".format(self.event.slug), {"slug": self.event.slug}
        )

        self.assertContains(
            response, "Your are already registered for this event.", status_code=200
        )

    def test_non_existing(self):
        slug = "bad_slug"
        self.client.login(username="bbq_user", password="secret")
        response = self.client.get("/events/invite/{}".format(slug), {"slug": slug})

        self.assertContains(
            response, "The event specified does not exist", status_code=200
        )


class TestRegisterEventView(TestCase):
    def setUp(self):
        self.password = "secret"
        self.user = User.objects.create_user(
            username="bbq_user", password=self.password
        )
        self.now = dt.now().strftime("%Y-%m-%d")
        self.event = Event(date=self.now, author=self.user).save()
        self.meat_1 = MeatType(name="Bacon")
        self.meat_1.save()

    def test_url_resolves_to_view(self):
        found = resolve("/events/invite/register/{}".format(self.event.slug))
        self.assertEqual(found.func, bbq_views.register_event)

    def test_not_logged_in(self):
        response = self.client.post(
            "/events/invite/register/{}".format(self.event.slug)
        )
        self.assertEqual(response.status_code, 302)

    def test_register_valid_data(self):
        body = {"meats": [self.meat_1.pk], "extras": "0", "name": "test"}

        self.client.login(username="bbq_user", password="secret")
        response = self.client.post(
            "/events/invite/register/{}".format(self.event.slug),
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies.get("registered").value, self.event.slug)

    def test_register_invalid_meat_id(self):
        body = {"meats": ["1000"], "extras": "0", "name": "test"}

        self.client.login(username="bbq_user", password="secret")
        response = self.client.post(
            "/events/invite/register/{}".format(self.event.slug),
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")

    def test_register_invalid_number_meat_id(self):
        body = {"meats": ["abc"], "extras": "0", "name": "test"}

        self.client.login(username="bbq_user", password="secret")
        response = self.client.post(
            "/events/invite/register/{}".format(self.event.slug),
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")

    def test_register_invalid_event(self):
        body = {"meats": ["abc"], "extras": "0", "name": "test"}
        slug = "bad_slug"

        self.client.login(username="bbq_user", password="secret")
        response = self.client.post(
            "/events/invite/register/{}".format(slug),
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_register_non_numeric_extras(self):
        body = {"meats": [], "extras": "abc", "name": "test"}

        self.client.login(username="bbq_user", password="secret")
        response = self.client.post(
            "/events/invite/register/{}".format(self.event.slug),
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_already_registered(self):
        body = {"meats": [], "extras": "0", "name": "test"}

        self.client.cookies["registered"] = self.event.slug
        self.client.login(username="bbq_user", password="secret")
        response = self.client.post(
            "/events/invite/register/{}".format(self.event.slug),
            data=json.dumps(body),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_using_get(self):
        self.client.login(username="bbq_user", password="secret")
        response = self.client.get("/events/invite/register/{}".format(self.event.slug))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your are already registered for this event.")


class TestEventsListView(TestCase):
    def setUp(self):
        self.password = "secret"
        self.user = User.objects.create_user(
            username="bbq_user", password=self.password
        )
        self.now = dt.now().strftime("%Y-%m-%d")
        self.event_1 = Event(date=self.now, author=self.user)
        self.event_1.save()

        self.event_2 = Event(date=self.now, author=self.user)
        self.event_2.save()

    def test_url_resolves_to_view(self):
        found = resolve("/events/list/")
        self.assertEqual(found.func, bbq_views.events_list)

    def test_all_events_shown(self):
        self.client.login(username="bbq_user", password="secret")
        response = self.client.get("/events/list/")

        request_event_set = {self.event_1, self.event_2}
        response_event_set = {event for event in response.context["events"]}
        self.assertEqual(request_event_set, response_event_set)


class TestSignupView(TestCase):
    def test_url_resolves_to_view(self):
        found = resolve("/signup/")
        self.assertEqual(found.func, bbq_views.signup)

    def test_get(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)

    def test_valid_signup(self):
        password = "ABCabc123!@#"
        username = "bbq_user"

        body = {
            "username": username,
            "password1": password,
            "password2": password
        }

        response = self.client.post("/signup/", data=body)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/")

    def test_invalid_signup(self):
        username = "bbq_user"

        body = {
            "username": username,
            "password1": "bad_pass_1",
            "password2": "bad_pass_2"
        }

        response = self.client.post("/signup/", data=body)
        self.assertEqual(response.status_code, 200)


class TestDeleteEventView(TestCase):
    def setUp(self):
        self.password = "secret"
        self.user = User.objects.create_user(
            username="bbq_user", password=self.password
        )
        self.now = dt.now().strftime("%Y-%m-%d")
        self.event = Event(date=self.now, author=self.user)
        self.event.save()

    def test_url_resolves_to_view(self):
        found = resolve("/events/delete/")
        self.assertEqual(found.func, bbq_views.delete_event)

    def test_delete_existing_event(self):
        body = {"slug": self.event.slug}

        query_event = Event.objects.filter(slug=self.event.slug)
        self.assertEqual(len(query_event), 1)

        self.client.login(username="bbq_user", password="secret")
        response = self.client.post(
            "/events/delete/",
            data=json.dumps(body),
            content_type="application/json",
        )

        query_event = Event.objects.filter(slug=self.event.slug)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(query_event), 0)

    def test_delete_non_logged_in(self):
        body = {"slug": self.event.slug}

        response = self.client.post(
            "/events/delete/",
            data=json.dumps(body),
            content_type="application/json",
        )

        url = response.url.split("?")[0]
        self.assertEqual(response.status_code, 302)
        self.assertEqual(url, "/accounts/login/")

    def test_delete_non_existing(self):
        body = {"slug": "does_not_exist"}

        self.client.login(username="bbq_user", password="secret")
        response = self.client.post(
            "/events/delete/",
            data=json.dumps(body),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/error/")


class Test404View(TestCase):
    def test_non_existing_url(self):
        response = self.client.get("/this/url/does/not/exist")
        self.assertEqual(response.status_code, 302)
