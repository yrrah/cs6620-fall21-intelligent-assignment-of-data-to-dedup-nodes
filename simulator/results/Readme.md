Experiments were grouped arbitrarily into collections of about 50 simulator runs with various parameters.    
The notations "ex0-####, ex1-####, etc" don't have any specific correlation to any run parameters. They are just the order we did the work in.   

Each run configuration generated a csv file. The csv files are named with a run number followed by a unix timestamp. The run number is a unique collection of run parameters.   
ex#-run#[timestamp].csv


Datasets were assigned numbers after-the-fact, when we were analyzing data.    

The csv file will have something like this   
`,,,,,,,,,SIMULATOR_TRACES_LISTS:fslhomes_2011-8kb-only_018,fslhomes_2012-8kb-only_018`

Dataset 1 = "fslhomes_2011-8kb-only_018,fslhomes_2012-8kb-only_018"   
Dataset 2 = "fslhomes_2011-8kb-only_014018019"   
Dataset 3 = "fslhomes_2011-8kb-only_014018019028,fslhomes_2012-8kb-only_014018019028"   

These file names refer to text files in this directory `simulator/front_end/src/traces`.   
Each one has a list of archive files to be downloaded from the tracer.filesystems.org website. The simulator downloads them at run time if they are not already cached.

`simulator/results/summary/combined_summary_stats.csv` has a combined summary of all the results.   
