import re
import csv
from collections import namedtuple
from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import post_save
from django.dispatch import receiver


class Record(models.Model):
    series = models.CharField(max_length=3) 
    number = models.CharField(max_length=8)
    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("series", "number", )


class FileUpload(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    media = models.FileField()


@receiver(post_save, sender=FileUpload)
def parse_csv(sender, instance, created, **kwargs):
    if created:
        with open(instance.media.path, "r") as file:
            reader = csv.reader(file)
            FileRecord = namedtuple("FileRecord", "series number")
            items = [FileRecord(*x) for x in reader]
            range_regex = re.compile("^[0-9]{6}\-[0-9]{6}$")
            for item in items:
                item.series.strip(" ")
                item.number.strip(" ")
                try:
                    if range_regex.findall(item.number):
                        start, end = item.number.split("-")
                        for number in range(int(start), int(end) + 1):
                            zeros = (6 - len(str(number))) * "0"
                            Record.objects.get_or_create(
                                series=item.series,
                                number=zeros + str(number)
                            )
                    else:
                        Record.objects.get_or_create(
                            series=item.series,
                            number=item.number
                        )
                except MultipleObjectsReturned:
                    continue
            file.close()
