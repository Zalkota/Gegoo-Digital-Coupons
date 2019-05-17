from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView, DeleteView, UpdateView
from django.views import generic

#messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

#Email
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template

from memberships.models import UserMembership, Transaction
from .models import Course, Lesson, Review

#Login
from django.contrib.auth.decorators import login_required  # This is to block pages to non users using function views
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ContactForm, AppointmentForm
from users.models import User, Profile
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.utils import timezone

#SuperUser Mixin
from braces import views
from django.conf import settings

#appointmentform
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

def AppointmentFormView(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AppointmentForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/appointment-confirmation/')

        # If this is a GET (or any other method) create the default form.
    else:
        form = AppointmentForm()

    day_plus_one = datetime.date.today() + datetime.timedelta(days=1)
    day_plus_two = datetime.date.today() + datetime.timedelta(days=2)
    day_plus_three = datetime.date.today() + datetime.timedelta(days=3)
    day_plus_four = datetime.date.today() + datetime.timedelta(days=4)

    return render(request, 'portal/appointment_form.html', {'form': form, 'day_plus_one': day_plus_one, 'day_plus_two': day_plus_two, 'day_plus_three': day_plus_three, 'day_plus_four': day_plus_four })


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


def SubscriptionListView(request):

    existing_order = get_user_pending_order(request)
    filtered_orders = Order.objects.filter(owner=request.user.user_profile, is_ordered=False)

    context = {
        'order': existing_order,
    }

    args = {}
    args.update(csrf(request))

    return render(request, "portal/subscription_list.html", context, args)



def get_course(course):
    course_qs = Course.objects.filter(id=course)
    if course_qs.exists():
        return course_qs.first()
    return None

@login_required
def Review(request, course):
    form_class = ReviewForm
    review_user = request.user
    if request.method == "GET":
        form_class = ReviewForm(initial={'review_course': course, 'review_user': review_user})

    # new logic!
    if request.method == 'POST':
        #form_class = ContactForm(initial={'contact_email': email, 'contact_name': user})
        form = ReviewForm(request.POST)

        if form.is_valid():

            review_course = request.POST.get(
                'review_course'
            , '')

            review_summary = request.POST.get('summary', '')

            rating = request.POST.get(
                'rating'
            , '')


            course_instance = get_course(course)

            review = form.save(commit=False)
            review.review_user = review_user
            review.review_course = course_instance
            review.summary = review_summary
            review.rating = rating
            review.created_time = timezone.now()
            review.save()
            print ("saved")
            messages.success(request, "Thank you for your review!")
            return redirect('portal:course_detail', slug=course_instance.slug)
            #return redirect('portal:course_list')

    else:
            form = ReviewForm()

    return render(request, 'portal/review_form_create.html', {
        'form': form_class,
    })

@login_required
def Contact(request, email, user):
    form_class = ContactForm
    if request.method == "GET":
        form_class = ContactForm(initial={'contact_email': email, 'contact_name': user})

    # new logic!
    if request.method == 'POST':
        #form_class = ContactForm(initial={'contact_email': email, 'contact_name': user})
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('portal/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            messages.success(request, "Email sent successfully")
            return redirect('memberships:admin_panel')


    return render(request, 'portal/contact_form.html', {
        'form': form_class,
    })



#class CourseListView(ListView):
#	model = Course


def CourseListView(request):
    count = Course.objects.all().count()
    free_list = Course.objects.filter(membership_required=False).order_by('ordering_id')
    paid_list = Course.objects.filter(membership_required=True).order_by('ordering_id')

    context = {
        'count': count,
        'free_list': free_list,
        'paid_list': paid_list,
    }

    args = {}
    args.update(csrf(request))

    return render(request, "portal/course_list.html", context, args)


def SearchTitles(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    course = Course.objects.filter(tags__contains=search_text)

    return render(request,'portal/search.html', {'course' : course })



class CourseDetailView(DetailView):
	model = Course

@login_required
def LessonDetailView(request, course_slug, lesson_slug, *args, **kwargs):

    #def get_context_data(self, **kwargs):
    #    context = super(LessonDetailView, self).get_context_data(**kwargs)
    #    context['lesson_list'] = Lesson.objects.filter('')
    #    return context

    user = request.user
    course_qs = Course.objects.filter(slug=course_slug)
    if course_qs.exists():
        course = course_qs.first()
    course_id = course.ordering_id
    #Used to pull lesson in sidenav
    lesson_list = Lesson.objects.filter(course=course_id)

    lesson_qs = course.lessons.filter(slug=lesson_slug)
    if lesson_qs.exists():
        lesson = lesson_qs.first()

    #Checks if the course needs a membership to view it
    if course.membership_required == True:

        #Request the users membership
        user_membership = UserMembership.objects.filter(user=user).first()

        if user_membership.membership != None:

            user_membership_type = user_membership.membership.membership_type
            #Query the allowed memberships from course
            course_allowed_mem_types = course.allowed_memberships.all()

            context = {
            'object': None
            }

            if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
                context = {'object': lesson}

        else:
            return render(request, "portal/membership_required.html")

    #Enrollment feature
    user_enrolled = user.user_profile.enrolled.filter(slug=course_slug).first()
    if user_enrolled == None:
        enrolled = course
        enrolled.save()
        user.user_profile.enrolled.add(course)

    context = {
    'object': lesson,
    'lesson_list': lesson_list
    }

    return render(request, "portal/lesson_detail.html", context)

def membership_required(request):
    return render(request, 'portal/membership_required.html')


def next_lesson(request, course_slug, lesson_slug):
    lesson_add = int(lesson_slug) + 1
    course_id = Course.objects.filter(slug=course_slug)
    try:
        lesson_qs = Lesson.objects.get(course=course_id[0], ordering_id=lesson_add)
        lesson_slug = lesson_qs.slug
        return redirect('portal:lesson_detail', course_slug, lesson_slug)

    except ObjectDoesNotExist:
        lesson_qs = Lesson.objects.get(course=course_id[0], ordering_id=lesson_slug)
        lesson_slug = lesson_qs.slug
        return redirect('portal:lesson_detail', course_slug, lesson_slug)

def previous_lesson(request, course_slug, lesson_slug):
    lesson_add = int(lesson_slug) - 1
    course_id = Course.objects.filter(slug=course_slug)
    try:
        lesson_qs = Lesson.objects.get(course=course_id[0], ordering_id=lesson_add)
        lesson_slug = lesson_qs.slug
        return redirect('portal:lesson_detail', course_slug, lesson_slug)

    except ObjectDoesNotExist:
        lesson_qs = Lesson.objects.get(course=course_id[0], ordering_id=lesson_slug)
        lesson_slug = lesson_qs.slug
        return redirect('portal:lesson_detail', course_slug, lesson_slug)

class LessonCreateView(SuccessMessageMixin, views.SuperuserRequiredMixin, CreateView):
    model = Lesson
    fields = '__all__'
    template_name = 'portal/lesson_form_create.html'
    success_message = "Lesson Created"
    success_url = reverse_lazy('memberships:lesson_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True

class LessonUpdateView(SuccessMessageMixin, views.SuperuserRequiredMixin, UpdateView):
    model = Lesson
    fields = '__all__'
    success_message = "Lesson Edited Successfully"
    success_url = reverse_lazy('memberships:lesson_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True

class LessonDeleteView(SuccessMessageMixin, views.SuperuserRequiredMixin, DeleteView):
    model = Lesson
    warning_message = "Lesson Deleted"
    success_url = reverse_lazy('memberships:lesson_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True


class CourseCreateView(SuccessMessageMixin, views.SuperuserRequiredMixin, CreateView):
    model = Course
    fields = '__all__'
    template_name = 'portal/course_form_create.html'
    success_message = "Course Created"
    success_url = reverse_lazy('memberships:course_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True


class CourseUpdateView(SuccessMessageMixin, views.SuperuserRequiredMixin, UpdateView):
    model = Course
    fields = '__all__'
    success_message = "Course Edited Successfully"
    success_url = reverse_lazy('memberships:course_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True

class CourseDeleteView(SuccessMessageMixin, views.SuperuserRequiredMixin, DeleteView):
    model = Course
    warning_message = "Course Deleted"
    success_url = reverse_lazy('memberships:course_panel')

    #Superuser Mixin
    login_url = settings.LOGIN_URL
    raise_exception = False
    redirect_field_name = '/'
    redirect_unauthenticated_users = True
