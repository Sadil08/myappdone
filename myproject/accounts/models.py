from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model




def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/teachers/<username>/<filename>
    return f'teachers/{instance.username}/{filename}'

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    age = models.IntegerField(null=True, blank=True)
    alevel_batch_year = models.IntegerField(null=True, blank=True)  # For students
    subject = models.CharField(max_length=100, null=True, blank=True)  # For teachers
    nic_photo = models.ImageField(upload_to=user_directory_path, null=True, blank=True)  # For teachers
    alevel_result_sheet = models.ImageField(upload_to=user_directory_path, null=True, blank=True)  # For teachers

        # Add these fields for teachers
    full_name = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Adjust max_length as needed
    MEDIUM_CHOICES = (
        ('english', 'English Medium'),
        ('sinhala', 'Sinhala Medium'),
        ('tamil', 'Tamil Medium'),
    )
    medium = models.CharField(max_length=20, choices=MEDIUM_CHOICES, null=True, blank=True)  # Teaching Medium


class TeacherRequest(models.Model):
    student = models.ForeignKey(CustomUser, related_name='student_requests', on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, related_name='teacher_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')])
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.student} requested {self.teacher}"
    




class ClassSchedule(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_classes')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_classes')
    proposed_time_teacher = models.DateTimeField(null=True, blank=True)
    proposed_time_student = models.DateTimeField(null=True, blank=True)
    confirmed_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('declined', 'Declined'),
    ], default='pending')
    
    def confirm_schedule(self):
        self.status = 'confirmed'
        self.confirmed_time = self.proposed_time_teacher or self.proposed_time_student
        self.save()

    def is_teacher(self, user):
        return self.teacher == user

    def is_student(self, user):
        return self.student == user

    def __str__(self):
        return f"Class: {self.teacher.username} teaching {self.student.username}"
    


class Review(models.Model):
    teacher = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'})
    student = models.ForeignKey(CustomUser, related_name='student_reviews', on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('teacher', 'student')  # One review per student per teacher

    def __str__(self):
        return f"{self.student} rated {self.teacher} - {self.rating} stars"
    



# Assuming you want to assign the first user (admin) as the default author
def get_default_user():
    return get_user_model().objects.first().id

User = get_user_model()

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=get_default_user)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.author} on {self.subject}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=get_default_user)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='answers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.author} to Question {self.question.id}"



class PaperUpload(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('english', 'English'),
        # Add other subjects
    ]

    MEDIUM_CHOICES = [
        ('english', 'English'),
        ('sinhala', 'Sinhala'),
        ('tamil', 'Tamil'),
    ]

    TYPE_CHOICES = [
        ('school','School Paper'),
        ('model', 'Model Paper'),
        ('al', 'A/L Paper')
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    medium = models.CharField(max_length=100, choices=MEDIUM_CHOICES)
    type =  models.CharField(max_length=50, choices=TYPE_CHOICES, default='model')
    paper = models.FileField(upload_to='papers/', null=True, blank=False)
    marking_scheme = models.FileField(upload_to='marking_schemes/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student}'s {self.subject} paper in {self.medium}  ({self.get_type_display()})"