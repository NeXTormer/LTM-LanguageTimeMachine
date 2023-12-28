#!/bin/zsh

input_folder="/Users/felix/Developer/Jupyter/dump"
output_folder="/Volumes/Extreme SSD/TXT"

mkdir -p "$output_folder"

# Use find to get a list of all epub files in the input folder
find "$input_folder" -type f -name "*.epub" | parallel 'pandoc -s {} -o '"$output_folder"'/{/.}.txt && echo {}'
