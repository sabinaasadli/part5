from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

# Ana səhifə – sual siyahısı
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

# Sualın detalları (variantların siyahısı)
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

# Səsvermə (form POST göndərir)
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "Seçim etməmisiniz!"},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Səsvermədən sonra nəticələr səhifəsinə yönləndirir
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# Nəticələr səhifəsi
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
