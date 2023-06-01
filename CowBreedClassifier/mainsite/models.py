from django.db import models

class Breed(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='picture')
    description = models.TextField()
    key_information = models.TextField()
    
    def __str__(self):
        return self.name

class Uploads(models.Model):
  photo = models.ImageField()

  def __str__(self):
    return str(self.photo)