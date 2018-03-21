use strict;
use warnings;
die "<1 parameter>" unless @ARGV == 2;
my $direction = shift;
my $file =shift;

my $test = `df -lh`;

system("mkdir -p $direction");
open OUT,">$direction/$file" || die $!;
print OUT "$test";
close OUT;
