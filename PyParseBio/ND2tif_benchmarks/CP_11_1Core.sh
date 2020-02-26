#!/bin/bash
start=`date +%s%N`

cellprofiler -c -r -p CP_11_Batch_data.h5 -o datasets/output_CP #-f 0 -l 11

wait

end=`date +%s%N`
runtime=$((end-start))
echo "done"
echo $runtime