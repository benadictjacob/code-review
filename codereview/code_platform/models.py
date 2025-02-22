from django.db import models

class CodeFile(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    documentation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
