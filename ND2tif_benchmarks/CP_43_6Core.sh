#!/bin/bash

start1=`date +%s%N`

cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 0 -l 48 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 49 -l 97 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 98 -l 146 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 147 -l 195 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 196 -l 244 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 245 -l 300

wait
end1=`date +%s%N`
runtime1=$((end1-start1))
echo $runtime1
echo "done"
