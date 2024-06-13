#!/bin/bash
#
# STFU Tensorflow
# https://spacecruft.org/deepcrayon/sndid/issues/12
#
# Temporary workaround to silence Tensorflow

sndid-list "$@" {tmp}>&1 1>&2 2>&$tmp {tmp}>&- | \
  grep -v \
  -e 'INFO: Created TensorFlow Lite XNNPACK delegate for CPU.' 

