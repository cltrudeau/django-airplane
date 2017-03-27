#!/usr/bin/env python
import os, sys
from unittest import TestSuite

import django
from django.conf import settings

default_labels = ['airplane.tests', ]

def get_suite(labels=default_labels):
    #-- Configure Django
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'airplane'))

    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            'default':{
                'ENGINE':'django.db.backends.sqlite3',
            }
        },
        ROOT_URLCONF='airplane.tests.urls',
        MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.staticfiles',
            'awl',
            'awl.rankedmodel',
            'airplane',
            'airplane.tests',
        ),
        TEMPLATES = [{
            'BACKEND':'django.template.backends.django.DjangoTemplates',
            'DIRS':[
                os.path.abspath(os.path.join(BASE_DIR, 'airplane/templates')),
            ],
            'APP_DIRS':True,
            'OPTIONS': {
                'context_processors':[
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ]
            }
        }],
        STATIC_URL='/static/',
    )

    django.setup()

    #from django.core.management import call_command
    #call_command('shell')
    #quit()

    #-- Run Tests
    from awl.waelsteng import WRunner
    runner = WRunner(verbosity=1)
    failures = runner.run_tests(labels)
    if failures:
        sys.exit(failures)

    # in case this is called from setup tools, return a test suite
    return TestSuite()


if __name__ == '__main__':
    labels = default_labels
    if len(sys.argv[1:]) > 0:
        labels = sys.argv[1:]

    get_suite(labels)
