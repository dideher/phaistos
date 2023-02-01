from collections import namedtuple
import operator
from django.db.models import Q
from functools import reduce

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet

from django.http import QueryDict, JsonResponse
from django.views import View


class DataTablesDS(object):

    def __init__(self, request, columns, qs):

        self.columns = columns
        # values specified by the datatable for filtering, sorting, paging
        self.request_values: QueryDict = request.GET
        # results from the db
        self.result_data = None
        # total in the table after filtering
        self.cardinality_filtered = 0
        # total in the table unfiltered
        self.cardinality = 0
        self.user = request.user
        self.qs = qs

        print(self.request_values)
        print("********")

        self.run_queries()

    def output_result(self):
        output = dict()

        output['draw'] = str(int(self.request_values.get('draw', 0)))
        output['recordsTotal'] = str(self.qs.count())
        output['recordsFiltered'] = str(self.cardinality_filtered)
        data_rows = []

        for row in self.result_data:
            data_row = []
            for i in range(len(self.columns)):
                val = row[self.columns[i]]
                data_row.append(val)

            data_rows.append(data_row)

        output['data'] = data_rows

        print("*****************************************************")
        print(f"recordsTotal : {output.get('recordsTotal')}")
        print(f"recordsFiltered : {output.get('recordsFiltered')}")
        print(f"data count : {len(output.get('data', list()))}")
        return output

    def filtering(self):
        # build your filter spec
        or_filter = []
        #
        # if (self.request_values.get('sSearch')) and (self.request_values['sSearch'] != ""):
        #     for i in range(len(self.columns)):
        #         or_filter.append((self.columns[i]+'__icontains', self.request_values['sSearch']))
        #
        # q_list = [Q(x) for x in or_filter]
        #return q_list

        # are we performing a global search
        global_search_pattern = self.request_values.get('search[value]', '')
        if global_search_pattern != '':
            print("****** global search : ", global_search_pattern)
            for i in range(len(self.columns)):
                column_is_searchable = self.request_values.get(f'columns[{i}][searchable]', 'false')
                if column_is_searchable == "true":
                    or_filter.append((self.columns[i] + '__icontains', global_search_pattern))

        # check if we have column specific search patterns
        # CURRENTLY, WE DON'T SUPPORT REGEX
        for i in range(len(self.columns)):
            column_search_value = self.request_values.get(f'columns[{i}][search][value]', '')
            is_search_value_regex = self.request_values.get(f'columns[{i}][search][regex]', 'false')

            if column_search_value != '' and is_search_value_regex == 'false':
                or_filter.append((self.columns[i], column_search_value))


        print(or_filter)

        return [Q(x) for x in or_filter]

    def sorting(self):

        order = list()

        for i in range(len(self.columns)):
            order_column = self.request_values.get(f'order[{i}][column]')
            try:
                if order_column:
                    order_column_dir = self.request_values.get(f'order[{i}][dir]', 'asc')
                    column_name = self.columns[int(order_column)]
                    order.append("-"+column_name if order_column_dir == 'desc' else column_name)
            except IndexError:
                pass

        # if (self.request_values['iSortCol_0'] != "") and (int(self.request_values['iSortingCols']) > 0):
        #
        #     for i in range(int(self.request_values['iSortingCols'])):
        #         # column number
        #         column_number = int(self.request_values['iSortCol_' + str(i)])
        #         # sort direction
        #         sort_direction = self.request_values['sSortDir_' + str(i)]
        #
        #         order = ('' if order == '' else ',') +order_dict[sort_direction]+self.columns[column_number]

        return order

    def paging(self):

        pages = namedtuple('pages', ['start', 'length'])

        start = self.request_values.get('start', 0)
        length = self.request_values.get('length', 50)
        # if (self.request_values['iDisplayStart'] != "") and (self.request_values['iDisplayLength'] != -1):
        #     pages.start = int(self.request_values['iDisplayStart'])
        #     pages.length = pages.start + int(self.request_values['iDisplayLength'])

        pages.start = int(start)
        pages.length = pages.start + int(length)

        print(pages)

        return pages

    def run_queries(self):
        # pages has 'start' and 'length' attributes
        pages = self.paging()
        # # the term you entered into the datatable search

        _filter = self.filtering()
        # # the document field you chose to sort
        sorting = self.sorting()
        # # custom filter
        qs = self.qs

        # if _filter:
        #     data = qs.filter(
        #         reduce(operator.or_, _filter)).order_by('%s' % sorting)
        #     len_data = data.count()
        #     data = list(data[pages.start:pages.length].values(*self.columns))
        # else:
        #     data = qs.order_by('%s' % sorting).values(*self.columns)
        #     len_data = data.count()
        #     _index = int(pages.start)
        #     data = data[_index:_index + (pages.length - pages.start)]

        if _filter:
            data = qs.filter(reduce(operator.or_, _filter)).order_by(*sorting)
            len_data = data.count()
            data = list(data[pages.start:pages.length].values(*self.columns))
            #data = list(data[pages.start:pages.length])
        else:
            data = qs.order_by(*sorting).values(*self.columns)
            #data = qs.order_by(*sorting)

            len_data = data.count()
            _index = int(pages.start)
            data = data[_index:_index + (pages.length - pages.start)]

        self.result_data = list(data)

        # # length of filtered set
        if _filter:
            self.cardinality_filtered = len_data
        else:
            self.cardinality_filtered = len_data

        self.cardinality = pages.length - pages.start


class OurServerSideDatatableView(View):
    columns = None
    queryset = None
    model = None

    def get(self, request, *args, **kwargs):
        result = DataTablesDS(
            request, self.columns, self.get_queryset()).output_result()

        return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        return queryset
