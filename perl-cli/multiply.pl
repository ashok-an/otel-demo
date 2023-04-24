#!/usr/bin/perl

use strict;
use warnings;

# Generate a random delay between 1 and 5 seconds
my $delay = int(rand(5)) + 1;
sleep $delay;

# Multiply all the arguments
my $product = 1;
foreach my $arg (@ARGV) {
  $product *= $arg;
}

# Return the result
print "$product\n";

