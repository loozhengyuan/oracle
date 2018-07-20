from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)
    descriptor = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=255)
    descriptor = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Outcome(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    code = models.CharField(max_length=255)
    descriptor = models.CharField(max_length=255)

    def __str__(self):
        return '%s: %s' % (self.code, self.descriptor)


class Course(models.Model):
    code = models.CharField(max_length=255, verbose_name="course code", unique=True)
    title = models.CharField(max_length=65535, verbose_name="course title")
    topic = models.CharField(max_length=65535, verbose_name="course topic", blank=True, null=True)
    type = models.CharField(max_length=65535, verbose_name="course type", blank=True, null=True)
    opening = models.CharField(max_length=65535, verbose_name="open to", blank=True, null=True)
    duration = models.CharField(max_length=65535, verbose_name="duration", blank=True, null=True)
    venue = models.CharField(max_length=65535, verbose_name="venue", blank=True, null=True)
    fee = models.CharField(max_length=65535, verbose_name="course fee", blank=True, null=True)
    grant = models.CharField(max_length=65535, verbose_name="grant info", blank=True, null=True)
    wsa = models.CharField(max_length=65535, verbose_name="who should attend", blank=True, null=True)
    remark = models.CharField(max_length=65535, verbose_name="remark", blank=True, null=True)
    overview = models.CharField(max_length=65535, verbose_name="course overview", blank=True, null=True)
    outline = models.CharField(max_length=65535, verbose_name="course outline", blank=True, null=True)
    testimonial = models.CharField(max_length=65535, verbose_name="testimonial", blank=True, null=True)
    upcoming = models.CharField(max_length=65535, verbose_name="upcoming dates", blank=True, null=True)
    hyperlink = models.CharField(max_length=65535, verbose_name="hyperlink", blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    outcomes = models.ManyToManyField(Outcome, blank=True)

    def __str__(self):
        return '%s: %s' % (self.code, self.title)
