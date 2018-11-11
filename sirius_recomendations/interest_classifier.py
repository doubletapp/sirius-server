# -*- coding: utf-8 -*-
import os
import pickle
import retrying
from urllib.parse import urljoin
from requests import Session
from traceback import format_exc

CLASSES = ['history', 'math', 'proger']
dir_path = os.path.dirname(__file__)
with open(os.path.join(dir_path, 'interest_classifier.pkl'), 'rb') as f:
    classifier = pickle.load(f)
with open(os.path.join(dir_path, 'vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)


class TooManyRequests(Exception):
    code = 6
    message = 'Too many requests per second'


class AccessDenied(Exception):
    code = 15
    message = 'Access denied: this profile is private'


class UserDeleted(Exception):
    code = 18
    message = 'User was deleted or banned'


class UnknownException(Exception):
    pass


class ApiMethod():
    URL = 'https://api.vk.com'

    def __init__(self, session, request_args):
        self._session = session
        self._request_args = request_args

    @retrying.retry(wait_fixed=1000, stop_max_attempt_number=5)
    def _request(self, method, **params):
        url = urljoin(self.URL, '.'.join((self.method, method)))
        try:
            response = self._session.get(url, params=dict(params,
                                                          **self._request_args))
            _json = response.json()
            if 'response' in _json:
                return _json['response']
            elif 'error' in _json:
                if _json['error']['error_code'] == TooManyRequests.code:
                    raise TooManyRequests()
                elif _json['error']['error_code'] in (
                AccessDenied.code, UserDeleted.code):
                    return {'items': []}  # quite unsafe
                else:
                    raise UnknownException  # Todo
            else:
                raise UnknownException  # Todo
        except TooManyRequests:
            raise
        except (Exception, UnknownException):
            # debug
            print(format_exc())
            print(response.content)
            raise


class Users(ApiMethod):
    method = '/method/users'

    def get(self, user_id, **params):
        return self._request('get', user_id=user_id, **params)


class Groups(ApiMethod):
    method = '/method/groups'

    def get(self, user_id, **params):
        return self._request('get', user_id=user_id, **params)

    def get_members(self, group_id, **params):
        return self._request('getMembers', group_id=group_id, **params)


class Friends(ApiMethod):
    method = '/method/friends'

    def get(self, user_id, **params):
        return self._request('get', user_id=user_id, **params)


class VkAPI():
    VERSION = '5.87'

    def __init__(self, token):
        self._session = Session()
        self.token = token
        request_args = {
            'v': self.VERSION,
            'access_token': token
        }
        self.users = Users(self._session, request_args)
        self.groups = Groups(self._session, request_args)
        self.friends = Friends(self._session, request_args)


def predict_proba(vk_id, vk_token):
    api = VkAPI(vk_token)
    user_groups = api.groups.get(user_id=vk_id)['items']
    x = dict.fromkeys(user_groups, 1)
    _X = vectorizer.transform(x)

    return dict(zip(classifier.classes_, classifier.predict_proba(_X)[0]))
