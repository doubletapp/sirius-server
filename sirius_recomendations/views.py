# -*- coding: utf-8 -*-
import os
import subprocess

from django.http import HttpResponse


def recommend_achievements(request):
    params = dict(request.GET.items())
    user_id = params.get('user_id')
    achievements = params.get('achievements')
    dir_path = os.path.dirname(__file__)

    r = subprocess.Popen(
        "python2 %s %s %s" % (os.path.join(dir_path, 'recomendator.py'), user_id, achievements or '[]'),
        shell=True, stdout=subprocess.PIPE).stdout.read()

    return HttpResponse(r, content_type='application/json; charset=utf-8')
