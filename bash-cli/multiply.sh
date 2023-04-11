#!/bin/bash

# Create a new span
OTEL_TRACE_ID=$(cat /proc/sys/kernel/random/uuid)
OTEL_SPAN_ID=$(cat /proc/sys/kernel/random/uuid)
OTEL_PARENT_SPAN_ID=$(cat /proc/sys/kernel/random/uuid)
OTEL_TRACE_FLAG=1
OTEL_TRACE_EXPORTER_ENDPOINT=http://localhost:55680/v1/traces
OTEL_SERVICE_NAME=multiply

# Propagate the span context via environment variables
export OTEL_TRACE_ID OTEL_SPAN_ID OTEL_PARENT_SPAN_ID OTEL_TRACE_FLAG OTEL_TRACE_EXPORTER_ENDPOINT OTEL_SERVICE_NAME

# Add a delay
sleep $(awk -v min=0 -v max=2 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')

# Multiply the two numbers
result=$(($1 * $2))

# Set the span status based on the result
if [ $result -eq 0 ]; then
  export OTEL_STATUS_CODE=ERROR
else
  export OTEL_STATUS_CODE=OK
fi

# Log the span
echo "SPAN $OTEL_SPAN_ID $OTEL_SERVICE_NAME $result $OTEL_STATUS_CODE"

# Return the result
echo $result
