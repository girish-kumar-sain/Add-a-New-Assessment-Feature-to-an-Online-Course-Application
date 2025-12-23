from django.shortcuts import render, redirect
from .models import Question, Choice, Submission

def submit(request, course_id):
    if request.method == 'POST':
        user = request.user
        Submission.objects.filter(user=user).delete()

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                choice_id = int(value)
                Submission.objects.create(
                    user=user,
                    question_id=question_id,
                    choice_id=choice_id
                )

        return redirect('show_exam_result', course_id=course_id)
