#!/bin/bash
a=$(ps aux | grep crawler.py | wc -l)
if [[ a -eq 1 ]]; then
  echo Executing cron job crawler.py
  python -B /home/kieutran/crawler.py >/home/kieutran/logs/crawler.stdout 2>>/h$
else
  echo Not executing cron job. crawler is already running.
fi