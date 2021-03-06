from django.db import models

# Create your models here.

class Tour(models.Model):
    tour_name = models.CharField(max_length = 512)
    artist_name = models.CharField(max_length = 32)
    #start_date = models.DateTimeField()
    #end_date = models.DateTimeField()
    def __str__(self):
        return ("%s %s" % (self.artist_name, self.tour_name))
    
class Live(models.Model):
    tour = models.ForeignKey(Tour, on_delete = models.CASCADE)
    live_name = models.CharField(max_length = 512)
    def __str__(self):
        return self.live_name

class Ticket(models.Model):
    # an auto-increament field `id' is automatically added by django
    live = models.ForeignKey(Live, on_delete = models.CASCADE)
    registered_by = models.CharField(max_length = 512)
    owner = models.CharField(max_length = 512, null = True)
    owned_by_self = models.BooleanField(default = True)
    user = models.CharField(max_length = 512, null = True)
    used_by_self = models.BooleanField(default = True)
    state = models.IntegerField(default = 0)
    def __str__(self):
       return self.live
