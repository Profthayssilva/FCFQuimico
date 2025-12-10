from django.db import models
import uuid

class Document(models.Model):
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='docs/')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DownloadRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    allowed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.company}"
