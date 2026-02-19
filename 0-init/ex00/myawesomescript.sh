#!/bin/sh
curl --head --silent "$1" | 
grep --max-count=1 "Location:" | 
cut --delimiter=' ' --fields=2