#!/bin/bash

# Generate a random delay between 1 and 5 seconds
DELAY=$(awk 'BEGIN{srand();print int(rand()*4)+1}')
sleep "$DELAY"

# Add all the arguments
sum=0
for arg in "$@"
do
  sum=$(expr "$sum" + "$arg")
done

# Return the result
echo "$sum"

