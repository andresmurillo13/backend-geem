#!/usr/bin/env bash
export $(cat .env | sed -e /^$/d -e /^#/d | xargs)
python consumer.py
