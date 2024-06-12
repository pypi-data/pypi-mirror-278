#Python Imports
from functools import wraps

#Django Imports

#Third-Party Imports

#Project-Specific Imports
from common_utils.utils import generate_response,generate_error_response

#Relative Import

def replace_placeholder_with_id(model, attribute, placeholder_key):
    """
    A decorator to replace a placeholder value in request.data with the corresponding model's ID.

    Args:
        model (class): The Django model class to query.
        attribute (str): The attribute name in the model to match.
        placeholder_key (str): The key in request.data where the placeholder value is located.

    Returns:
        function: A decorator function.

    Example:
        @replace_placeholder_with_id(Endpoint, 'name', 'endpoint_name')
        def your_view(request):
            # Your view logic here
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if request.data.get(placeholder_key) is not None:
                # Get the placeholder value from request.data
                placeholder_value = request.data[placeholder_key]
                obj = model.objects.filter(**{attribute: placeholder_value}).first()
                if obj:
                    # Replace the placeholder value with the object's ID
                    request.data[placeholder_key] = obj.id
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator

def check_required_keys(keys):
    """
    A decorator that checks if the specified keys are present in the request query parameters or request data and not None.
    """

    def decorator(view_func):
        @ wraps(view_func)
        def wrapper(*args, **kwargs):
            request = args[1]
            if request.method == 'GET':
                data = request.query_params
            elif request.method in ['POST', 'PUT']:
                data = request.data
            else:
                return generate_response(status=status.HTTP_400_BAD_REQUEST, message='Invalid request method')

            for key in keys:
                if key not in data or data[key] is None:
                    return generate_response(status=status.HTTP_400_BAD_REQUEST, message=f"'{key}' is required and cannot be None.")

            return view_func(*args, **kwargs)
        return wrapper
    return decorator


def add_tenant_identifier_to_request_data(func):
    """
    A decorator that adds the 'tenant_identifier' from the 'HTTP_TENANT_IDENTIFIER' header to the request's data.

    This decorator checks for the presence of the 'HTTP_TENANT_IDENTIFIER' header in the request's META dictionary. If the header
    exists, it adds the 'tenant_identifier' value to the request's data dictionary, making it accessible within the view function.

    Args:
        func (function): The view function to decorate.

    Returns:
        function: The decorated view function with 'tenant_identifier' added to request.data if the header is present.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        tenant_identifier = request.META.get('HTTP_TENANT_IDENTIFIER')
        
        if tenant_identifier:
            request.data['tenant_identifier'] = tenant_identifier
        
        return func(request, *args, **kwargs)
    
    return wrapper


