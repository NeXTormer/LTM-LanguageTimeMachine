for file in *.epub; do pandoc -s "$file" -o "/Volumes/Extreme SSD/TXT/${file}.txt"; echo $file; done

