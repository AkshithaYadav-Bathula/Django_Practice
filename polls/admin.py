from django.contrib import admin
from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    list_display = ["question_text", "pub_date", "was_published_recently"]  # Fields must exist in Question model
    inlines = [ChoiceInline]  # Add choices inline in admin panel
    search_fields = ["question_text"]  # Optional: Add search in Django admin

admin.site.register(Question, QuestionAdmin)
