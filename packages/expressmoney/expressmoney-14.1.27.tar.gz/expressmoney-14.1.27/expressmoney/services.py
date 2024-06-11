import json
import os
import time
from datetime import datetime, timedelta
from decimal import Decimal

import boto3
import jwt
import requests
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class _IamTokenService:
    URL = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

    def __init__(self):
        authorized_key = json.loads(os.getenv('IAM'))
        self._service_account_id = authorized_key['service_account_id']
        self._key_id = authorized_key['id']
        self._private_key = authorized_key['private_key']
        self._iam_token = None
        self._expires_at = None

    def get_token(self):
        if self._expires_at and self._expires_at > datetime.now():
            return self._iam_token
        else:
            self._iam_token, self._expires_at = self._request()
        return self._iam_token

    def _request(self):
        now = int(time.time())
        payload = {
            'aud': self.URL,
            'iss': self._service_account_id,
            'iat': now,
            'exp': now + 360}
        encoded_token = jwt.encode(
            payload,
            self._private_key,
            algorithm='PS256',
            headers={'kid': self._key_id})
        response = requests.post(self.URL, json={'jwt': encoded_token}).json()
        return response['iamToken'], datetime.now() + timedelta(hours=1)


class RuSmsService:
    _url = 'https://omnichannel.mts.ru/http-api/v1/messages'

    def __init__(self, sender):
        self._login, self._password = os.getenv('MTS_SMS').split('||')
        self._sender = sender

    def send(self, phonenumber, message):
        response = requests.post(self._url,
                                 json=self._get_payload(phonenumber, self._sender, message),
                                 auth=HTTPBasicAuth(self._login, self._password),
                                 timeout=(30, 30)
                                 )
        if not status.is_success(response.status_code):
            raise ValidationError(response.text)
        result = self._get_result(response.json().get("messages")[0].get("internal_id"))
        self._handle_errors(result)

    def _get_result(self, internal_id):
        try:
            response_info = requests.post(url=f"{self._url}/info",
                                          json={"int_ids": [internal_id]},
                                          auth=HTTPBasicAuth(self._login, self._password), )
            return response_info.json().get('events_info')[0].get('events_info')[0]
        except (IndexError, TypeError, IOError):
            pass

    @staticmethod
    def _get_payload(phonenumber, sender, message):
        msisdn = f'{phonenumber.country_code}{phonenumber.national_number}'
        payload = {
            "messages": [
                {
                    "content": {
                        "short_text": message
                    },
                    "from": {
                        "sms_address": sender
                    },
                    "to": [
                        {
                            "msisdn": msisdn
                        }
                    ]
                }
            ]
        }
        return payload

    @staticmethod
    def _handle_errors(result):
        if not result:
            return
        internal_errors = result.get('internal_errors')
        if not internal_errors:
            return result
        elif 10802 in internal_errors:
            raise ValidationError('phonenumber_format_error')
        elif 10803 in internal_errors:
            raise ValidationError('unsupported_code_country')
        elif 10904 in internal_errors:
            raise ValidationError('phonenumber_blacklist')
        elif 10100 in internal_errors:
            raise ValidationError('incorrect_sender')
        else:
            raise ValidationError(internal_errors)


class YandexObjectService:
    _bucket = 'expressmoney'
    _filename = None

    def __init__(self):
        self._s3 = boto3.session.Session().client(service_name='s3', endpoint_url='https://storage.yandexcloud.net')

    def generate_key(self, filename):
        self._filename = filename
        prepared_form_fields = self._s3.generate_presigned_post(Bucket=self._bucket,
                                                                Key=f'files/{self._filename}',
                                                                Conditions=[["starts-with", "$key", "files"], ],
                                                                ExpiresIn=60 * 60)
        return json.dumps(prepared_form_fields)


class ScoringService:
    _url = 'https://api.expressmoney.com/ru_scoring/pdl_ru/scoring'

    def __init__(self):
        self._headers = {'Authorization': f'Token {os.getenv("SERVICE_TOKEN")}'}

    def request(self, data: dict) -> Decimal:
        response = requests.post(self._url, headers=self._headers, json=data, verify=False, timeout=(300, 300))
        order_id = data.get("order_id")
        if status.is_success(response.status_code):
            return response.json().get('amount_approved')
        elif response.status_code == status.HTTP_400_BAD_REQUEST and order_id:
            response = requests.get(f'{self._url}/{order_id}', headers=self._headers)
            if status.is_success(response.status_code):
                return response.json().get('amount_approved')
        raise ValidationError(response.text[:1024])


class RuPartnerService:
    SERVICE_URL = 'https://bbaic3serh6adpvivht0.containers.yandexcloud.net'

    def __init__(self):
        self._iam_token_service = _IamTokenService()

    def create_lead(self, referral_id: int):
        url = f'{self.SERVICE_URL}/ru_partners/leads/lead'
        requests.post(url, headers=self._get_header(referral_id), data={'description': 1})

    def create_referral(self, referral_id, partner_code):
        url = f'{self.SERVICE_URL}/ru_partners/referrals/referral'
        requests.post(url, headers=self._get_header(referral_id), data={'partner_code': partner_code})

    def create_bonus(self, user_id, description_id):
        url = f'{self.SERVICE_URL}/ru_partners/bonuses/bonus'
        requests.post(url, headers=self._get_header(user_id), data={'description': description_id})

    def send_order_postback(self, user_id: int, order_id: int, utm_source: str, transaction_id: str, amount):
        url = f'{self.SERVICE_URL}/ru_partners/cpa/order_client_post_back'
        requests.post(url,
                      headers=self._get_header(user_id),
                      data={
                          'order_id': order_id,
                          'utm_source': utm_source,
                          'transaction_id': transaction_id,
                          'amount': amount
                      })

    def send_loan_postback(self, user_id: int, loan_id: int, utm_source: str, transaction_id: str, amount):
        url = f'{self.SERVICE_URL}/ru_partners/cpa/loan_client_post_back'
        requests.post(url, headers=self._get_header(user_id), data={
            'loan_id': loan_id,
            'utm_source': utm_source,
            'transaction_id': transaction_id,
            'amount': amount
        })

    def get_cpa_client(self, user_id: int):
        url = f'{self.SERVICE_URL}/ru_partners/cpa/cpa_client/{user_id}'
        return requests.get(url, headers=self._get_header(user_id))

    def _get_header(self, user_id):
        refresh = RefreshToken.for_user(User.objects.get(pk=user_id))
        headers = {
            'Authorization': f'Bearer {self._iam_token_service.get_token()}',
            'Auth': f'Bearer {refresh.access_token}'
        }
        return headers
