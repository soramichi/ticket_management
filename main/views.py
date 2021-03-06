import itertools

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from .models import Tour, Live, Ticket

# "{'a', 'b', 'c'}" => "a,b,c"
def process_string_for_js(s):
    if not isinstance(s, str):
        s = s.__str__()
    return s[1:-1].replace("'","")

def delete_heading_spaces(s):
    n_spaces = 0
    for i in range(0, len(s)):
        if s[i] == ' ':
            n_spaces += 1
        else:
            break
    return s[n_spaces:]

# Create your views here.
@login_required(login_url='/login/')
def index(req, **kwargs):
    template = loader.get_template("main/index.html")
    context = {
        "tickets": Ticket.objects.filter(registered_by = req.user.username),
        "username": req.user.username,
    }
    return HttpResponse(template.render(context, req))

def add_ticket(req, **kargs):
    template = loader.get_template("main/add_ticket.html")
    live_list = [[l.tour.artist_name, l.tour.tour_name, l.live_name] for l in Live.objects.all()]
    context = {
        "live_list": live_list
    }
    return HttpResponse(template.render(context, req))

def do_add_ticket(req, **kwargs):
    try:
        number = int(req.POST["number"])
        
        if req.POST["select_live"] == "choose_existing":
            artist_name = delete_heading_spaces(req.POST["artist_selected"])
            tour_name = delete_heading_spaces(req.POST["tour_selected"])
            live_name = delete_heading_spaces(req.POST["live_selected"])
        elif req.POST["select_live"] == "add_new":
            artist_name = req.POST["artist_added"]
            tour_name = req.POST["tour_added"]
            live_name = req.POST["live_added"]
    except ValueError:
        message = "Number of tickets should be an ascii integer"
        return HttpResponse(message)
    except KeyError:
        message = "Invalid argument"
        return HttpResponse(message)

    tour = Tour.objects.filter(tour_name = tour_name, artist_name = artist_name)
    if len(tour) == 0:
        # creat a new tour
        tour = Tour(tour_name = tour_name, artist_name = artist_name)
        tour.save()
    else:
        # use the existing tour, take [0] as filter returns a dict even if len is 1
        tour = tour[0]

    live = Live.objects.filter(tour = tour, live_name = live_name)
    if len(live) == 0:
        # create a new live
        live = Live(tour = tour, live_name = live_name)
        live.save()
    else:
        # use the existing live, take [0] as filter returns a dict even if len is 1
        live = live[0]

    for i in range(0, number):
        # multiple tickets are distinguishable by `.id', which is automatically
        # added by the django framework
        ticket = Ticket(registered_by = req.user.username, live = live)
        ticket.save()

    return HttpResponse("ok")

def edit_user(req, **kwargs):
    template = loader.get_template("main/edit_user.html")
    ticket_id = int(req.POST["ticket_id"])
    ticket = Ticket.objects.filter(id = ticket_id)[0]

    context = {
        "ticket_id": ticket_id,
        "owner": ticket.owner,
        "owned_by_self": ticket.owned_by_self,
        "user": ticket.user,
        "used_by_self": ticket.used_by_self,
        "state": ticket.state,
    }

    return HttpResponse(template.render(context, req))

def do_edit_user(req, **kwargs):
    ticket_id = int(req.POST["ticket_id"])
    used_by_self = bool(int(req.POST["used_by_self"]))
    user = req.POST["user"]
    owned_by_self = bool(int(req.POST["owned_by_self"]))
    owner = req.POST["owner"]
    state = int(req.POST["state"])

    ticket = Ticket.objects.filter(id = ticket_id)[0]

    # the ticket specified is not owned by the requesting user, hacked?
    if ticket.registered_by != req.user.username:
        message = "ticket id is invalid"
        return HttpResponse(message)

    ticket.used_by_self = used_by_self
    ticket.owned_by_self = owned_by_self
    ticket.state = state
    ticket.user = user if used_by_self == False else ""
    ticket.owner = owner if owned_by_self == False else ""
    ticket.save()
    
    return HttpResponse("%d [%s] %d" % (ticket_id, user, state))

def get_artists(req, **kwargs):
    tours = Tour.objects.all()
    artists = set([t.artist_name for t in tours])
    return HttpResponse("%s" % process_string_for_js(artists.__str__()))

def get_tours(req, **kwargs):
    artist_name = delete_heading_spaces(req.POST["artist_selected"])
    tours = Tour.objects.filter(artist_name = artist_name)
    return HttpResponse("%s" % process_string_for_js([t.tour_name for t in tours]))

def get_lives(req, **kwargs):
    tour_name = delete_heading_spaces(req.POST["tour_selected"])
    tour = Tour.objects.filter(tour_name = tour_name)[0] # assume every tours have different names
    lives = Live.objects.filter(tour = tour)
    return HttpResponse("%s" % process_string_for_js([l.live_name for l in lives]))
