#!/bin/bash
start=`date +%s%N`

cellprofiler -c -r -p CP_43_Batch_data.h5 -o datasets/output_CP

wait

end=`date +%s%N`
runtime=$((end-start))
echo "done"
echo $runtime