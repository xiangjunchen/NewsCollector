#!/bin/bash
ps -ef | grep zhengwen | grep -v grep | awk  '{ print $2 }' | xargs -n 1 kill

