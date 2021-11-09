from django.core import paginator
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin

from leaves.models import Leave

class BaseDeleteView(SingleObjectMixin, DeletionMixin, View):

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)
        
        if request.POST is not None:
            self.success_url = request.POST['success_url']

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.deleted_on = timezone.now()
        self.object.deleted_comment = request.POST.get('delete_comment_text')
        self.object.save()
        return HttpResponseRedirect(success_url)

class LeaveDeleteView(BaseDeleteView):

    model = Leave

    
    
    