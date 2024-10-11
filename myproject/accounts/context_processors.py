# context_processors.py
from .models import Subject

def subjects_processor(request):
    subjects = Subject.objects.all()
    return {'subjects': subjects}
