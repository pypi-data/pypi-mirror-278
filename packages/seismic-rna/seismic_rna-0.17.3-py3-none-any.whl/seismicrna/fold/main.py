from datetime import datetime
from itertools import chain
from logging import getLogger
from pathlib import Path
from typing import Iterable

from click import command

from .report import FoldReport
from .rnastructure import ct2dot, fold, require_data_path
from ..core.arg import (CMD_FOLD,
                        docdef,
                        arg_input_path,
                        opt_tmp_dir,
                        opt_keep_tmp,
                        opt_fold_sections_file,
                        opt_fold_coords,
                        opt_fold_primers,
                        opt_fold_full,
                        opt_quantile,
                        opt_fold_temp,
                        opt_fold_constraint,
                        opt_fold_md,
                        opt_fold_mfe,
                        opt_fold_max,
                        opt_fold_percent,
                        opt_max_procs,
                        opt_parallel,
                        opt_force)
from ..core.extern import (RNASTRUCTURE_CT2DOT_CMD,
                           RNASTRUCTURE_FOLD_CMD,
                           require_dependency)
from ..core.parallel import as_list_of_tuples, dispatch, lock_tmp_dir
from ..core.rna import RNAProfile
from ..core.seq import DNA, RefSections, RefSeqs, Section
from ..table.base import MaskPosTable, ClustPosTable
from ..table.load import find_pos_tables, load_pos_table

logger = getLogger(__name__)

DEFAULT_QUANTILE = 0.95


def find_foldable_tables(input_path: Iterable[str | Path]):
    """ Find tables that can be folded. """
    for file in find_pos_tables(input_path):
        try:
            table = load_pos_table(file)
        except Exception as error:
            logger.error(f"Failed to load table from {file}: {error}")
        else:
            if isinstance(table, (ClustPosTable, MaskPosTable)):
                yield file, table


def fold_section(rna: RNAProfile,
                 out_dir: Path,
                 quantile: float,
                 fold_temp: float,
                 fold_constraint: Path | None,
                 fold_md: int,
                 fold_mfe: bool,
                 fold_max: int,
                 fold_percent: float,
                 force: bool,
                 n_procs: int,
                 **kwargs):
    """ Fold a section of an RNA from one mutational profile. """
    began = datetime.now()
    rna.to_varna_color_file(out_dir)
    ct_file = fold(rna,
                   out_dir=out_dir,
                   fold_temp=fold_temp,
                   fold_constraint=fold_constraint,
                   fold_md=fold_md,
                   fold_mfe=fold_mfe,
                   fold_max=fold_max,
                   fold_percent=fold_percent,
                   force=force,
                   n_procs=n_procs,
                   **kwargs)
    ct2dot(ct_file)
    ended = datetime.now()
    report = FoldReport(sample=rna.sample,
                        ref=rna.ref,
                        sect=rna.sect,
                        profile=rna.profile,
                        quantile=quantile,
                        fold_temp=fold_temp,
                        fold_md=fold_md,
                        fold_mfe=fold_mfe,
                        fold_max=fold_max,
                        fold_percent=fold_percent,
                        began=began,
                        ended=ended)
    return report.save(out_dir, force=force)


def fold_profile(table: MaskPosTable | ClustPosTable,
                 sections: list[Section],
                 quantile: float,
                 n_procs: int,
                 **kwargs):
    """ Fold an RNA molecule from one table of reactivities. """
    return dispatch(fold_section,
                    n_procs,
                    parallel=True,
                    hybrid=True,
                    pass_n_procs=True,
                    args=as_list_of_tuples(table.iter_profiles(
                        sections=sections, quantile=quantile)
                    ),
                    kwargs=dict(out_dir=table.top,
                                quantile=quantile,
                                **kwargs))


@lock_tmp_dir
@docdef.auto()
def run(input_path: tuple[str, ...], *,
        fold_coords: tuple[tuple[str, int, int], ...],
        fold_primers: tuple[tuple[str, DNA, DNA], ...],
        fold_sections_file: str | None,
        fold_full: bool,
        quantile: float,
        fold_temp: float,
        fold_constraint: str | None,
        fold_md: int,
        fold_mfe: bool,
        fold_max: int,
        fold_percent: float,
        tmp_dir: str,
        keep_tmp: bool,
        max_procs: int,
        parallel: bool,
        force: bool):
    """ Predict RNA secondary structures using mutation rates. """
    # Check for the dependencies and the DATAPATH environment variable.
    if error := require_dependency(RNASTRUCTURE_FOLD_CMD, __name__):
        logger.critical(error)
        return list()
    if error := require_dependency(RNASTRUCTURE_CT2DOT_CMD, __name__):
        logger.critical(error)
        return list()
    if error := require_data_path():
        logger.critical(error)
        return list()
    # Reactivities must be normalized before using them to fold.
    if quantile <= 0.:
        logger.warning("Fold needs normalized mutation rates, but got quantile "
                       f"= {quantile}; setting quantile to {DEFAULT_QUANTILE}")
        quantile = DEFAULT_QUANTILE
    # List the tables.
    tables = [table for _, table in find_foldable_tables(input_path)]
    # Get the sections to fold for every reference sequence.
    ref_seqs = RefSeqs()
    for table in tables:
        ref_seqs.add(table.ref, table.refseq)
    fold_sections = RefSections(ref_seqs,
                                sects_file=(Path(fold_sections_file)
                                            if fold_sections_file
                                            else None),
                                coords=fold_coords,
                                primers=fold_primers,
                                default_full=fold_full).dict
    # For each table whose reference had no sections defined, default to
    # the table's section.
    args = [(table, (fold_sections[table.ref]
                     if fold_sections[table.ref]
                     else [table.section]))
            for table in tables]
    # Fold the RNA profiles.
    return list(chain(dispatch(fold_profile,
                               max_procs,
                               parallel,
                               pass_n_procs=True,
                               args=args,
                               kwargs=dict(tmp_dir=Path(tmp_dir),
                                           keep_tmp=keep_tmp,
                                           quantile=quantile,
                                           fold_temp=fold_temp,
                                           fold_constraint=(
                                               Path(fold_constraint)
                                               if fold_constraint
                                               else None
                                           ),
                                           fold_md=fold_md,
                                           fold_mfe=fold_mfe,
                                           fold_max=fold_max,
                                           fold_percent=fold_percent,
                                           force=force))))


params = [
    arg_input_path,
    opt_fold_sections_file,
    opt_fold_coords,
    opt_fold_primers,
    opt_fold_full,
    opt_quantile,
    opt_fold_temp,
    opt_fold_constraint,
    opt_fold_md,
    opt_fold_mfe,
    opt_fold_max,
    opt_fold_percent,
    opt_tmp_dir,
    opt_keep_tmp,
    opt_max_procs,
    opt_parallel,
    opt_force,
]


@command(CMD_FOLD, params=params)
def cli(*args, **kwargs):
    """ Predict RNA secondary structures using mutation rates. """
    return run(*args, **kwargs)

########################################################################
#                                                                      #
# © Copyright 2024, the Rouskin Lab.                                   #
#                                                                      #
# This file is part of SEISMIC-RNA.                                    #
#                                                                      #
# SEISMIC-RNA is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# SEISMIC-RNA is distributed in the hope that it will be useful, but   #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANT- #
# ABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General     #
# Public License for more details.                                     #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with SEISMIC-RNA; if not, see <https://www.gnu.org/licenses>.  #
#                                                                      #
########################################################################
