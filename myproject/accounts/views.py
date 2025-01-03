from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import StudentRegisterForm, TeacherRegistrationForm, AdminRegisterForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
from django.shortcuts import get_object_or_404
from .models import TeacherRequest, CustomUser, ClassSchedule, Review
from .forms import TeacherRequestForm, ProposeTimeForm, ReviewForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Avg
from .models import Subject, Question, Answer
from .forms import QuestionForm, AnswerForm
from .forms import PaperUploadForm
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

# Ensure only admins can approve teachers
def is_admin(user):
    return user.is_superuser

# Home Page View
def home(request):
    return render(request, 'home.html')

def about_us(request):
    return render(request, 'about_us.html')

def terms_view(request):
    return render(request, 'terms.html')

def how_it_works(request):
    return render(request, 'how_it_works.html')

def how_it_works1(request):
    return render(request, 'how_it_works1.html')




@login_required
def approve_teacher(request, teacher_id):
    # Only allow admins to approve teachers
    if request.user.user_type != 'admin':
        return redirect('login')
    
    teacher = get_object_or_404(CustomUser, id=teacher_id, user_type='teacher')
    teacher.is_active = True
    teacher.save()
    return redirect('admin_dashboard')


def student_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken. Please choose a different one.')
            else:
                student = form.save(commit=False)
                student.user_type = 'student'
                student.save()
                login(request, student, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('student_dashboard')
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts/student_register.html', {'form': form})

@transaction.atomic
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.user_type = 'teacher'
                    user.is_active = False
                    user.set_password(form.cleaned_data['password'])
                    
                    # Handle file uploads
                    if 'nic_photo' in request.FILES:
                        user.nic_photo = request.FILES['nic_photo']
                    if 'alevel_result_sheet' in request.FILES:
                        user.alevel_result_sheet = request.FILES['alevel_result_sheet']
                    
                    user.save()
                    form.save_m2m()
                messages.success(request, 'Your account has been created! Wait for admin approval.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'accounts/teacher_register.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)  # Ensure only admins can delete
def admin_register(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            admin_user = form.save(commit=False)
            admin_user.user_type = 'admin'
            admin_user.save()
            login(request, admin_user, backend = 'django.contrib.auth.backends.ModelBackend')
            return redirect('admin_dashboard')
    else:
        form = AdminRegisterForm()
    return render(request, 'accounts/admin_register.html', {'form': form})




# User login view
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user, backend =  'accounts.backends.EmailBackend')
            # Redirect to the respective dashboard based on user role
            if user.user_type == 'student':
                return redirect('student_dashboard')
            elif user.user_type == 'teacher':
                return redirect('teacher_dashboard')
            elif user.user_type == 'admin':
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')


# User logout view
def user_logout(request):
    logout(request)
    return redirect('login')




@login_required
def student_dashboard(request):
    student = request.user
    if student.user_type != 'student':
        return render(request, 'error.html', {'message': 'Unauthorized access'})  

    # Get the list of teachers assigned to the logged-in student (via accepted requests)
    student_requests = TeacherRequest.objects.filter(student=student, status='accepted')
    teachers = [request.teacher for request in student_requests]
    class_schedules = ClassSchedule.objects.filter(student=student)

    if request.method == 'POST':
        form = ProposeTimeForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.student = student
            teacher_id = request.POST.get('teacher')
            if teacher_id:
                schedule.teacher = CustomUser.objects.get(id=teacher_id)
            schedule.save()
            return redirect('student_dashboard')
    else:
        form = ProposeTimeForm()

    return render(request, 'accounts/student_dashboard.html', {
        'teachers': teachers,
        'student': student,
        'class_schedules': class_schedules,
        'form': form,
    })


@login_required
def submit_review(request, teacher_id):
    teacher = get_object_or_404(CustomUser, id=teacher_id, user_type='teacher')
    student = request.user
    
    if student.user_type != 'student':
        return render(request, 'error.html', {'message': 'Unauthorized access'})  

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.student = student
            review.teacher = teacher
            review.save()
            return redirect('student_dashboard')
    else:
        form = ReviewForm()

    return render(request, 'accounts/submit_review.html', {
        'form': form,
        'teacher': teacher,
    })


@login_required
def teacher_dashboard(request):
    # Ensure we're fetching the correct logged-in teacher's details
    teacher = request.user  # Logged-in teacher

    if teacher.user_type != 'teacher':
        return render(request, 'error.html', {'message': 'Unauthorized access'})  # Ensure only teachers can access this dashboard

    # Get the list of students assigned to the logged-in teacher (via accepted requests)
    teacher_requests = TeacherRequest.objects.filter(teacher=teacher, status='accepted')
    students = [request.student for request in teacher_requests]  # Get a list of students who have been accepted

    class_schedules = ClassSchedule.objects.filter(teacher=teacher)

    if request.method == 'POST':
        form = ProposeTimeForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.teacher = teacher
            student_id = request.POST.get('student')  # Get the student from the form
            if student_id:
                schedule.student = CustomUser.objects.get(id=student_id)  # Assign the student
            schedule.save()
            return redirect('teacher_dashboard')
    else:
        form = ProposeTimeForm()

    return render(request, 'accounts/teacher_dashboard.html', {
        'students': students,  # Pass the students list to the template
        'teacher': teacher,  # Pass the teacher object to display correct username
        'class_schedules': class_schedules,  # Pass class schedules
        'form' : form,
    })

# Admin dashboard view
@login_required
def admin_dashboard(request):

    if request.user.user_type != 'admin':
        return redirect('login')
    # For admin, we can also show pending teacher approvals
    pending_teachers = CustomUser.objects.filter(user_type='teacher', is_active=False)
    context = {'pending_teachers': pending_teachers}
    return render(request, 'accounts/admin_dashboard.html', context)


# views.py
@login_required
def search_teachers(request):
            # Initialize a query for active teachers
    teachers = CustomUser.objects.filter(user_type='teacher', is_active=True)

    if request.method == 'GET':
        district = request.GET.get('district')
        medium = request.GET.get('medium')
        subject = request.GET.getlist('subject')  # Get a list of selected subjects
        

                # Log the filter values
        logger.debug(f"District: {district}, Medium: {medium}, Subjects: {subject}")

        
        # Apply filters only if the fields are provided in the request
        if district or medium or subject:
            if district:
                teachers = teachers.filter(district=district)
            if medium:
                teachers = teachers.filter(medium=medium)
            if subject:
                teachers = teachers.filter(subject__in=subject)
        
        teachers = teachers.annotate(avg_rating=Avg('reviews__rating'))

        # Get all subjects for the subject dropdown in the template
        subjects = Subject.objects.all()

        context = {
            'teachers': teachers,
            'subjects': subjects,  # Pass subjects for the dropdown
        }
        return render(request, 'accounts/search_teachers.html', context)

@login_required
def request_teacher(request, teacher_id):
    teacher = get_object_or_404(CustomUser, id=teacher_id, user_type='teacher')

    # Check if the request already exists
    existing_request = TeacherRequest.objects.filter(student=request.user, teacher=teacher).exists()
    if existing_request:
        messages.error(request, 'You have already requested this teacher.')
    else:
        # Create a new request
        TeacherRequest.objects.create(student=request.user, teacher=teacher, status='pending')
        messages.success(request, 'Your request has been sent to the admin.')

    return redirect('student_dashboard')



@login_required
def admin_teacher_requests(request):
    pending_requests = TeacherRequest.objects.filter(status='pending')
    print(pending_requests) 
    return render(request, 'accounts/admin_teacher_requests.html', {'pending_requests': pending_requests})

@login_required
def approve_teacher_request(request, request_id):
    teacher_request = get_object_or_404(TeacherRequest, id=request_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            teacher_request.status = 'accepted'
            teacher_request.save()
            messages.success(request, 'The request has been accepted.')
        elif action == 'decline':
            teacher_request.status = 'declined'
            teacher_request.save()
            messages.success(request, 'The request has been declined.')

    return redirect('admin_teacher_requests')



@login_required
def admin_teacher_overview(request):
    if request.user.user_type != 'admin':
        return render(request, 'error.html', {'message': 'Unauthorized access'})

    # Fetch all accepted teachers and prefetch related class schedules and requests
    teachers = CustomUser.objects.filter(user_type='teacher', is_active=True).prefetch_related('teacher_classes', 'teacher_requests').annotate(avg_rating=Avg('reviews__rating'))

    return render(request, 'accounts/admin_teacher_overview.html', {
        'teachers': teachers,
    })




@login_required
def confirm_time(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)

    if schedule.is_student(request.user) or schedule.is_teacher(request.user):
        schedule.confirmed_time = schedule.proposed_time_teacher or schedule.proposed_time_student
        schedule.status = 'confirmed'
        schedule.save()
        return redirect(reverse('student_dashboard') if schedule.is_student(request.user) else reverse('teacher_dashboard'))

    return render(request, 'error.html', {'message': 'Unauthorized access'})


@login_required
def decline_time(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)

    if schedule.is_student(request.user) or schedule.is_teacher(request.user):
        schedule.status = 'declined'
        schedule.save()
        return redirect(reverse('student_dashboard') if schedule.is_student(request.user) else reverse('teacher_dashboard'))

    return render(request, 'error.html', {'message': 'Unauthorized access'})




def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(CustomUser, id=teacher_id, role='teacher')
    teacher.delete()
    return redirect(reverse('teachers_overview'))  # Redirect to the teachers overview page








@login_required
def forum_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'accounts/forum_subjects.html', {'subjects': subjects})

@login_required
def forum_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.subject = subject
            # Remove this block to prevent double saving
            # if 'image' in request.FILES:
            #     question.image = request.FILES['image']
            question.save()
            return redirect('forum_by_subject', subject_id=subject.id)
    else:
        form = QuestionForm()
    return render(request, 'accounts/forum_by_subject.html', {
        'subject': subject,
        'questions': questions,
        'form': form,
    })

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question)

    if request.method == 'POST':
        # Check if the question already has 5 or more answers
        if answers.count() >= 5:
            messages.error(request, "This question already has the maximum number of answers (5).")
            return redirect('question_detail', question_id=question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            # Remove this block to prevent double saving
            # if 'image' in request.FILES:
            #     answer.image = request.FILES['image']
            answer.save()
            messages.success(request, "Your answer has been added successfully.")
            return redirect('question_detail', question_id=question.id)
    else:
        form = AnswerForm()

    return render(request, 'accounts/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })




@login_required
def upload_paper(request):
    if request.method == 'POST':
        form = PaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create paper upload instance but don't save yet
                paper_upload = form.save(commit=False)
                # Set the student to current user
                paper_upload.student = request.user
                
                # Save the form to store the files in Cloudinary and create the database record
                paper_upload.save()
                
                messages.success(request, 'Paper uploaded successfully!')
                return redirect('student_dashboard')
            
            except Exception as e:
                logger.error(f"Error uploading paper: {str(e)}")
                messages.error(request, 'An error occurred while uploading the paper. Please try again.')
        else:
            # Log form errors for debugging
            logger.error(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PaperUploadForm()

    return render(request, 'upload_paper.html', {
        'form': form,
        'title': 'Upload Paper'
    })