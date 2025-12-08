#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Copyright (2026) Beachgeek.co.uk
# Author: Ricardo Sueiras
# Apache 2.0 license

cd "$(dirname "$0")"
PYTHONPATH=$(pwd) uv run pytest "$@"
