from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from django_countries.fields import CountryField

from django.db.models import Min, Max


class Company(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    country = CountryField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Period(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.ForeignKey(to='Status', related_name='status', on_delete=models.CASCADE)
    agreement = models.ForeignKey(to='Agreement', related_name='periods', on_delete=models.CASCADE)

    def clean(self):
        agr_start = self.agreement.start_date
        agr_end = self.agreement.stop_date

        if self.start < agr_start:
            raise ValidationError('Period\'s start date cant be lower then agreement\'s start date')
        if self.end > agr_end:
            raise ValidationError('Period\'s end date cant be lower then agreement\'s stop date')

        if self.pk not in self.agreement.periods.all():
            for period in self.agreement.periods.all():
                if self.start >= period.start or self.end <= period.end:
                    raise ValidationError('You can\'t create this period,'
                                          ' because inside agreement periods should not intersect.')


class Status(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'new'),
        ('ACTIVE', 'active'),
        ('RECONCILIATION', 'reconciliation'),
        ('CLOSED', 'close'),
    )

    title = models.CharField(max_length=15, choices=STATUS_CHOICES, default='NEW')

    def __str__(self):
        return self.title


class Agreement(models.Model):
    start_date = models.DateTimeField()
    stop_date = models.DateTimeField()
    # period = models.ManyToManyField(to='Period', related_name='periods')
    company = models.ForeignKey(to='Company', related_name='company', on_delete=models.CASCADE)
    negotiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    debit = models.IntegerField()
    credit = models.IntegerField()
