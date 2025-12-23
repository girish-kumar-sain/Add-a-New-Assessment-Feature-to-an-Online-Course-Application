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


def show_exam_result(request, course_id):
    submissions = Submission.objects.filter(user=request.user)
    total_score = 0
    score = 0

    for submission in submissions:
        total_score += submission.question.grade
        if submission.choice.is_correct:
            score += submission.question.grade

    context = {
        'score': score,
        'total': total_score,
        'passed': score >= total_score * 0.5
    }
    return render(request, 'onlinecourse/exam_result.html', context)
