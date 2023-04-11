#!/usr/bin/perl

use strict;
use warnings;
use File::Basename;

# Extract the parent span context from the environment
my $parent_span_context = {
    trace_id => $ENV{OTEL_TRACE_ID},
    span_id => $ENV{OTEL_PARENT_SPAN_ID},
    is_remote => 1,
};

# Start a new span
my $span_id = `uuidgen`;
chomp($span_id);
my $span_context = {
    trace_id => $ENV{OTEL_TRACE_ID},
    span_id => $span_id,
    is_remote => 0,
};

# Add the delay
sleep int(rand(3));

# Get the three input numbers
my $num1 = $ARGV[0];
my $num2 = $ARGV[1];
my $num3 = $ARGV[2];

# Add the first two numbers
my $sum = $num1 + $num2;

my $cwd = dirname($0);

# Call the multiply.sh script
my $result = `OTEL_PARENT_SPAN_ID=$span_id bash ${cwd}/../bash-cli/multiply.sh $sum $num3`;

# Set the span status based on the result
if ($result == 0) {
    $ENV{OTEL_STATUS_CODE} = "ERROR";
} else {
    $ENV{OTEL_STATUS_CODE} = "OK";
}

# Log the span
print "SPAN $span_id add $result $ENV{OTEL_STATUS_CODE}\n";

# Print the result
print $result;
