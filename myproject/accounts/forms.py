from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import ClassSchedule
from .models import TeacherRequest, Review
from .models import Question, Answer
from .models import PaperUpload
from .models import Subject
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe



class StudentRegisterForm(UserCreationForm):
    agree_to_terms = forms.BooleanField(
    label=mark_safe('I agree to the <a href="/terms/" target="_blank" style="color: blue; text-decoration: underline;">Terms and Conditions</a>'),
    required=True,
    )

 
    class Meta:
        model = CustomUser
        fields = ['full_name','username', 'email', 'age','town', 'district', 'alevel_batch_year','phone_number', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        agree_to_terms = cleaned_data.get('agree_to_terms')

        # Check if terms and conditions are agreed upon
        if not agree_to_terms:
            raise ValidationError('You must agree to the terms and conditions.')
        
        

class TeacherRegistrationForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(
    label=mark_safe('I agree to the <a href="/terms/" target="_blank" style="color: blue; text-decoration: underline;">Terms and Conditions</a>'),
    required=True,
)
    

        # District is chosen from predefined choices
    district = forms.ChoiceField(
        choices=CustomUser.DISTRICT_CHOICES,
        required=True,
    )
    
    # Subject is a multiple choice field (Many-to-Many relationship)
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),  # Assuming Subject is a separate model
        widget=forms.CheckboxSelectMultiple,  # Display as checkboxes
        required=True,
    )


    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'age', 'nic_photo', 'alevel_result_sheet', 'subject', 'town', 'district', 'medium','phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


    def clean_subject(self):
        """Custom validation to ensure only 2 subjects are selected."""
        selected_subjects = self.cleaned_data.get('subject')

        if len(selected_subjects) > 2:
            raise forms.ValidationError("You can select a maximum of 2 subjects.")

        return selected_subjects


    def clean(self):
        cleaned_data = super().clean()
        nic_photo = cleaned_data.get('nic_photo')
        alevel_result_sheet = cleaned_data.get('alevel_result_sheet')
        agree_to_terms = cleaned_data.get('agree_to_terms')

        if not nic_photo:
            self.add_error('nic_photo', 'NIC photo is required.')

        if not alevel_result_sheet:
            self.add_error('alevel_result_sheet', 'A-Level result sheet is required.')

        # Check if terms and conditions are agreed upon
        if not agree_to_terms:
            raise ValidationError('You must agree to the terms and conditions.')

class AdminRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),

        }



class TeacherRequestForm(forms.ModelForm):
    class Meta:
        model = TeacherRequest
        fields = ['teacher']





class ProposeTimeForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['proposed_time_teacher', 'proposed_time_student']
        widgets = {
            'proposed_time_teacher': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Select a time for the teacher',  # Optional placeholder
            }),
            'proposed_time_student': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600',
                'placeholder': 'Select a time for the student',  # Optional placeholder
            }),
        }




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }
        labels = {
            'rating': 'Rate your teacher (1 to 5 stars)',
            'comment': 'Leave a comment (optional)',
        }




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'text', 'image']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'image']







class PaperUploadForm(forms.ModelForm):
    class Meta:
        model = PaperUpload
        fields = ['subject', 'medium', 'type', 'paper', 'marking_scheme']
        labels = {
            'subject': 'Select Subject',
            'medium': 'Select Medium',
            'type':' Select Type',
            'paper': 'Upload Paper (PDF)',
            'marking_scheme': 'Upload Marking Scheme (PDF, optional)'
        }
        widgets = {
            'subject': forms.Select(choices=PaperUpload.SUBJECT_CHOICES),
            'medium': forms.Select(choices=PaperUpload.MEDIUM_CHOICES),
            'type': forms.Select(choices=PaperUpload.TYPE_CHOICES),
        }