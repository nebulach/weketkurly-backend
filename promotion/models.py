from django.db import models

class Notice(models.Model):
    title           = models.CharField(max_length = 50, null = True, blank = True)
    banner_image    = models.URLField(null = True)
    landing_url     = models.URLField(null = True)

    class Meta:
        db_table = 'notices'


class Event(models.Model) :
    title           = models.CharField(max_length = 100, null = True, blank = True)
    subtitle        = models.CharField(max_length = 100, null = True, blank = True)
    image           = models.URLField(null = True, blank = True)
    landing_url     = models.URLField(null = True, blank = True)
    
    class Meta :
        db_table = 'events'
        
class Recipe(models.Model) :
    title           = models.CharField(max_length = 100, null = True, blank = True)
    image           = models.URLField(null = True, blank = True)
    landing_url     = models.URLField(null = True, blank = True)
    
    class Meta :
        db_table = 'recipes'