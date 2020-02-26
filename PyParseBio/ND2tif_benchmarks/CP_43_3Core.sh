#!/bin/bash

start1=`date +%s%N`
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 0 -l 97 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 98 -l 195 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 196 -l 300
wait
end1=`date +%s%N`
runtime1=$((end1-start1))
echo $runtime1

start2=`date +%s%N`
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 0 -l 97 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 98 -l 195 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 196 -l 300
wait
end2=`date +%s%N`
runtime2=$((end2-start2))
echo $runtime2

start3=`date +%s%N`
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 0 -l 97 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 98 -l 195 &
cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP -f 196 -l 300
wait
end3=`date +%s%N`
runtime3=$((end3-start3))
echo $runtime3

echo "done"
echo $runtime1
echo $runtime2
echo $runtime3