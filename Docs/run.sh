#!/bin/sh

npx @marp-team/marp-cli@latest *.md -o ./"Manual_$(date +%F)".pdf --allow-local-files

