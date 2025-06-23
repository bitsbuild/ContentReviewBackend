from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
class ContentsPnPagination(PageNumberPagination):
    page_size = 3
    # page_query_param = 'p' instead of page= we do p= in url to access page
    page_size_query_param = 'size'
    max_page_size = 30
    last_page_strings = ['end']
    invalid_page_message = 'Invalid Page Selected'
    display_page_controls = True
class ContentsLoPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 30
    limit_query_param = 'limit'
    offset_query_param = 'start'
class ContentsCPagination(CursorPagination):
    page_size = 3
    ordering = 'content_created'
    cursor_query_param = 'autopage'