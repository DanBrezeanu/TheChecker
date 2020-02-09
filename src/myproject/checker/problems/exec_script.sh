#!/bin/bash

timeout --signal=SIGINT 5 $1
echo $? 