#!/usr/bin/env bash
export $(cat /home/ubuntu/geem/maxim-backend-geem/.env | sed -e /^$/d -e /^#/d | xargs)
cd /home/ubuntu/geem/maxim-backend-geem && /home/ubuntu/geem/venv/bin/uvicorn main:app --workers 2 --port 3004 --host 127.0.0.1
