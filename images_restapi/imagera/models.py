from django.db import models

class accessKey():
    """ Access key for authentication """
    key = models.CharField(unique = True, primary_key = True, max_length = 16)

class imagera(models.Model):
    """ Model for images """
    key = models.CharField(max_length = 16)
    image_id = models.CharField(primary_key = True, max_length = 32)
    image_name = models.CharField(unique = True, max_length = 64)
    image_path = models.CharField(max_length = 256)

    def __str__(self):
        """ Returns image name of the instance """
        return self.image_name
    
    