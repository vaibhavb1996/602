#!/bin/sh

# Copyright 2018 Vaibhav Bansal vbansal@bu.edu
g++ fourargs.cpp -o fourargs
python fourargs.py one two 3 four five six
python fourargs.py one two 3
fourargs one two three 4 five 6
fourargs one two three 