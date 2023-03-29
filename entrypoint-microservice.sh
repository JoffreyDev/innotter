#!/bin/bash
poetry run uvicorn innotter.microservice.main:app --host 0.0.0.0 --port 8001 --reload --reload-dir /innotter

