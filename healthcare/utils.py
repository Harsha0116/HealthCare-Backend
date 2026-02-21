from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'success': False,
            'status_code': response.status_code,
            'errors': response.data,
        }

        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_data['message'] = str(response.data['detail'])
                error_data['errors'] = {}
        elif isinstance(response.data, list):
            error_data['message'] = 'Validation error'
            error_data['errors'] = response.data

        response.data = error_data

    return response


def success_response(data=None, message='Success', status_code=status.HTTP_200_OK):
    response_data = {
        'success': True,
        'message': message,
    }
    if data is not None:
        response_data['data'] = data
    return Response(response_data, status=status_code)
