# Copyright (c) 2024 The KUTE contributors
import argparse
import numpy as np
import MDAnalysis as mda

from kute import GreenKuboIntegral, IntegralEnsemble
from kute.loaders import load_com_velocity
from kute.analysis import COMVelocity

def run_one_analysis(top, traj, filename, verbose=True):

    u = mda.Universe(top, traj)
    analysis = COMVelocity(universe=u, filename=filename)
    analysis.run(verbose=verbose)

def calculation_for_one(name, splits, resname, weight=None):
    
    if weight is not None:
        weight = np.loadtxt(weight)
    else:
        weight = 1

    t, Vx, Vy, Vz = load_com_velocity(name, resname, splits)
    integral = GreenKuboIntegral(t, Vx, Vy, Vz)
    tavg, avg, u_avg = integral.get_isotropic_running_average()

    avg *= weight
    u_avg *= weight

    return tavg, avg, u_avg

def calculation_for_ensemble(names, splits, resname, weights=None):

    if weights is not None:
        weights = np.loadtxt(weights)

    integrals = []
    for name in names:
        t, Vx, Vy, Vz = load_com_velocity(name, resname, splits)
        integrals.append(GreenKuboIntegral(t, Vx, Vy, Vz))
    
    ensemble = IntegralEnsemble(integrals, factors=weights)
    return ensemble.get_isotropic_average()


def save_results(out_file, tavg, avg, uavg):

    to_save = np.vstack([tavg, avg, uavg]).T
    np.savetxt(out_file, to_save, header="Time       Average         Uncertainty")


def main():

    description = 'Calculates the isotropic diffusion coefficient as a function of averaging cutoff'

    parser = argparse.ArgumentParser(description=description)

    ## Input arguments

    parser.add_argument("-f", required=False, type=str, dest="h5_files", metavar="current.h5", nargs="+", default=None,
                        help = ("List of h5 binary files containing the electric current for each replica."))

    
    parser.add_argument("--traj", required=False, type=str, dest="traj_files", metavar="traj.trr, traj.xtc", nargs="+",
                        help = ("List of trajectory files used to calculate the electric current. Note that they must contain velocities"))


    parser.add_argument("--topo", required=False, type=str, dest="topo_files", metavar="traj.tpr, data.lmp", nargs="+",
                        help = ("List of topology files used to calculate the electric current. They must contain, mass and residue information"))
    
    parser.add_argument("--resname", required=True, type=str, metavar="resname", dest="resname",
                        help=("Name of the residue for which to calculate the diffusion coefficient"))


    ## Calculation arguments

    parser.add_argument("--splits", required=False, type=int, dest="splits", metavar="slipts", default=1,
                        help = ("Number of fragments of equal size into which to split the center of mass velocities of each replica"))

    parser.add_argument("--weights", required=False, type=str, default=None, metavar="weights.dat", dest="weights", 
                        help=("File containing the weighting factor for each replica. Can be used to change units or to include replica-dependent values such as the volume."))

    ## Output arguments

    parser.add_argument("-o", required=False, type=str, dest="out_file", metavar="diffusion.dat", default="diffusion.dat",
                        help = ("Name of the output file"))
    

    args = parser.parse_args()


    ### Check if h5 file was given. If not, carry out the calcultions from the trajectories

    if args.h5_files is None:
        
        print("Didn't specify an h5 file. Falling back to current calculation from MD trajectories")
        for i, (top, traj) in enumerate(zip(args.topo_files, args.traj_files)):
            run_one_analysis(top, traj, f"com_velocity_from_traj_replica_{i+1}.h5")

        names = [ f"com_velocity_from_traj_replica_{i+1}.h5" for i in range(len(args.topo_files)) ]
    else:
        names = args.h5_files

    ### Carry out the Green-Kubo calculations

     ### Carry out the Green-Kubo calculations

    if len(names) == 1:
        tavg, avg, uavg = calculation_for_one(names[0], args.splits, args.resname, args.weights)
    
    else:
        tavg, avg, uavg = calculation_for_ensemble(names, args.splits, args.resname, args.weights)



    ## Save the results

    save_results(args.out_file, tavg, avg, uavg)



if __name__ == 'main':
    main()