# models.py
from django.db import models
from datetime import timedelta
class Branch(models.Model):
    brnumb = models.PositiveSmallIntegerField(primary_key=True)
    brname = models.CharField(max_length=25)
    brlocation = models.CharField(max_length=40)

    class Meta:
        db_table = 'BRANCH'
        
    def __str__(self):
        return self.brname

class Employee(models.Model):
    employid = models.CharField(primary_key=True, max_length=5)
    employname = models.CharField(max_length=40, blank=True, null=True)
    deptname = models.CharField(max_length=25, blank=True, null=True)
    brnumb = models.ForeignKey(Branch, models.DO_NOTHING, db_column='BRNUMB')

    class Meta:
        db_table = 'EMPLOYEE'
        
    def __str__(self):
        return f"{self.employname} ({self.employid})"

class Ticket(models.Model):
    ticid = models.CharField(primary_key=True, max_length=7)
    ticname = models.CharField(max_length=100, blank=True, null=True)
    ticcreatedate = models.DateTimeField()
    ticacceptdate = models.DateTimeField(blank=True, null=True)
    ticpriority = models.CharField(max_length=10, blank=True, null=True)
    ticclosetime = models.DateTimeField(blank=True, null=True)
    employid = models.ForeignKey(Employee, models.DO_NOTHING, db_column='EMPLOYID', related_name='tickets_submitted')
    agentid = models.ForeignKey(Employee, models.DO_NOTHING, db_column='AGENTID', related_name='tickets_handled')

    class Meta:
        db_table = 'TICKET'
        
    def __str__(self):
        return f"Ticket #{self.ticid}: {self.ticname}"
    
    @property
    def status(self):
        if not self.ticacceptdate:
            return "open"
        elif not self.ticclosetime:
            return "in-progress"
        else:
            return "resolved"

class Comment(models.Model):
    commentid = models.CharField(primary_key=True, max_length=2)
    ticid = models.ForeignKey(Ticket, models.DO_NOTHING, db_column='TICID')
    employid = models.ForeignKey(Employee, models.DO_NOTHING, db_column='EMPLOYID', blank=True, null=True, related_name='comments_as_employee')
    agentid = models.ForeignKey(Employee, models.DO_NOTHING, db_column='AGENTID', blank=True, null=True, related_name='comments_as_agent')
    comments = models.TextField()

    class Meta:
        db_table = 'COMMENT'
        unique_together = (('commentid', 'ticid'),)
        
    def __str__(self):
        return f"Comment {self.commentid} on Ticket {self.ticid}"

class Ticketmetrics(models.Model):
    ticclosetime = models.DateTimeField(primary_key=True)
    ticid = models.OneToOneField(Ticket, models.DO_NOTHING, db_column='TICID')
    agentid = models.ForeignKey(Employee, models.DO_NOTHING, db_column='AGENTID')
    satisfaction = models.CharField(max_length=1)
    resolutiontime = models.TimeField(blank=True, null=True) 

    class Meta:
        db_table = 'TICKETMETRICS'
        unique_together = (('ticclosetime', 'ticid'),)
        
    def __str__(self):
        return f"Metrics for Ticket {self.ticid}"
