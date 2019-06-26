#!/bin/sh


#SBATCH -J cobaya
#SBATCH -n 4
#SBATCH -c 12
#SBATCH -p dpt
####SCH -p dpt,mono-shared
#SBATCH -t 11:00:00
#TCH -t 23:50:00
#TCH --constraint="V3|V4|V5|V6|V7"

#export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load foss/2018b
module load Python/3.3.6
module load intel

. ~/cobenv/bin/activate

#srun cobaya-run rtMP.yaml -f -d | tee stdout.txt
#srun cobaya-run -r rtgen.yaml | tee stdout.txt
srun cobaya-run -r rtmin.yaml | tee stdout.txt


