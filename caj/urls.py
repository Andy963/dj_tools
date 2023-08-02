#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: urls.py
# Author: Zhou
# Date: 2023/7/31
# Copyright: 2023 Zhou
# License:
# Description: caj urls
from django.urls import path

from caj.views import caj2pdf

urlpatterns = [
    path('', caj2pdf, name="index"),
]
