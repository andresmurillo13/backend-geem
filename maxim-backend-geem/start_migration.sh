#!/usr/bin/env bash
export $(cat /home/ubuntu/geem/maxim-backend-geem/.env | sed -e /^$/d -e /^#/d | xargs)
cd /home/ubuntu/geem/maxim-backend-geem && /home/ubuntu/geem/venv/bin/python migration.py
