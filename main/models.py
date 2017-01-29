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
    owner = models.CharField(max_length = 512, null = True)
    live = models.ForeignKey(Live, on_delete = models.CASCADE)
    number = models.IntegerField("number of tickets you have", default = 0)
    def __str__(self):
       return ("%s:%d" % (self.live, self.number))
