#!/bin/sh

BINPATH=`dirname $0`
python=python
${python} "$BINPATH/../minja" $@

