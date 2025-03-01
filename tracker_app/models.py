from django.db import models

# Create your models here.

class UserDomainsHistory(models.Model):
    user_id = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)

    created_at = models.BigIntegerField(default=0)
    updated_at = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'user_domains_history'
        indexes = [
            models.Index(fields=['user_id', 'created_at',]),
            models.Index(fields=['user_id', 'domain','created_at',]),
        ]
        unique_together = ('user_id', 'domain', 'created_at',)

    def __str__(self):
        return f'{self.user_id}:{self.domain}'


