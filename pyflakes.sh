#!/bin/bash

echo "============================================================"
echo "== pyflakes =="
pyflakes airplane | grep -v migration
