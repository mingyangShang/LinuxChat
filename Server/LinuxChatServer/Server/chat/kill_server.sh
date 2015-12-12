#!/usr/bin/env bash
#kill all process using port 8888
kill $(lsof -i:8888 | awk ' $2 ~ /^[0-9]+$/ {print $2}')
