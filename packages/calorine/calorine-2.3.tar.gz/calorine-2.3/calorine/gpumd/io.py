from warnings import warn
from collections.abc import Iterable
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np
from ase import Atoms
from ase.io import read, write
from pandas import DataFrame


def read_kappa(filename: str) -> DataFrame:
    """Parses a file in ``kappa.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found `here
    <https://gpumd.org/gpumd/output_files/kappa_out.html>`__.

    Parameters
    ----------
    filename
        Input file name.
    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in kappa.out, append a dimension
        data = data.reshape(1, -1)
    tags = 'kx_in kx_out ky_in ky_out kz_tot'.split()
    if len(data[0]) != len(tags):
        raise ValueError(
            f'Input file contains {len(data[0])} data columns.'
            f' Expected {len(tags)} columns.'
        )
    df = DataFrame(data=data, columns=tags)
    df['kx_tot'] = df.kx_in + df.kx_out
    df['ky_tot'] = df.ky_in + df.ky_out
    return df


def read_hac(filename: str) -> DataFrame:
    """Parses a file in ``hac.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found `here
    <https://gpumd.org/gpumd/output_files/hac_out.html>`__.

    Parameters
    ----------
    filename
        Input file name.
    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in hac.out, append a dimension
        data = data.reshape(1, -1)
    tags = 'time'
    tags += ' jin_jtot_x jout_jtot_x jin_jtot_y jout_jtot_y jtot_jtot_z'
    tags += ' kx_in kx_out ky_in ky_out kz_tot'
    tags = tags.split()
    if len(data[0]) != len(tags):
        raise ValueError(
            f'Input file contains {len(data[0])} data columns.'
            f' Expected {len(tags)} columns.'
        )
    df = DataFrame(data=data, columns=tags)
    df['kx_tot'] = df.kx_in + df.kx_out
    df['ky_tot'] = df.ky_in + df.ky_out
    # remove columns with less relevant data to save space
    for col in df:
        if 'jtot' in col or '_in' in col:
            del df[col]
    return df


def read_thermo(filename: str, natoms: int = 1) -> DataFrame:
    """Parses a file in ``thermo.out`` format from GPUMD and returns the
    content as a data frame. More information concerning file format,
    content and units can be found `here
    <https://gpumd.org/gpumd/output_files/thermo_out.html>`__.

    Parameters
    ----------
    filename
        Input file name.
    natoms
        Number of atoms; used to normalize energies.
    """
    data = np.loadtxt(filename)
    if isinstance(data[0], np.float64):
        # If only a single row in loss.out, append a dimension
        data = data.reshape(1, -1)
    if len(data[0]) == 9:
        # orthorhombic box
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz'
        tags += ' cell_xx cell_yy cell_zz'
    elif len(data[0]) == 12:
        # orthorhombic box with stresses in Voigt notation (v3.3.1+)
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz stress_yz stress_xz stress_xy'
        tags += ' cell_xx cell_yy cell_zz'
    elif len(data[0]) == 15:
        # triclinic box
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz'
        tags += (
            ' cell_xx cell_xy cell_xz cell_yx cell_yy cell_yz cell_zx cell_zy cell_zz'
        )
    elif len(data[0]) == 18:
        # triclinic box with stresses in Voigt notation (v3.3.1+)
        tags = 'temperature kinetic_energy potential_energy'
        tags += ' stress_xx stress_yy stress_zz stress_yz stress_xz stress_xy'
        tags += (
            ' cell_xx cell_xy cell_xz cell_yx cell_yy cell_yz cell_zx cell_zy cell_zz'
        )
    else:
        raise ValueError(
            f'Input file contains {len(data[0])} data columns.'
            ' Expected 9, 12, 15 or 18 columns.'
        )
    df = DataFrame(data=data, columns=tags.split())
    assert natoms > 0, 'natoms must be positive'
    df.kinetic_energy /= natoms
    df.potential_energy /= natoms
    return df


def read_xyz(filename: str) -> Atoms:
    """
    Reads the structure input file (``model.xyz``) for GPUMD and returns the
    structure.

    This is a wrapper function around :func:`ase.io.read_xyz` since the ASE implementation does
    not read velocities properly.

    Parameters
    ----------
    filename
        Name of file from which to read the structure.

    Returns
    -------
        Structure as ASE Atoms object with additional per-atom arrays
        representing atomic masses, velocities etc.
    """
    structure = read(filename, format='extxyz')
    if structure.has('vel'):
        structure.set_velocities(structure.get_array('vel'))
    return structure


def read_runfile(filename: str) -> List[Tuple[str, list]]:
    """
    Parses a GPUMD input file in ``run.in`` format and returns the
    content in the form a list of keyword-value pairs.

    Parameters
    ----------
    filename
        Input file name.

    Returns
    -------
        List of keyword-value pairs.
    """
    data = []
    with open(filename, 'r') as f:
        for k, line in enumerate(f.readlines()):
            flds = line.split()
            if len(flds) == 0:
                continue
            elif len(flds) == 1:
                raise ValueError(f'Line {k} contains only one field:\n{line}')
            keyword = flds[0]
            values = tuple(flds[1:])
            if keyword in ['time_step', 'velocity']:
                values = float(values[0])
            elif keyword in ['dump_thermo', 'dump_position', 'dump_restart', 'run']:
                values = int(values[0])
            elif len(values) == 1:
                values = values[0]
            data.append((keyword, values))
    return data


def write_runfile(
    file: Path, parameters: List[Tuple[str, Union[int, float, Tuple[str, float]]]]
):
    """Write a file in run.in format to define input parameters for MD simulation.

    Parameters
    ----------
    file
        Path to file to be written.

    parameters : dict
        Defines all key-value pairs used in run.in file
        (see GPUMD documentation for a complete list).
        Values can be either floats, integers, or lists/tuples.
    """

    with open(file, 'w') as f:
        # Write all keywords with parameter(s)
        for key, val in parameters:
            f.write(f'{key} ')
            if isinstance(val, Iterable) and not isinstance(val, str):
                for v in val:
                    f.write(f'{v} ')
            else:
                f.write(f'{val}')
            f.write('\n')


def write_xyz(filename: str, structure: Atoms, groupings: List[List[List[int]]] = None):
    """
    Writes a structure into GPUMD input format (`model.xyz`).

    Parameters
    ----------
    filename
        Name of file to which the structure should be written.
    structure
        Input structure.
    groupings
        Groups into which the individual atoms should be divided in the form of
        a list of list of lists. Specifically, the outer list corresponds to
        the grouping methods, of which there can be three at the most, which
        contains a list of groups in the form of lists of site indices. The
        sum of the lengths of the latter must be the same as the total number
        of atoms.

    Raises
    ------
    ValueError
        Raised if parameters are incompatible.
    """
    # Make a local copy of the atoms object
    _structure = structure.copy()

    # Check velocties parameter
    velocities = _structure.get_velocities()
    if velocities is None or np.max(np.abs(velocities)) < 1e-6:
        has_velocity = 0
    else:
        has_velocity = 1

    # Check groupings parameter
    if groupings is None:
        number_of_grouping_methods = 0
    else:
        number_of_grouping_methods = len(groupings)
        if number_of_grouping_methods > 3:
            raise ValueError('There can be no more than 3 grouping methods!')
        for g, grouping in enumerate(groupings):
            all_indices = [i for group in grouping for i in group]
            if len(all_indices) != len(_structure) or set(all_indices) != set(
                range(len(_structure))
            ):
                raise ValueError(
                    f'The indices listed in grouping method {g} are'
                    ' not compatible with the input structure!'
                )

    # Allowed keyword=value pairs. Use ASEs extyz write functionality.
    #   pbc="pbc_a pbc_b pbc_c"
    #   lattice="ax ay az bx by bz cx cy cz"
    #   properties=property_name:data_type:number_of_columns
    #       species:S:1
    #       pos:R:3
    #       mass:R:1
    #       vel:R:3
    #       group:I:number_of_grouping_methods
    if _structure.has('mass'):
        # If structure already has masses set, use those
        warn('Structure already has array "mass"; will use existing values.')
    else:
        _structure.new_array('mass', _structure.get_masses())

    if has_velocity:
        _structure.new_array('vel', _structure.get_velocities())
    if groupings is not None:
        group_indices = np.array(
            [
                [
                    [
                        group_index
                        for group_index, group in enumerate(grouping)
                        if structure_idx in group
                    ]
                    for grouping in groupings
                ]
                for structure_idx in range(len(_structure))
            ]
        ).squeeze()  # pythoniccc
        _structure.new_array('group', group_indices)

    write(filename=filename, images=_structure, write_info=True, format='extxyz')


def read_mcmd(filename: str, accumulate: bool = True) -> DataFrame:
    """Parses a Monte Carlo output file in ``mcmd.out`` format
    and returns the content in the form of a DataFrame.

    Parameters
    ----------
    filename
        Path to file to be parsed.
    accumulate
        If ``True`` the MD steps between subsequent Monte Carlo
        runs in the same output file will be accumulated.

    Returns
    -------
        DataFrame containing acceptance ratios and concentrations (if available),
        as well as key Monte Carlo parameters.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    data = []
    offset = 0
    step = 0
    accummulated_step = 0
    for line in lines:
        if line.startswith('# mc'):
            flds = line.split()
            mc_type = flds[2]
            md_steps = int(flds[3])
            mc_trials = int(flds[4])
            temperature_initial = float(flds[5])
            temperature_final = float(flds[6])
            if mc_type.endswith('sgc'):
                ntypes = int(flds[7])
                species = [flds[8+2*k] for k in range(ntypes)]
                phis = {f'phi_{flds[8+2*k]}': float(flds[9+2*k]) for k in range(ntypes)}
            kappa = float(flds[8+2*ntypes]) if mc_type == 'vcsgc' else np.nan
        elif line.startswith('# num_MD_steps'):
            continue
        else:
            flds = line.split()
            previous_step = step
            step = int(flds[0])
            if step <= previous_step and accumulate:
                offset += previous_step
            accummulated_step = step + offset
            record = dict(
                step=accummulated_step,
                mc_type=mc_type,
                md_steps=md_steps,
                mc_trials=mc_trials,
                temperature_initial=temperature_initial,
                temperature_final=temperature_final,
                acceptance_ratio=float(flds[1]),
            )
            if mc_type.endswith('sgc'):
                record.update(phis)
                if mc_type == 'vcsgc':
                    record['kappa'] = kappa
                concentrations = {f'conc_{s}': float(flds[k])
                                  for k, s in enumerate(species, start=2)}
                record.update(concentrations)
            data.append(record)
    df = DataFrame.from_dict(data)
    return df
