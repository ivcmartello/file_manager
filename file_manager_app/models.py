"""File manager models"""
from django.db import models
from .exceptions import ItemStructureAlredyExists


class Structure(models.Model):
    """Structure model"""

    name = models.CharField(max_length=50)
    parent_id = models.IntegerField(default=0)
    file_path = models.CharField(max_length=255, null=True, blank=True)

    def is_file(self):
        """Return is a file"""
        return self.file_path is not None

    def mtype(self):
        """Return type"""
        if self.is_file():
            return "File"
        return "Folder"

    def save(self, *args, **kwargs) -> None:

        if Structure.objects.filter(parent_id=self.parent_id, name=self.name):
            raise ItemStructureAlredyExists()

        return super().save(*args, **kwargs)
