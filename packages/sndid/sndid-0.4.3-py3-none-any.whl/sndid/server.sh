#!/bin/bash
#
# STFU Tensorflow
# https://spacecruft.org/deepcrayon/sndid/issues/12
#
# Temporary workaround to silence Tensorflow
#
# If port in use, wait a few secs for timeout. To see, run:
# echo "netstat -pant | grep 9988"

sndid-server "$@" {tmp}>&1 1>&2 2>&$tmp {tmp}>&- | \
  grep -v \
  -e 'INFO: Created TensorFlow Lite XNNPACK delegate for CPU.'

