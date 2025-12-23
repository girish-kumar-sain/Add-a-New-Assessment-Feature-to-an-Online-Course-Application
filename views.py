from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Question, Choice, Submission
def submit(request, course_id):
    if request.method == 'POST':
        user = request.user
        course = get_object_or_404(Course, pk=course_id)

        Submission.objects.filter(user=user, question__course=course).delete()

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
    course = get_object_or_404(Course, pk=course_id)
    submissions = Submission.objects.filter(
        user=request.user,
        question__course=course
    )

    selected_ids = [s.choice.id for s in submissions]

    grade = 0
    possible = 0

    for question in course.question_set.all():
        possible += question.grade
        for submission in submissions:
            if submission.question == question and submission.choice.is_get_score():
                grade += question.grade

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': grade,
        'possible': possible
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def is_get_score(self):
        return self.is_correct

