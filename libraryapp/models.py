from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Book(models.Model):
    title = models.CharField(max_length=200)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveBigIntegerField()

    def __str__(self):
        return self.title

class BorrowingRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    due_date = models.DateTimeField(default=datetime.now()+timedelta(days=30))
    renewed = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    