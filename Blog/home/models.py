from django.db import models
import  uuid 
from django.contrib.auth.models import User


class BaseModel(models.Model):
    # generates a unique id
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # stores the time of creation of object
    created_at = models.DateField(auto_now_add=True)
    # last updated time for the application
    updated_at = models.DateField(auto_now_add=True)

    # enabling the class to be abstract class
    class Meta:
        abstract = True


class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "blogs")
    title = models.CharField(max_length=500)
    blog_text = models.TextField()
    main_image = models.ImageField(upload_to="blogs")

    def __str__(self):
        return self.title

