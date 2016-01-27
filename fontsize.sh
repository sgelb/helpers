#!/bin/bash

# Change console fontsize 

# exit if any statement returns non-true
set -o errexit

# exit script if using unset variable
set -o nounset

default=$(grep "^[^#]*font: " ~/.Xresources | sed 's/^.*font: //g')

if [ $# -ne 1 ]; then
  echo "Setting font size to value set in .Xresources"
  printf '\33]50;%s%d\007' "${default}"
elif [[ $1 =~ ^[0-9]*$ ]]; then
  echo "Setting font size to ${1}"
  new=$(echo "${default}" | sed -e "s/\(size=\)[0-9]*/\1$1/")
  printf '\33]50;%s%d\007' "${new}"
else
  echo "Invalid argument"
fi
