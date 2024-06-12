from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django.core.paginator import Paginator





class GenericPaginator:

    @staticmethod
    def paginate(queryset, serializer_class, page_number, page_size):
        paginator = Paginator(queryset, page_size)
        serialized_data = serializer_class(
            paginator.page(page_number), many=True).data
        return {"data": serialized_data, "count": paginator.count}


class CustomFilterPagination(PageNumberPagination):
    """
    Custom pagination class that extends Django Rest Framework's PageNumberPagination class.
    Overrides the get_paginated_response method to return a custom response object that includes
    pagination metadata and the paginated data.

    Attributes:
        page_size (int): The number of objects to include in each page of results.
    """

    page_size = 1

    def get_paginated_response(self, data):
        """
        Overrides the get_paginated_response method of the parent class to return a custom response
        object that includes pagination metadata and the paginated data.

        Args:
            data (list): The list of objects in the current page of results.

        Returns:
            Response: A Response object containing pagination metadata and the paginated data.
        """

        return Response({
            'pagination': {
                'count': self.page.paginator.count,
                'current_page': self.page.number,
                'has_more': self.page.has_next(),
            },
            'data': data
        })
