from typing import Dict
from typing import List
from typing import Any
from typing import Tuple
from typing import Optional

import collections
import itertools
import pandas as pd

from rdkit import Chem
from rdkit.Chem import rdFMCS
from rdkit.Chem import rdmolops
from rdkit.Chem import rdRGroupDecomposition

from rdkit.Chem.rdmolops import AdjustQueryParameters
from rdkit.Chem.rdmolops import AdjustQueryProperties

from rdkit.Chem.Scaffolds import MurckoScaffold

from ..types import Mol
from ..mol import keep_largest_fragment
from ..mol import fix_mol
from ..mol import to_mol
from ..mol import add_hs
from ..mol import remove_hs
from ..convert import to_smiles
from ..convert import to_smarts
from ..convert import from_smarts


def trim_side_chain(mol: Chem.rdchem.Mol, core, unwanted_side_chains):
    """Trim list of side chain from a molecule."""

    mol = add_hs(mol)

    match = mol.GetSubstructMatch(core)
    map2idx = {}
    map2nei = {}
    unwanted2map = {}
    for patt in unwanted_side_chains:
        unwanted2map[patt] = [a.GetAtomMapNum() for a in patt.GetAtoms() if a.GetAtomMapNum()]
    unwanted_mapping = list(itertools.chain.from_iterable(unwanted2map.values()))

    for atom in core.GetAtoms():
        num = atom.GetAtomMapNum()
        if num and num in unwanted_mapping:
            mol_atom_idx = match[atom.GetIdx()]
            map2idx[mol_atom_idx] = num
            nei_atoms = mol.GetAtomWithIdx(mol_atom_idx).GetNeighbors()
            map2nei[mol_atom_idx] = [n.GetIdx() for n in nei_atoms if n.GetIdx() in match]

    emol = Chem.EditableMol(mol)
    for atom_idx, atom_map in map2idx.items():
        dummy = Chem.rdchem.Atom("*")
        dummy.SetAtomMapNum(atom_map)
        nei_idx = map2nei.get(atom_idx, [None])[0]
        if nei_idx:
            bond = mol.GetBondBetweenAtoms(atom_idx, nei_idx)
            emol.RemoveBond(atom_idx, nei_idx)
            new_ind = emol.AddAtom(dummy)
            emol.AddBond(nei_idx, new_ind, bond.GetBondType())

    mol = emol.GetMol()
    mol = remove_hs(mol)
    query_param = AdjustQueryParameters()
    query_param.makeDummiesQueries = False
    query_param.adjustDegree = False
    query_param.aromatizeIfPossible = True
    for patt, _ in unwanted2map.items():
        cur_frag = fix_mol(patt)
        mol = Chem.DeleteSubstructs(mol, cur_frag, onlyFrags=True)

    return keep_largest_fragment(mol)


def fuzzy_scaffolding(
    mols: List[Chem.rdchem.Mol],
    enforce_subs: Optional[List[str]] = None,
    n_atom_cuttoff: int = 8,
    additional_templates: Optional[List[Mol]] = None,
    ignore_non_ring: bool = False,
    mcs_params: Optional[Dict[Any, Any]] = None,
) -> Tuple[set, pd.DataFrame, pd.DataFrame]:
    """Generate fuzzy scaffold with enforceable group that needs to appear
    in the core, forcing to keep the full side chain if required

    Args:
        mols: List of all molecules
        enforce_subs: List of substructure to enforce on the scaffold.
        n_atom_cuttoff: Minimum number of atom a core should have.
        additional_templates: Additional template to use to generate scaffolds.
        ignore_non_ring: Whether to ignore atom no in murcko ring system, even if they are in the framework.
        mcs_params: Arguments of MCS algorithm.

    Returns:
        - `set` - `scaffolds` - All found scaffolds in the molecules as valid smiles.
        - `pd.DataFrame` - `df_scaffold_infos_transposed` - A pandas dataframe with Infos on the scaffold mapping, ignoring
            any side chain that had to be enforced. Key corresponds to generic scaffold smiles.
            Values at ['smarts'] corresponds to smarts representation of the true scaffold (from MCS)
            Values at ['mols'] corresponds to list of molecules matching the scaffold
            Values at ['scf'] corresponds to the list of scaffolds from MurckoScaffold.GetScaffoldForMol
        - `pd.DataFrame` - `df_scaffold_groups` - A pandas dataframe with Map between each generic scaffold
            and the R-groups decomposition row.
    """

    # NOTE(hadim): consider parallelize this (if possible).
    # NOTE(hadim): consider refactoring this function in smaller reusable functions.

    if enforce_subs is None:
        enforce_subs = []

    if additional_templates is None:
        additional_templates = []

    if mcs_params is None:
        mcs_params = {}

    rg_params = rdRGroupDecomposition.RGroupDecompositionParameters()
    rg_params.removeAllHydrogenRGroups = True
    rg_params.removeHydrogensPostMatch = True
    rg_params.alignment = rdRGroupDecomposition.RGroupCoreAlignment.MCS
    rg_params.matchingStrategy = rdRGroupDecomposition.RGroupMatching.Exhaustive
    rg_params.rgroupLabelling = rdRGroupDecomposition.RGroupLabelling.AtomMap
    rg_params.labels = rdRGroupDecomposition.RGroupLabels.AtomIndexLabels

    core_query_param = AdjustQueryParameters()
    core_query_param.makeDummiesQueries = True
    core_query_param.adjustDegree = False
    core_query_param.makeBondsGeneric = True

    # group molecules by they generic Murcko scaffold, allowing
    # side chain that contains cycle (might be a bad idea)
    scf2infos = collections.defaultdict(dict)
    scf2groups = {}
    all_scaffolds = set([])

    for m in mols:
        generic_m = MurckoScaffold.MakeScaffoldGeneric(m)
        scf = MurckoScaffold.GetScaffoldForMol(m)
        try:
            scf = MurckoScaffold.MakeScaffoldGeneric(scf)
        except Exception:
            pass

        if ignore_non_ring:
            rw_scf = Chem.RWMol(scf)
            atms = [a.GetIdx() for a in rw_scf.GetAtoms() if not a.IsInRing()]
            atms.sort(reverse=True)
            for a in atms:
                rw_scf.RemoveAtom(a)
            scfs = list(rdmolops.GetMolFrags(rw_scf, asMols=False))
        else:
            scfs = [to_smiles(scf)]

        # add templates mols if exists:
        for tmp in additional_templates:
            tmp = to_mol(tmp)
            tmp_scf = MurckoScaffold.MakeScaffoldGeneric(tmp)
            if generic_m.HasSubstructMatch(tmp_scf):
                scfs.append(to_smiles(tmp_scf))

        for scf in scfs:
            if scf2infos[scf].get("mols"):
                scf2infos[scf]["mols"].append(m)
            else:
                scf2infos[scf]["mols"] = [m]

    for scf in scf2infos:
        # cheat by adding murcko as last mol always
        popout = False
        mols = scf2infos[scf]["mols"]
        if len(mols) < 2:
            mols = mols + [MurckoScaffold.GetScaffoldForMol(mols[0])]
            popout = True

        # compute the MCS of the cluster
        mcs = rdFMCS.FindMCS(
            mols,
            atomCompare=rdFMCS.AtomCompare.CompareAny,
            bondCompare=rdFMCS.BondCompare.CompareAny,
            completeRingsOnly=True,
            **mcs_params,
        )

        mcsM = from_smarts(mcs.smartsString)
        mcsM.UpdatePropertyCache(False)
        Chem.SetHybridization(mcsM)

        if mcsM.GetNumAtoms() < n_atom_cuttoff:
            continue

        scf2infos[scf]["smarts"] = to_smarts(mcsM)
        if popout:
            mols = mols[:-1]

        core_groups = []
        # generate rgroups based on the mcs core
        success_mols = []
        try:
            rg = rdRGroupDecomposition.RGroupDecomposition(mcsM, rg_params)
            for i, analog in enumerate(mols):
                analog.RemoveAllConformers()
                res = rg.Add(analog)
                if not (res < 0):
                    success_mols.append(i)
            rg.Process()
            core_groups = rg.GetRGroupsAsRows()
        except Exception:
            pass

        mols = [mols[i] for i in success_mols]
        scf2groups[scf] = core_groups
        for mol, gp in zip(mols, core_groups):
            core = gp["Core"]
            acceptable_groups = [
                a.GetAtomMapNum()
                for a in core.GetAtoms()
                if (a.GetAtomMapNum() and not a.IsInRing())
            ]

            rgroups = [gp[f"R{k}"] for k in acceptable_groups if f"R{k}" in gp.keys()]
            if enforce_subs is not None:
                rgroups = [
                    rgp
                    for rgp in rgroups
                    if not any([len(rgp.GetSubstructMatch(frag)) > 0 for frag in enforce_subs])
                ]
            try:
                scaff = trim_side_chain(mol, AdjustQueryProperties(core, core_query_param), rgroups)
            except Exception:
                continue
            all_scaffolds.add(to_smiles(scaff))
        # if user wants a dataframe turned on...
        # there are processing routines to make the df more readable.
    df_infos = pd.DataFrame(scf2infos)
    df_infos_t = df_infos.transpose()
    df_infos_t.insert(0, "scf", list(scf2infos.keys()), True)
    df_infos_t.reset_index(inplace=True, drop=True)

    # relabel index and column labels to
    # to be more readable
    df_infos_t.index.name = "index"

    df_groups = pd.DataFrame.from_dict(scf2groups, orient="index")
    df_groups.reset_index(inplace=True, drop=True)

    # relabel index and column labels to
    # to be more readable
    df_groups.index.name = "index"
    df_groups.columns = [f"{str(h)}_core_group" for h in df_groups.columns]

    # enter the scf columns at the first column for df_groups
    df_groups.insert(0, "scf", list(scf2groups.keys()), True)
    return all_scaffolds, df_infos_t, df_groups
