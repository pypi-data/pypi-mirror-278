from drf_yasg import openapi


from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view



schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="Your API Description",
        terms_of_service="https://yourapi.com/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)



# Define common responses
common_responses = {
    '401': openapi.Response('Authentication credentials were not provided.'),
    '403': openapi.Response('Permission denied.'),
    '500': openapi.Response('Internal Server Error', response_body=None),
}

# Define responses for create view
create_responses = {
    '400': openapi.Response('Validation error'),
    **common_responses,
}

# Define responses for list view
list_responses = {
    '200': openapi.Response('Resources retrieved Successfully.'),
    '204': openapi.Response('No Content'),
    **common_responses,
}

# Define responses for retrieve view
retrieve_responses = {
    '400': openapi.Response('Validation error'),
    '200': openapi.Response('Resource retrieved Successfully.'),
    '404': openapi.Response('Resource not found.'),
    **common_responses,
}

# Define responses for update view
update_responses = {
    '200': openapi.Response('Resource updated Successfully.'),
    '400': openapi.Response('Validation error'),
    '404': openapi.Response('Resource not found.'),
    **common_responses,
}

# Define responses for delete view
delete_responses = {
    '200': openapi.Response('Resource deleted Successfully.'),
    '404': openapi.Response('Resource not found.'),
    **common_responses,
}
