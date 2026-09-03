from django.db import models


class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.CharField(max_length=255)
    agent = models.CharField(max_length=255)
    request = models.TextField()
    data_accessed = models.TextField(blank=True, null=True)
    tool = models.CharField(max_length=255, blank=True, null=True)
    action = models.TextField()
    approval = models.CharField(max_length=255, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.agent} - {self.action}"
