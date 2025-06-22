#!/bin/bash

RESOLUTIONS=(
    48
    72
    96
    144
    168
    180
    192
    256
    384
    512
)

for res in "${RESOLUTIONS[@]}"; do
    convert "icon.png" -resize "${res}x${res}" "icon${res}.png"
done