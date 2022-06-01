# https://gist.github.com/eternalflow/263a5621988415a33dbcd34499746108

import csv
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook
import datetime

from operator import attrgetter, itemgetter, methodcaller
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.encoding import force_str

from django.urls import reverse, re_path
from django.contrib.admin.options import IncorrectLookupParameters
from django.views.generic.list import ListView


class ExportResponseHelper(object):
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def export(self, extension, *args, **kwargs):
        method = getattr(self, "export_{}".format(extension), None)
        if method is not None:
            return method(*args, **kwargs)
        return HttpResponseBadRequest()

    def export_csv(self, **kwargs):
        header, footer = kwargs.get('header'), kwargs.get('footer')

        response = HttpResponse(content_type='text/csv', charset='utf-8')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="{}.csv"'.format(self.filename))
        writer = csv.writer(response)
        if header is not None:
            writer.writerow(header)
        for row in self.data:
            writer.writerow(row)
        if footer is not None:
            writer.writerow(footer)
        return response

    def export_xls(self, **kwargs):
        header, footer = kwargs.get('header'), kwargs.get('footer')


        wb = openpyxl.Workbook()

        #ws = wb.add_sheet(self.filename)

        # header_style = xlwt.XFStyle()
        # header_style.font.bold = True
        # footer_style = xlwt.XFStyle()
        # footer_style.font.bold = True
        # data_cells_style = xlwt.XFStyle()
        # data_cells_style.alignment.wrap = 1
        #
        row_num = 0
        # if header:
        #     for col_num, col_header in enumerate(header):
        #         ws.write(row_num, col_num, col_header, header_style)

        if header:
            wb.active.append(header)

        for row in self.data:
            row_num += 1
            wb.active.append(row)
            # for col_num, col_val in enumerate(row):
            #     # avoiding issue when excel converts dates to numbers by setting cell format
            #     if isinstance(col_val, datetime.datetime):
            #         data_cells_style.num_format_str = "YYYY-MM-DD h:mm"
            #         # datetime may come with tzinfo
            #         # but due to internal xlwt module magic we should pass timezone unaware datetime
            #         tzunaware = col_val.replace(tzinfo=None)
            #         offset = col_val.timestamp() - tzunaware.timestamp()
            #         col_val = tzunaware + datetime.timedelta(seconds=offset)
            #     elif isinstance(col_val, datetime.time):
            #         data_cells_style.num_format_str = "h:mm"
            #     elif isinstance(col_val, datetime.date):
            #         data_cells_style.num_format_str = "YYYY-MM-DD"
            #     else:
            #         data_cells_style.num_format_str = "@"
            #
            #     ws.write(row_num, col_num, col_val, data_cells_style)

        row_num += 1
        # if footer:
        #     for col_num, col_footer in enumerate(footer):
        #         ws.write(row_num, col_num, col_footer, footer_style)

        if footer:
            wb.active.append(footer)

        # # TODO calc comfortable col width
        # col_width_list = [6000] * len(self.data[0])  if self.data else []
        # for col_num, width in enumerate(col_width_list):
        #     ws.col(col_num).width = col_width_list[col_num]

        response = HttpResponse(content=save_virtual_workbook(workbook=wb),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="{}.xls"'.format(self.filename))
        return response

    def export_txt(self, **kwargs):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="{}.txt"'.format(self.filename))
        for row in self.data:
            response.write(row)
        return response


class ExportMixin(object):
    """
    Params:
     - export_formats (list of str): list of formats we're able to export to
     - export_filename (str): export filename without extension. defaults to model._meta.model_name
     - export_header (list of str): optional. if defined, this will be the first row of output file
     - export_footer: like header but last line
     - export_fields (list of str/callable): required. describes how to access values
        Example value:
        [
            "field_name",
            "related_object.field_name",
            "dict_key",
            "model_instance_method",
            "this_view_instance_method"
            your_own_callable
        ]
        Example exported row:
        [
            item.field_name,
            item.related_object.field_name
            item['dict_key'],
            item.model_instance_method(),
            self.this_view_instance_method(),
            your_own_callable(item)
        ]
    """

    export_formats = ["xls", "csv", "txt"]
    export_filename = None
    export_header = None
    export_footer = None
    export_fields = None

    def _row_mapper(self, item):
        """
        This function knows how to make table row from queryset item using export_fields.
        """

        def anyget(obj, field, default=None):
            getters = methodcaller(field), itemgetter(field), attrgetter(field)
            for getter in getters:
                try:
                    v = getter(obj)
                    #  when trying to get magic model methods like get_<fieldname>_display,
                    #  methodcaller will fail, but attrgetter will not, so i want to call it explicitly
                    if callable(v):
                        v = v()
                    return v
                except (TypeError, KeyError, AttributeError):
                    continue
            return default

        row = []
        for field in self.get_export_fields():
            if isinstance(field, str):
                v = anyget(item, field)
                if v is None:
                    fn = getattr(self, field, None)
                    if callable(fn):
                        v = fn(item)
            elif callable(field):
                v = field(item)
            else:
                v = None
            row.append(v)
        return row

    def get_export_queryset(self, *args, **kwargs):
        return self.get_queryset()

    def get_export_header(self):
        return list(map(force_str, self.export_header)) if self.export_header else None

    def get_export_footer(self):
        return list(map(force_str, self.export_footer)) if self.export_footer else None

    def get_export_fields(self):
        return self.export_fields

    def get_export_filename(self):
        return self.export_filename

    def get_export_response(self, request, extension):
        if extension not in self.export_formats:
            return HttpResponseBadRequest()

        export_qs = self.get_export_queryset(request)
        export_items = list(map(self._row_mapper, export_qs))
        filename = self.get_export_filename()
        header = self.get_export_header()
        footer = self.get_export_footer()
        return ExportResponseHelper(filename, export_items).export(extension, header=header, footer=footer)


class ExportableListView(ExportMixin, ListView):
    export_get_arg = "export"

    def get(self, *args, **kwargs):
        ext = self.request.GET.get(self.export_get_arg)
        if ext not in self.export_formats:
            return super(ExportableListView, self).get(*args, **kwargs)
        return self.get_export_response(self.request, ext)


class ModelAdminExportMixin(ExportMixin):
    """
    Mix this class with any ModelAdmin

    Contains logic:
        - get queryset after applying all filters and ordering
        - add export view to ModelAdmin
        - register URLs to access it
        - makes URL available in change_list template
    """

    def get_export_urlname(self):
        default_url = "{app_label}_{model_name}_export".format(
            app_label=self.opts.app_label,
            model_name=self.opts.model_name)
        return default_url

    def get_urls(self):
        urls = super(ModelAdminExportMixin, self).get_urls()
        my_urls = [
            re_path('^export/(?P<extension>[a-z]*)/$',
                self.admin_site.admin_view(self.export_view),
                name=self.get_export_urlname())
        ]
        return my_urls + urls

    def export_view(self, request, extension):
        return super(ModelAdminExportMixin, self).get_export_response(request, extension)

    def get_export_queryset(self, request):
        #  self.get_queryset will not apply filters
        #  create ChangeList to apply filters and ordering
        #  see https://github.com/django/django/blob/stable/1.9.x/django/contrib/admin/options.py:1453

        cl_type = self.get_changelist(request)
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)
        list_select_related = self.get_list_select_related(request)
        actions = self.get_actions(request)
        if actions:
            list_display = ['action_checkbox'] + list(list_display)

        try:
            changelist = cl_type(request, self.model, list_display, list_display_links,
                         list_filter, self.date_hierarchy, search_fields,
                         list_select_related, self.list_per_page,
                         self.list_max_show_all, self.list_editable, self)
        except IncorrectLookupParameters:
            return redirect(
                reverse('admin:{}_{}_changelist'.format(
                    self.opts.app_label, self.opts.model_name)))

        return changelist.queryset

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        param_str = '?' + request.GET.urlencode()
        extra_context['export_urls'] = {
            ext: reverse("admin:" + self.get_export_urlname(), kwargs={'extension': ext}) + param_str
            for ext in self.export_formats
        }
        response = super(ModelAdminExportMixin, self).changelist_view(request, extra_context)
        return response