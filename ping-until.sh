$!/bin/bash

while ! ping -c 1 8.8.8.8 ; do
  sleep 1
done
say ready

