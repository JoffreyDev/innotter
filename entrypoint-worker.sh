#!/bin/bash
poetry run celery -A innotter worker -l info