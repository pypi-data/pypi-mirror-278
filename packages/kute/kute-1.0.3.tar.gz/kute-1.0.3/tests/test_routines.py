# Copyright (c) 2024 The KUTE contributors

import os 
import pytest
import numpy as np
import kute.__main__
import sys



ACTUAL_PATH = os.path.split(os.path.join(os.path.abspath(__file__)))[0]

@pytest.fixture
def topo_file():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/topo.tpr")
    return file

@pytest.fixture
def traj_file():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/traj.trr")
    return file

@pytest.fixture
def current_file_h5():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/current_test.h5")
    return file

@pytest.fixture
def velocity_file_h5():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/com_velocity_test.h5")
    return file

@pytest.fixture
def pressure_file_h5():
    file = os.path.join(ACTUAL_PATH, "files_for_tests/inputs/pressure_tensor_test.h5")
    return file

class TestElectricConductivityRoutine(object):

    def test_run_one_analysis(self, topo_file, traj_file):

        from kute.routines._electric_conductivity import run_one_analysis

        run_one_analysis(topo_file, traj_file, "temporal_result.h5", verbose=False)

        assert os.path.isfile("temporal_result.h5")

        os.remove("temporal_result.h5")

    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_calculation_for_one(self, current_file_h5, splits):

        from kute.routines._electric_conductivity import calculation_for_one

        ## Create random weight for the test
        weight = np.array(np.random.random((1,1)))
        np.savetxt("weight_temp.dat", weight)

        t, avg, uavg = calculation_for_one(current_file_h5, splits, "weight_temp.dat")

        assert len(t) == len(avg)
        assert len(avg) == len(uavg)

        os.remove("weight_temp.dat")

    @pytest.mark.parametrize("splits,repetitions", [(1, 5), (2, 5), (10, 5), (1, 10), (2, 10), (10, 10)])
    def test_calculation_for_ensemble(self, current_file_h5, splits, repetitions):

        from kute.routines._electric_conductivity import calculation_for_ensemble

        weight = np.random.random(repetitions)
        np.savetxt("weight_temp.dat", weight)

        t, avg, uavg = calculation_for_ensemble([current_file_h5 for _ in range(repetitions)], splits, "weight_temp.dat")

        assert len(t) == len(avg)
        assert len(avg) == len(uavg)

        os.remove("weight_temp.dat")

    @pytest.mark.parametrize("number", [100, 500, 1000])
    def test_save_results(self, number):
    
        from kute.routines._electric_conductivity import save_results

        t, avg, uavg = np.random.random((3, number))
        save_results("temporal.dat", t, avg, uavg)

        assert os.path.isfile("temporal.dat")

        os.remove("temporal.dat")

    @pytest.mark.parametrize("splits,repetitions", [(1, 5), (2, 5), (10, 5), (1, 10), (2, 10), (10, 10)])
    def test_commandline_function(self, current_file_h5, splits, repetitions):

        file_list = " ".join([current_file_h5 for _ in range(repetitions)])
        print(file_list)
        command = f"kute electric_conductivity -f {file_list} --splits {splits} -o temporary_out.dat"
        sys.argv = command.split()

        kute.__main__.main()

        assert os.path.isfile("temporary_out.dat")
        os.remove("temporary_out.dat")


class TestViscosityRoutine(object):

    def test_run_one_analysis(self, topo_file, traj_file):

        from kute.routines._viscosity import run_one_analysis

        run_one_analysis(topo_file, traj_file, "temporal_result.h5", verbose=False)

        assert os.path.isfile("temporal_result.h5")

        os.remove("temporal_result.h5")

    @pytest.mark.parametrize("splits", [1, 2, 5, 10])
    def test_calculation_for_one(self, pressure_file_h5, splits):

        from kute.routines._viscosity import calculation_for_one

        ## Create random weight for the test
        weight = np.array(np.random.random((1,1)))
        np.savetxt("weight_temp.dat", weight)

        t, avg, uavg = calculation_for_one(pressure_file_h5, splits, "weight_temp.dat")

        assert len(t) == len(avg)
        assert len(avg) == len(uavg)

        os.remove("weight_temp.dat")

    @pytest.mark.parametrize("splits,repetitions", [(1, 5), (2, 5), (10, 5), (1, 10), (2, 10), (10, 10)])
    def test_calculation_for_ensemble(self, pressure_file_h5, splits, repetitions):
            
            from kute.routines._viscosity import calculation_for_ensemble
    
            weight = np.random.random(repetitions)
            np.savetxt("weight_temp.dat", weight)
    
            t, avg, uavg = calculation_for_ensemble([pressure_file_h5 for _ in range(repetitions)], splits, "weight_temp.dat")
    
            assert len(t) == len(avg)
            assert len(avg) == len(uavg)
    
            os.remove("weight_temp.dat")

    @pytest.mark.parametrize("number", [100, 500, 1000])
    def test_save_results(self, number):
        
            from kute.routines._viscosity import save_results
    
            t, avg, uavg = np.random.random((3, number))
            save_results("temporal.dat", t, avg, uavg)
    
            assert os.path.isfile("temporal.dat")
    
            os.remove("temporal.dat")

    @pytest.mark.parametrize("splits,repetitions", [(1, 5), (2, 5), (10, 5), (1, 10), (2, 10), (10, 10)])
    def test_commandline_function(self, pressure_file_h5, splits, repetitions):
            
            file_list = " ".join([pressure_file_h5 for _ in range(repetitions)])
            command = f"kute viscosity -f {file_list} --splits {splits} -o temporary_out.dat"
            sys.argv = command.split()
    
            kute.__main__.main()
    
            assert os.path.isfile("temporary_out.dat")
            os.remove("temporary_out.dat")


class TestDiffusionCoefficientRoutine(object):

    def test_run_one_analysis(self, topo_file, traj_file):

        from kute.routines._diffusion_coefficient import run_one_analysis

        run_one_analysis(topo_file, traj_file, "temporal_result.h5", verbose=False)

        assert os.path.isfile("temporal_result.h5")

        os.remove("temporal_result.h5")

    @pytest.mark.parametrize("splits,resname", [(1, "ea"), (1, "no3"), (10, "ea"), (10, "no3")])
    def test_calculation_for_one(self, velocity_file_h5, splits, resname):

        from kute.routines._diffusion_coefficient import calculation_for_one

        ## Create random weight for the test
        weight = np.array(np.random.random((1,1)))
        np.savetxt("weight_temp.dat", weight)

        t, avg, uavg = calculation_for_one(velocity_file_h5, splits, resname, "weight_temp.dat")

        assert len(t) == len(avg)
        assert len(avg) == len(uavg)

        os.remove("weight_temp.dat")

    @pytest.mark.parametrize("splits,repetitions,resname", [(1, 5, "ea"), (1, 5, "no3"), (10, 2, "ea"), (10, 2, "no3")])
    def test_calculation_for_ensemble(self, velocity_file_h5, splits, repetitions, resname):

        from kute.routines._diffusion_coefficient import calculation_for_ensemble

        weight = np.random.random(repetitions)
        np.savetxt("weight_temp.dat", weight)

        t, avg, uavg = calculation_for_ensemble([velocity_file_h5 for _ in range(repetitions)], splits, resname, "weight_temp.dat")

        assert len(t) == len(avg)
        assert len(avg) == len(uavg)

        os.remove("weight_temp.dat")

    @pytest.mark.parametrize("number", [100, 500, 1000])
    def test_save_results(self, number):
    
        from kute.routines._diffusion_coefficient import save_results

        t, avg, uavg = np.random.random((3, number))
        save_results("temporal.dat", t, avg, uavg)

        assert os.path.isfile("temporal.dat")

        os.remove("temporal.dat")

    @pytest.mark.parametrize("splits,repetitions,resname", [(1, 5, "ea"), (1, 5, "no3"), (10, 2, "ea"), (10, 2, "no3")])
    def test_commandline_function(self, velocity_file_h5, splits, repetitions, resname):

        file_list = " ".join([velocity_file_h5 for _ in range(repetitions)])
        command = f"kute diffusion_coefficient -f {file_list} --splits {splits} -o temporary_out.dat --resname {resname}"
        sys.argv = command.split()

        kute.__main__.main()

        assert os.path.isfile("temporary_out.dat")
        os.remove("temporary_out.dat")