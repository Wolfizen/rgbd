#!/bin/sh

export PYTHONPATH="$(pwd)"
./daemon/rgbd "$@" --test