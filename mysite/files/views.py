import base64
import hashlib
import hmac
import os
import time
import datetime
from django.utils import timezone
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .config_s3_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
    AWS_UPLOAD_ACCESS_KEY_ID,
    AWS_UPLOAD_SECRET_KEY,
    AWS_S3_SIGNATURE_VERSION,
)
from .models import DownloadableFile, VideoFile, ImageFile
from .forms import ImageFileForm, VideoFileForm, DownloadableFileForm
from portal.models import Store
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View, CreateView, DeleteView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import json
from django.contrib import messages
from django.shortcuts import redirect
from users.decorators import IsMerchantMixin, IsUserObject

from django.core.exceptions import ValidationError

class VideoFileUploadView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        # video_list = VideoFile.objects.filter(user=self.request.user)

        store_slug = self.kwargs['slug']
        store_qs = Store.objects.get(slug=store_slug)

        try:
            video = store_qs.videofile
            if store_qs.videofile.file != None:
                messages.warning(self.request, "Video already exists, please delete it before uploading a new one. Visit 'View Content' to delete.")
                return redirect('/dashboard/')
        except:
            context = {
            # "video_list": video_list,
            "store_slug": store_slug,
            }
            return render(self.request, 'files/videofile_form_create.html', context)

<<<<<<< HEAD


=======
>>>>>>> bug_fixes
    def post(self, request, *args, **kwargs):
        form = VideoFileForm(self.request.POST, self.request.FILES)
        # user = request.user
        store_slug = self.kwargs['slug']
        store_qs = Store.objects.get(slug=store_slug)

        if form.is_valid():
            videofile = form.save(commit=False)
            videofile.store = store_qs
            videofile = form.save()
            data = {'is_valid': True, 'url': videofile.file.url}

            user = store_qs.merchant.merchant_profile
            user.content_uploaded = True
            user.save()
        else:
            if ValidationError:
                # returns ValdiationError Message as a Json Object
                error = form.errors.as_json()

                # Loads Json data from a string
                error_json_object = json.loads(error)
                print(error_json_object)
                message = error_json_object['file'][0]['message']

                data = {'is_valid': False, 'message': message}
        return JsonResponse(data)



class MerchantVideoFileDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = VideoFile
    template_name = 'files/merchant_video_delete.html'
    success_url = reverse_lazy('users:userPage')
    success_message = "Video Deleted"


class MerchantVideoFileDetailView(DetailView):
	model = VideoFile
	template_name = 'files/merchant_video_detail.html'


# ***************** IMAGE UPLOAD ************************

class ImageFileUploadView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        store_slug = self.kwargs['slug']
        store = Store.objects.get(slug=store_slug)
        imagefile_list = ImageFile.objects.filter(store__slug=store_slug)

        context = {
        "imagefile_list": imagefile_list,
        "store_slug": store_slug,
        "store": store,
        }
        return render(self.request, 'files/imagefile_form_create.html', context)


    def post(self, request, *args, **kwargs):
        form = ImageFileForm(self.request.POST, self.request.FILES)
        # user = request.user
        store_slug = self.kwargs['slug']
        store_qs = Store.objects.get(slug=store_slug)

        if form.is_valid():
            imagefile = form.save(commit=False)
            imagefile.store = store_qs
            imagefile = form.save()
            data = {'is_valid': True, 'name': imagefile.title, 'url': imagefile.file.url }

            user = store_qs.merchant.merchant_profile
            user.content_uploaded = True
            user.save()
        else:
            if ValidationError:
                # returns ValdiationError Message as a Json Object
                error = form.errors.as_json()

                # Loads Json data from a string
                error_json_object = json.loads(error)
                print(error_json_object)
                message = error_json_object['file'][0]['message']

                data = {'is_valid': False, 'message': message}
        return JsonResponse(data)

class MerchantImageFileDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ImageFile
    template_name = 'files/merchant_image_delete.html'
    success_url = reverse_lazy('users:userPage')
    success_message = "Image Deleted"


class MerchantImageFileDetailView(DetailView):
	model = ImageFile
	template_name = 'files/merchant_video_detail.html'


# ***************** DOWNLOADABLE FILE UPLOAD ************************


class FileUploadView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        store_slug = self.kwargs['slug']
        store_qs = Store.objects.get(slug=store_slug)
        store = Store.objects.get(slug=store_slug)

        try:
            file = store_qs.downloadablefile
            if store_qs.downloadablefile.file != None:
                messages.warning(self.request, "File already exists, please delete it before uploading a new one. Visit 'View Content' to delete.")
                return redirect('/dashboard/')
        except:
            context = {
            "store_slug": store_slug,
            "store": store,
            }
            return render(self.request, 'files/downloadable_files/file_form_create.html', context)


    def post(self, request, *args, **kwargs):
        form = DownloadableFileForm(self.request.POST, self.request.FILES)
        # user = request.user
        store_slug = self.kwargs['slug']
        store_qs = Store.objects.get(slug=store_slug)

        if form.is_valid():
            downloadablefile = form.save(commit=False)
            downloadablefile.store = store_qs
            downloadablefile = form.save()
            data = {'is_valid': True, 'url': downloadablefile.file.url}

            user = store_qs.merchant.merchant_profile
            user.content_uploaded = True
            user.save()
        else:
            if ValidationError:
                # returns ValdiationError Message as a Json Object
                error = form.errors.as_json()

                # Loads Json data from a string
                error_json_object = json.loads(error)
                print(error_json_object)
                message = error_json_object['file'][0]['message']

                data = {'is_valid': False, 'message': message}
        return JsonResponse(data)


class MerchantFileDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DownloadableFile
    template_name = 'files/downloadable_files/merchant_file_delete.html'
    success_url = reverse_lazy('users:userPage')
    success_message = "File Deleted"


class MerchantFileDetailView(DetailView):
	model = DownloadableFile
	template_name = 'files/downloadable_files/merchant_file_detail.html'


#****************** FILE UPLOAD SELECTOR *********************************

class FileUploadSelector(LoginRequiredMixin, IsMerchantMixin, View):

    def get(self, request, *args, **kwargs):
        store_slug = self.kwargs['slug']
        context = {
            'store_slug': store_slug
        }
        return render(self.request, 'files/merchant_file_select.html', context)


class MerchantContentDetailView(LoginRequiredMixin, IsMerchantMixin, View):
    def get(self, request, *args, **kwargs):
        store_slug = self.kwargs['slug']
        store_qs = Store.objects.get(slug=store_slug)

        downloadablefile_qs = []
        videofile_qs = []
        try:
            downloadablefile_qs = DownloadableFile.objects.get(store__slug=store_slug)
        except:
            pass
        try:
            videofile_qs = VideoFile.objects.get(store__slug=store_slug)
        except:
            pass
        imagefile_qs = ImageFile.objects.filter(store__slug=store_slug)


        context = {
            'downloadablefile': downloadablefile_qs,
            'image_list': imagefile_qs,
            'videofile': videofile_qs,
            'store_slug': store_slug,
            'object': store_qs
        }
        return render(self.request, 'files/merchant_content_detail.html', context)



class FilePolicyAPI(APIView):
    """
    This view is to get the AWS Upload Policy for our s3 bucket.
    What we do here is first create a FileItem object instance in our
    Django backend. This is to include the FileItem instance in the path
    we will use within our bucket as you'll see below.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        """
        The initial post request includes the filename
        and auth credientails. In our case, we'll use
        Session Authentication but any auth should work.
        """
        filename_req = request.data.get('filename')
        if not filename_req:
                return Response({"message": "A filename is required"}, status=status.HTTP_400_BAD_REQUEST)
        policy_expires = int(time.time()+1000)

        #Testing
        two_months = datetime.timedelta(days=61)
        date_two_months_later = datetime.date.today() + two_months
        expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")
        print (expires)
        print('time.now', timezone.now)

        user = request.user
        username_str = str(request.user.username)
        """
        Below we create the Django object. We'll use this
        in our upload path to AWS.

        Example:
        To-be-uploaded file's name: Some Random File.mp4
        Eventual Path on S3: <bucket>/username/2312/2312.mp4
        """
        file_obj = FileItem.objects.create(user=user, name=filename_req)
        file_obj_id = file_obj.id
        upload_start_path = "{username}/{file_obj_id}/".format(
                    username = username_str,
                    file_obj_id=file_obj_id
            )
        _, file_extension = os.path.splitext(filename_req)
        filename_final = "{file_obj_id}{file_extension}".format(
                    file_obj_id= file_obj_id,
                    file_extension=file_extension

                )
        """
        Eventual file_upload_path includes the renamed file to the
        Django-stored FileItem instance ID. Renaming the file is
        done to prevent issues with user generated formatted names.
        """
        final_upload_path = "{upload_start_path}{filename_final}".format(
                                 upload_start_path=upload_start_path,
                                 filename_final=filename_final,
                            )
        if filename_req and file_extension:
            """
            Save the eventual path to the Django-stored FileItem instance
            """
            file_obj.path = final_upload_path
            file_obj.save()

        policy_document_context = {
            "expire": policy_expires,
            "bucket_name": AWS_UPLOAD_BUCKET,
            "key_name": "",
            "acl_name": "private",
            "content_name": "",
            "content_length": 524288000,
            "upload_start_path": upload_start_path,

            }
        policy_document = """
        {"expiration": "2019-01-01T00:00:00Z",
          "conditions": [
            {"bucket": "%(bucket_name)s"},
            ["starts-with", "$key", "%(upload_start_path)s"],
            {"acl": "%(acl_name)s"},

            ["starts-with", "$Content-Type", "%(content_name)s"],
            ["starts-with", "$filename", ""],
            ["content-length-range", 0, %(content_length)d]
          ]
        }
        """ % policy_document_context
        aws_secret = str.encode(AWS_UPLOAD_SECRET_KEY)
        policy_document_str_encoded = str.encode(policy_document.replace(" ", ""))
        url = 'https://{bucket}.s3-{region}.amazonaws.com/'.format(
                        bucket=AWS_UPLOAD_BUCKET,
                        region=AWS_UPLOAD_REGION
                        )
        policy = base64.b64encode(policy_document_str_encoded)
        signature = base64.b64encode(hmac.new(aws_secret, policy, hashlib.sha1).digest())

        bucket_params = {'Key': AWS_UPLOAD_ACCESS_KEY_ID, 'Bucket': AWS_UPLOAD_BUCKET, 'ACL': 'public-read'}
        url = s3.generate_presigned_url(ClientMethod='put_object', Params=bucket_params)

        data = {
            "policy": policy,
            # "signature": signature,
            "key": AWS_UPLOAD_ACCESS_KEY_ID,
            "file_bucket_path": upload_start_path,
            "file_id": file_obj_id,
            "filename": filename_final,
            "url": url,
            "username": username_str,
        }
        return Response(data, status=status.HTTP_200_OK)

class FileUploadCompleteHandler(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]

    def post(self, request, *args, **kwargs):
        file_id = request.POST.get('file')
        size = request.POST.get('fileSize')
        data = {}
        type_ = request.POST.get('fileType')
        if file_id:
            obj = FileItem.objects.get(id=int(file_id))
            obj.size = int(size)
            obj.uploaded = True
            obj.type = type_
            obj.save()
            data['id'] = obj.id
            data['saved'] = True
        return Response(data, status=status.HTTP_200_OK)
