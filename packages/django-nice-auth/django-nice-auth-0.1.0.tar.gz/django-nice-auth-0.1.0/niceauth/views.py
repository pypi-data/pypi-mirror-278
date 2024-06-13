from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
import json
from .models import NiceAuthRequest, NiceAuthResult
from nice_auth.services import NiceAuthService
from nice_auth.exceptions import NiceAuthException


class GetNiceAuthView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return self.handle_request(request)

    def post(self, request):
        return self.handle_request(request)

    def handle_request(self, request):
        try:
            service = NiceAuthService(
                base_url=settings.NICE_AUTH_BASE_URL,
                client_id=settings.NICE_CLIENT_ID,
                client_secret=settings.NICE_CLIENT_SECRET,
                product_id=settings.NICE_PRODUCT_ID,
                return_url=settings.NICE_RETURN_URL,
                authtype=settings.NICE_AUTHTYPE,
                popupyn=settings.NICE_POPUPYN
            )
            auth_data = service.get_nice_auth()
            auth_request = NiceAuthRequest.objects.create(
                request_no=auth_data["requestno"],
                enc_data=auth_data["enc_data"],
                integrity_value=auth_data["integrity_value"],
                token_version_id=auth_data["token_version_id"],
                key=auth_data["key"],
                iv=auth_data["iv"]
            )
            return JsonResponse({
                'request_no': auth_request.request_no,
                'enc_data': auth_request.enc_data,
                'integrity_value': auth_request.integrity_value,
                'token_version_id': auth_request.token_version_id
            })
        except NiceAuthException as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


class GetNiceAuthUrlView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return self.handle_request(request)

    def post(self, request):
        return self.handle_request(request)

    def handle_request(self, request):
        try:
            service = NiceAuthService(
                base_url=settings.NICE_AUTH_BASE_URL,
                client_id=settings.NICE_CLIENT_ID,
                client_secret=settings.NICE_CLIENT_SECRET,
                product_id=settings.NICE_PRODUCT_ID,
                return_url=settings.NICE_RETURN_URL,
                authtype=settings.NICE_AUTHTYPE,
                popupyn=settings.NICE_POPUPYN
            )
            auth_data = service.get_nice_auth()
            auth_request = NiceAuthRequest.objects.create(
                request_no=auth_data["requestno"],
                enc_data=auth_data["enc_data"],
                integrity_value=auth_data["integrity_value"],
                token_version_id=auth_data["token_version_id"],
                key=auth_data["key"],
                iv=auth_data["iv"]
            )
            nice_url = f"https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb?m=service&token_version_id={auth_data['token_version_id']}&enc_data={auth_data['enc_data']}&integrity_value={auth_data['integrity_value']}"
            return JsonResponse({'nice_auth_url': nice_url})
        except NiceAuthException as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


class VerifyNiceAuthView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = request.POST
            enc_data = data['enc_data']
            token_version_id = data['token_version_id']
            integrity_value = data['integrity_value']

            auth_request = get_object_or_404(NiceAuthRequest, token_version_id=token_version_id)
            key = auth_request.key
            iv = auth_request.iv

            service = NiceAuthService(
                base_url=settings.NICE_AUTH_BASE_URL,
                client_id=settings.NICE_CLIENT_ID,
                client_secret=settings.NICE_CLIENT_SECRET,
                product_id=settings.NICE_PRODUCT_ID,
                return_url=settings.NICE_RETURN_URL,
                authtype=settings.NICE_AUTHTYPE,
                popupyn=settings.NICE_POPUPYN
            )

            result_data = service.verify_auth_result(enc_data, key, iv)
            auth_result = NiceAuthResult.objects.create(
                request=auth_request,
                result_data=result_data
            )
            return JsonResponse(result_data)
        except NiceAuthException as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
