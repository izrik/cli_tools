#!/bin/bash

pip uninstall "$@" $(pip freeze | cut -d= -f1)

