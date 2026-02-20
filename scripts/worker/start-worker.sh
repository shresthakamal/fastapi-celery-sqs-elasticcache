#!/bin/bash

celery -A app.celery:app worker --loglevel=info