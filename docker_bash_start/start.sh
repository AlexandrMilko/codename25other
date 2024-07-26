#!/bin/bash

# Run startsd.sh in the background
./startsd.sh &

# Run startapp.sh in the background
./startapp.sh &

# Wait for both background processes to finish
wait
