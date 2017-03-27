#!/bin/bash

find . -name "*.pyc" -exec rm {} \;
rm db.sqlite3
