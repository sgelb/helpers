#!/bin/bash

# Change console fontsize 

# exit if any statement returns non-true
# if we don't care, use: command || true 
set -o errexit

# exit script if using unset variable
set -o nounset

default=`grep "^[^#]*font: " ~/.Xdefaults | sed 's/^.*font: //g'`

if [ $# -ne 1 ]; then
    echo "Reset to .Xdefaults"
    printf '\33]50;%s%d\007' "${default}"
elif [[ $1 =~ ^[0-9]*$ ]]; then
    new=`echo ${default} | sed -e s/size=[0-9]*/size=$1/g`
    printf '\33]50;%s%d\007' "${new}"
else
    echo "Invalid argument"
fi
