from rest_framework.views import Response
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    """"""

    page_query_param = 'page'
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'data': data
        })
