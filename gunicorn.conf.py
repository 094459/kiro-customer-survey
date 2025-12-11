# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

"""Gunicorn configuration."""

bind = "0.0.0.0:8000"
workers = 2
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
