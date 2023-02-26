#!/bin/bash

#Ubicacion del script
script="/home/kallox/respaldo/thesis/dags/scripts/characterization/structural_characterization.py"
#Ubicacion del CSV
csv="/home/kallox/respaldo/thesis/dags/files/$1"
#Carpeta de salida
output="files/$2/salidas"
#Nombre del archivo de salida dentro de la carpeta
outputfile="result.csv"

folder="/home/kallox/respaldo/thesis/dags/$output"
rm -r $folder
mkdir $folder

lines=$(wc -l < $csv)
lines=$((lines))
lines=$((lines-1))

echo "name,sequence,database,ss8,ss3" >> "$folder/$outputfile"

for i in $(eval echo "{0..$lines..1000}")
do
    parallel -u "python3 $script $csv {.} $output" ::: $( seq $i $(($i+999)) ) >> "$folder/$outputfile"
done

exit 0