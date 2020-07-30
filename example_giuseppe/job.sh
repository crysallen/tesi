#!/bin/bash
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=48
#SBATCH --cpus-per-task=1
#SBATCH --time=0:59:00
#SBATCH --output=job.out
#SBATCH --account=Sis20_baroni
#SBATCH --partition=skl_usr_prod
#SBATCH --job-name=sil
#SBATCH --mail-user=afiorent@sissa.it
##SBATCH --mail-type=ALL
cd /marconi_scratch/userexternal/afiorent/examples_local/8_example_512
python3 calculate_phonons.py
#python3 ald.py
#python3 prova.py
