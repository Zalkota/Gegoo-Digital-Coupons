from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Question, Topic

class QuestionListView(ListView):
    model = Question
    template_name = 'blog/question_list.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'blog/topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.all().filter(topic__slug=self.kwargs['slug'])
        context['topics'] = Topic.objects.all()
        return context


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'blog/question_detail.html'

# class QuestionCreateView(CreateView):
#     model = Question
#     fields = [
#         'title',
#         'body',
#     ]
#     template_name = 'blog/question_create.html'

    # def form_valid(self, form):
    #     return super().form_valid(form)

# class QuestionUpdateView(UpdateView):
#     model = Question
#     fields = [
#         'title',
#         'body',
#     ]
#     template_name = 'blog/question_update.html'

# class QuestionDeleteView(DeleteView):
#     model = Question
#     template_name = 'blog/question_delete.html'
#     success_url = reverse_lazy('question_list')