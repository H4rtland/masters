#! /bin/bash -f

echo "Job $1"

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh

WORKDIR=/home/atlas/thartland/masters/week11

cd ${WORKDIR}

lsetup root

source /home/atlas/thartland/venvs/root-py2/bin/activate

python limit_dist.py "$1"
