import datetime
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.test import TestCase

from .models import Choice, Question

from django.shortcuts import render

# Custom 404 error handler
def custom_404_view(request, exception):
    """
    Renders a custom 404 page when a requested resource is not found.
    """
    return render(request, "polls/404.html", status=404)

# Custom view for demonstration
def custom_view(request):
    """
    Example of a custom view that renders a sample template.
    Modify this view as per your specific needs.
    """
    return render(request, "polls/custom.html")

class IndexView(generic.ListView):
    """
    Displays the latest 5 published questions on the index page.
    Questions set to be published in the future are excluded.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        # Filters questions that have been published (pub_date <= now)
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    """
    Shows the details of a single question.
    Questions not yet published are excluded.
    """
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        # Exclude questions scheduled for future publishing
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    """
    Displays the results for a specific question.
    """
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    """
    Handles voting for a particular question.
    If no choice is selected, it re-renders the form with an error message.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form with an error message
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # Increments the vote count using F() to prevent race conditions
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Redirects to the results page after voting to prevent duplicate submissions
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
