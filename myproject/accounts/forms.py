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
from cloudinary.forms import CloudinaryFileField



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
    
    # Subject is a multiple select dropdown field (Many-to-Many relationship)
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'subject-select', 'size': 4, 'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'age', 'nic_photo', 'alevel_result_sheet', 'subject', 'town', 'district', 'medium','phone_number','description', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_subject(self):
        """Custom validation to ensure only 2 subjects are selected."""
        selected_subjects = self.cleaned_data.get('subject')

        # Ensure 'subject' field was submitted properly
        if not selected_subjects:
            raise forms.ValidationError("Please select at least one subject.")

        # Ensure no more than 2 subjects are selected
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
    image = CloudinaryFileField(
        options={
            'folder': 'questions',
            'allow_empty': True,
        },
        required=False
    )

    class Meta:
        model = Question
        fields = ['subject', 'text', 'image']

class AnswerForm(forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'folder': 'answers',
            'allow_empty': True,
        },
        required=False
    )

    class Meta:
        model = Answer
        fields = ['text', 'image']

    def clean(self):
        cleaned_data = super().clean()
        
        # Only check for existing answers if we have a question
        if hasattr(self.instance, 'question') and self.instance.question:
            question = self.instance.question
            if Answer.objects.filter(question=question).count() >= 5:
                raise forms.ValidationError("This question already has the maximum number of answers (5).")

        return cleaned_data









class PaperUploadForm(forms.ModelForm):
    paper = CloudinaryFileField(
        options={
            'resource_type': 'raw',
            'folder': 'papers',
            'allowed_formats': ['pdf'],
        },
        label='Upload Paper (PDF only)'
    )
    
    marking_scheme = CloudinaryFileField(
        options={
            'resource_type': 'raw',
            'folder': 'marking_schemes',
            'allowed_formats': ['pdf'],
        },
        label='Upload Marking Scheme (PDF only)',
        required=False
    )

    class Meta:
        model = PaperUpload
        fields = ['subject', 'medium', 'type', 'paper', 'marking_scheme']
        labels = {
            'subject': 'Select Subject',
            'medium': 'Select Medium',
            'type': 'Select Type'
        }
        widgets = {
            'subject': forms.Select(choices=PaperUpload.SUBJECT_CHOICES),
            'medium': forms.Select(choices=PaperUpload.MEDIUM_CHOICES),
            'type': forms.Select(choices=PaperUpload.TYPE_CHOICES),
        }

    def clean_paper(self):
        paper = self.cleaned_data.get('paper')
        if paper:
            # Check if the file is actually uploaded
            if hasattr(paper, 'content_type') and 'pdf' not in paper.content_type.lower():
                raise forms.ValidationError('Only PDF files are allowed.')
        return paper

    def clean_marking_scheme(self):
        marking_scheme = self.cleaned_data.get('marking_scheme')
        if marking_scheme:
            # Check if the file is actually uploaded
            if hasattr(marking_scheme, 'content_type') and 'pdf' not in marking_scheme.content_type.lower():
                raise forms.ValidationError('Only PDF files are allowed.')
        return marking_scheme