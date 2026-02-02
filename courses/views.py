from django.shortcuts import render, get_object_or_404
from .models import Course, Submission, Choice


def submit(request, course_id):
    if request.method == 'POST':
        submission = Submission.objects.create(user=request.user)

        selected_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice'):
                choice = Choice.objects.get(id=value)
                submission.choices.add(choice)
                selected_ids.append(choice.id)

        return show_exam_result(request, submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)

    total_score = 0
    possible_score = 0

    for choice in submission.choices.all():
        possible_score += choice.question.grade
        if choice.is_get_score():
            total_score += choice.question.grade

    course = submission.choices.first().question.lesson.course
    selected_ids = [choice.id for choice in submission.choices.all()]

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': total_score,
        'possible': possible_score,
    }

    return render(request, 'courses/exam_result_bootstrap.html', context)
