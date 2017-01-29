import itertools

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from .models import Tour, Live, Ticket

# Create your views here.
@login_required(login_url='/login/')
def index(req, **kwargs):
    template = loader.get_template("main/index.html")
    context = {
        "tickets": Ticket.objects.filter(owner = req.user.username),
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
            in_str = req.POST["live"]
            # crazily bad assumption: in_str is in a form of "arist_tour_live"
            # (imagine what happens if say the artist name includes a '_')
            artist_name, tour_name, live_name = in_str.split("_")
        elif req.POST["select_live"] == "add_new":
            artist_name = req.POST["artist_name"]
            tour_name = req.POST["tour_name"]
            live_name = req.POST["live_name"]
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
        ticket = Ticket(owner = req.user.username, live = live)
        ticket.save()

    return HttpResponse("ok")
