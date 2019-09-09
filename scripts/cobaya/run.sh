#!/bin/sh


#SBATCH -J cobaya
#SBATCH -n 4
#SBATCH -c 12
#SBATCH -p dpt-EL7,mono-shared-EL7
####TCH -p dpt,mono-shared
#SBATCH -t 11:50:00
####TCH --constraint="V3|V4|V5|V6|V7"

#export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load foss/2018b
module load Python/3.6.6
module load intel

. ~/cobenv/bin/activate

#srun cobaya-run rtMP.yaml -f -d | tee stdout.txt

# remove -r (resume) for first run. add -f (force) for overwriting exising folder. 
srun cobaya-run -r rtmin.yaml | tee stdout.txt


