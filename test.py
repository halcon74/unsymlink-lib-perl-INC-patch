#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pieces of Michal Gorny's code
# from https://github.com/mgorny/unsymlink-lib
# ============================
# SYMLINK_LIB=no migration tool
# (c) 2017 Michal Gorny
# Licensed under 2-clause BSD license
# ============================

# Why this file?
#
# For testing the addition of 'perl5' to conditions
# of remaining in /usr/local/lib64
# (
# replacing
# if path in (b'locale',):
# with
# if path in (b'locale', b'perl5',):
# )
#
# Currently, unsymlink-lib --analyze is showing:
# orphan dirs/files (not owned by any package) that will be moved to /usr/local/lib/:
#        .keep
#        perl5
# And after the migration to 17.1 profile I have to run manually
# mv /usr/local/lib/perl5 /usr/local/lib64
# for restoring the functionality of perl modules, installed manually or via CPAN
#
# ALL the directories in which perl5 is looking for the installed modules, are listed in the perl environment variable @INC
# that can be seen with:
# for i in $(perl -e '@inc = sort {$a cmp $b} @INC; print qq(@inc)'); do echo $i; done
# An example of output:
# /etc/perl
# /usr/lib64/perl5/5.30.3
# /usr/lib64/perl5/5.30.3/x86_64-linux
# /usr/lib64/perl5/vendor_perl
# /usr/lib64/perl5/vendor_perl/5.30.3
# /usr/lib64/perl5/vendor_perl/5.30.3/x86_64-linux
# /usr/local/lib64/perl5
# /usr/local/lib64/perl5/5.30.3
# /usr/local/lib64/perl5/5.30.3/x86_64-linux
# ('lib64' only, no 'lib')
#
# The output of this file:
# orphan dirs/files (not owned by any package) that will be moved... somewhere
#        .keep
#
#orphan dirs/files (not owned by any package) that will be kept... somewhere
#        perl5
#
# So, the test is successful

import os
import os.path
import sys

if sys.hexversion >= 0x03050000:
    decode_error_handler = 'backslashreplace'
else:
    decode_error_handler = 'replace'

def decode(value):
    if isinstance(value, bytes):
        return value.decode('utf-8', errors=decode_error_handler)
    return value

def _log(template, *args, **kwargs):
    print(
        template.format(*(decode(arg) for arg in args)),
        **kwargs
    )

def log(template, *args, **kwargs):
    kwargs['file'] = sys.stderr
    _log(template, *args, **kwargs)

def is_lib64_candidate(path):
    if os.path.splitext(path)[1] in (b'.a', b'.chk', b'.la', b'.so'):
        return True
    if b'.so.' in path:
        return True
    if path in (b'locale', b'perl5'):
        return True
    return False

mylist = [b'.keep', b'perl5']
unowned_files = frozenset(mylist)

# library symlinks go to lib64
lib64_unowned = frozenset(x for x in unowned_files
                           if is_lib64_candidate(x))
lib_unowned = unowned_files - lib64_unowned

if lib_unowned:
    log('')
    log('orphan dirs/files (not owned by any package) that will be moved... somewhere')
    for p in sorted(lib_unowned):
        log('\t{}', p)

if lib64_unowned:
    log('')
    log('orphan dirs/files (not owned by any package) that will be kept... somewhere')
    for p in sorted(lib64_unowned):
        log('\t{}', p)
