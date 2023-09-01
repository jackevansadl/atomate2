import pytest
from pymatgen.core import Structure

from atomate2.vasp.flows.mp import MPMetaGGARelaxMaker, MPMetaGGAStaticMaker

expected_incar = {
    "ISIF": 3,
    "IBRION": 2,
    "NSW": 99,
    "ISMEAR": 0,
    "SIGMA": 0.05,
    "LREAL": False,
    "LWAVE": False,
    "LCHARG": True,
    "EDIFF": 1e-05,
    "EDIFFG": -0.02,
    "GGA": "PS",
}


def test_mp_meta_gga_static_maker(mock_vasp, clean_dir, vasp_test_dir):
    from emmet.core.tasks import TaskDoc
    from jobflow import run_locally

    # map from job name to directory containing reference output files
    ref_paths = {
        "MP meta-GGA static": "Si_mp_metagga_relax/r2scan_final_static",
    }
    si_struct = Structure.from_file(
        f"{vasp_test_dir}/Si_mp_metagga_relax/r2scan_final_static/inputs/POSCAR"
    )

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {
        key: {"incar_settings": ["LWAVE", "LCHARG"]} for key in ref_paths
    }

    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # generate flow
    job = MPMetaGGAStaticMaker().make(si_struct)  # , bandgap=0.8249

    # ensure flow runs successfully
    responses = run_locally(job, create_folders=True, ensure_success=True)

    # validate output
    output = responses[job.uuid][1].output
    assert isinstance(output, TaskDoc)
    assert output.output.energy == pytest.approx(-10.85043620)


def test_mp_meta_gga_relax_maker(mock_vasp, clean_dir, vasp_test_dir):
    from emmet.core.tasks import TaskDoc
    from jobflow import run_locally

    # map from job name to directory containing reference output files
    ref_paths = {
        "MP meta-GGA relax": "Si_mp_metagga_relax/r2scan_relax",
    }
    si_struct = Structure.from_file(
        f"{vasp_test_dir}/Si_mp_metagga_relax/r2scan_final_static/inputs/POSCAR"
    )

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {
        key: {"incar_settings": ["LWAVE", "LCHARG"]} for key in ref_paths
    }

    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # generate flow
    job = MPMetaGGARelaxMaker().make(si_struct)

    # ensure flow runs successfully
    responses = run_locally(job, create_folders=True, ensure_success=True)

    # validate output
    output = responses[job.uuid][1].output
    print(f"{output.output.bandgap=}")
    assert isinstance(output, TaskDoc)
    assert output.output.energy == pytest.approx(-46.86703814)
