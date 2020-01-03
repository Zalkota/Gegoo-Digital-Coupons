from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView, FormMixin
from .forms import ContactForm
from blog.models import Question, Topic

class QuestionListView(ListView):
    model = Question
    template_name = 'blog/question_list.html'
    ordering = ['-created_at']
    paginate_by = 4

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

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.all().filter(topic=self.object.topic)
        context['topics'] = Topic.objects.all()
        return context


class ContactFormView(FormView):
    form_class = ContactForm
    success_url = reverse_lazy('contact-landing-page')
    template_name = 'mysite/contact_page.html'


    def form_valid(self, form):
        ContactForm = form.save(commit=False)
        ContactForm.name = form.cleaned_data['name']
        ContactForm.email = form.cleaned_data['email']
        ContactForm.phone = form.cleaned_data['phone']
        ContactForm.description = form.cleaned_data['description']
        ContactForm.save()
        #send_email(ContactForm.name, ContactForm.email, ContactForm.phone, ContactForm.description)

        #template = get_template('contact_template.txt')
        #context = Context({
        #    'contact_name': contact_name,
        #    'contact_email': contact_email,
        #    'form_content': form_content
        #})
        #content = template.render(context)

        #email = EmailMessage(
        #    'New contact form submission',
        #    content,
        #    'Your website ' + '',
        #    ['youremail@gmail.com'],
        #    headers = {'Reply-To': contact_email}
        #
        #email.send()
        return super(ContactFormView, self).form_valid(form)

def contactLandingPage(request):
    return render(request, 'mysite/form_page_landing.html')
