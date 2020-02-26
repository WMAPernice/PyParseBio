#!/bin/bash
start=`date +%s%N`

cellprofiler -c -r -p CP_11_Batch_data.h5 -o datasets/output_CP -f 0 -l 13 &
cellprofiler -c -r -p CP_11_Batch_data.h5 -o datasets/output_CP -f 14 -l 27 &
cellprofiler -c -r -p CP_11_Batch_data.h5 -o datasets/output_CP -f 28 -l 41 &
cellprofiler -c -r -p CP_11_Batch_data.h5 -o datasets/output_CP -f 42 -l 55 &
cellprofiler -c -r -p CP_11_Batch_data.h5 -o datasets/output_CP -f 56 -l 69 &
cellprofiler -c -r -p CP_11_Batch_data.h5 -o datasets/output_CP -f 70 -l 76

wait

end=`date +%s%N`
runtime=$((end-start))
echo "done"
echo $runtime