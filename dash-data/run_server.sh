#!/bin/bash

# Starts a simple webserver that hosts the DASH files.
twistd -n web -p 8000 --path=. 
