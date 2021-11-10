#!/usr/bin/perl -w
use strict;
use warnings;
use Net::SSH::Perl;
use SonusQA::ATSHELPER;
use SonusQA::LISERVER;
use SonusQA::TSHARK;
use Data::Dumper;
my $sippobj = SonusQA::ATSHELPER::newFromAlias(
		-tms_alias      => "BATS20SIPPSB_SB",
		-ignore_xml     => 0,
		-sessionLog     => 1,
		-iptype         => 'any',
		-return_on_fail => 1,
		);
$sippobj->{ CMDERRORFLAG } = 0;
        my %scpArgs;

                $scpArgs{-hostuser} ="linuxadmin";
                $scpArgs{-hostpasswd} = "sonus";
                $scpArgs{-scpPort} = '2024';
                $scpArgs{-hostip} = "10.52.24.233";
                $scpArgs{-destinationFilePath} = "/home/linuxadmin";
                $scpArgs{-sourceFilePath} = "/home/bshwetha/pesq_results.txt";

                unless(&SonusQA::Base::secureCopy(%scpArgs)){
                print("Unable to copy source file from local Server to SBC");

  }

