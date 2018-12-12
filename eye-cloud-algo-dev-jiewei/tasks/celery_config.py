# -*- coding: utf-8 -*-

from celery import Celery

celery = Celery(
                'tasks', \
                backend='redis://localhost:6379/0', \
                broker='redis://localhost:6379/0', \
                include=['tasks.test', 'tasks.fundusImage', 'tasks.surfaceImage'] \
        )

