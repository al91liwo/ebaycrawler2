
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import EbayUser, EmailTemplate, AttachmentTemplate
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from pdf2image import convert_from_path
from datetime import time
import json
from django.db.models import Q
from data.cron import acquire_links

class EbayUserListView(ListView):

    model = EbayUser
    paginate_by = 10  # if pagination is desired
    queryset = EbayUser.objects.filter(sent=False, blacklisted=False, cleaned=False)
    ordering = ['-date_acquired']
    template_name = 'ebayuser_list.html'


def dies(request):
    results = acquire_links()
    for res in results:
        try:
            ebay_user = EbayUser(**res)
            ebay_user.save()
        except Exception as e:
            print(res)
            print(e)
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         try:
#             return FileResponse(open(file_path, 'rb'), content_type="application/pdf")
#         except:
#             Http404
#     raise Http404

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    pages = convert_from_path(file_path)
    if os.path.exists(file_path):
        try:
            response = HttpResponse(content_type='image/jpg')
            pages[0].save(response, "JPEG")
            response['Content-Disposition'] = 'attachment; filename="{f_name}.jpg"'.format(f_name=path)
            return response
        except:
            Http404
    raise Http404


def templates(request):
    emails = EmailTemplate.objects.all()
    attachments = AttachmentTemplate.objects.all()
    attachments = [(a.attachment.url.split('/')[-1], a.attachment.name.split('/')[-1]) for a in attachments]
    context = {'emails': emails, 'attachs': attachments}
    return render(request, 'edit_templates.html', context=context)


def delete_user(request, pk):
    user = EbayUser.objects.get(pk=pk)
    user.blacklisted = True
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_pdf_template(request):
    if request.POST:
        file = request.FILES['add_pdf']
        obj = AttachmentTemplate(attachment=file)
        obj.save()
        messages.success(request, 'Successfully added pdf template')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_email_template(request, pk):
    email_template = EmailTemplate.objects.get(pk=pk)
    email_template.text = request.POST['text']
    email_template.subject = request.POST['subject']
    email_template.save()
    messages.success(request, 'Successfully saved email template')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def add_new_email_template(request):
    if request.POST:
        email_template = EmailTemplate.objects.create()
        email_template.text = "Text goes here"
        email_template.subject = "Subject goes here"
        email_template.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/templates'))

@csrf_exempt
def update_user(request):
    allowed_fields = [x.attname for x in EbayUser._meta.fields]
    data = request.POST
    data = {k: v for k, v in data.items() if k in allowed_fields}
    user, created = EbayUser.objects.get_or_create(email=data['email'])
    for k, v in data.items():
        setattr(user, k, v)
    user.cleaned = True
    user.cleaned_date = time.now()
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@csrf_exempt
def send(request):
    emails = EmailTemplate.objects.all()
    attachments = AttachmentTemplate.objects.all()
    attachments = [(a.attachment.url.split('/')[-1], a.attachment.name.split('/')[-1], a.pk) for a in attachments]
    object_list = EbayUser.objects.filter(cleaned=True, sent=False, blacklisted=False)
    context = {'emails': emails, 'attachs': attachments, 'object_list': object_list}
    return render(request, 'send.html', context=context)


@csrf_exempt
def sending(request):
    data = json.loads(request.body)
    try:
        email = int(data['email'])
    except:
        response = {'status': 0, 'txt': "Email template not selected!"}
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        attachments = int(data['attachments'])
    except:
        response = {'status': 0, 'txt': "Attachment template not selected!"}
        return HttpResponse(json.dumps(response), content_type='application/json')
    try:
        users = [int(x) for x in data['users']]
        if len(users) == 0:
            raise Exception()
    except:
        response = {'status': 0, 'txt': "There is no user!" }
        return HttpResponse(json.dumps(response), content_type='application/json')

    ebay_users = EbayUser.objects.filter(pk__in=users)
    attachment = AttachmentTemplate.objects.filter(pk=attachments)
    email = EmailTemplate.objects.filter(pk=email)

    response = {'status': 1, 'txt': 'nice!'}
    for ebay_user in ebay_users:
        ebay_user.sent = True
        ebay_user.date_sent = time.now()
        ebay_user.save()
    return HttpResponse(json.dumps(response), content_type='application/json')


class SearchResultsView(ListView):
    model = EbayUser
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = EbayUser.objects.filter(
            Q(email__icontains=query) | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
        return object_list

