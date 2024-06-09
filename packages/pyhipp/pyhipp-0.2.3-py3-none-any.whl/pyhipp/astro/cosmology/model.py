from __future__ import annotations
from typing import Dict, Any, Self, Callable
import numpy as np
import h5py
import json
import os
from pathlib import Path
from scipy.interpolate import interp1d
import importlib_resources
from functools import cached_property
from .param import ParamList, Param
from ...core.abc import HasName, HasSimpleRepr, HasCache, IsImmutable
from ...core import dataproc as dp
import astropy.cosmology
from ..quantity import UnitSystem
from contextlib import contextmanager
from dataclasses import dataclass


class LambdaCDM(HasName, HasSimpleRepr, IsImmutable):
    def __init__(self,
                 params: ParamList,
                 data_dir: Path,
                 meta: Dict[str, Any] = None,
                 name: str = None) -> None:
        super().__init__(name=name)

        self.params = params
        self.data_dir = Path(data_dir)
        self.meta = meta

        self.big_hubble0 = np.array(0.1022712165045695)         # [h/Gyr]

        self.astropy_model = astropy.cosmology.FlatLambdaCDM(
            H0=self.hubble*100.0,
            Om0=self.omega_m0,
            Tcmb0=self.t_cmb,
            Ob0=self.omega_b0)

        self.unit_system = UnitSystem.create_for_cosmology(self.hubble.item())

    @staticmethod
    def from_conf_file(path: Path) -> LambdaCDM:
        file_name = str(path)
        assert file_name[-5:] == '.json', f'{file_name} must be a JSON file'
        with open(file_name, 'rb') as f:
            conf: dict = json.load(f)

        ps: dict = conf.pop('parameters')
        ps = ParamList([Param(value=v, name=k) for k, v in ps.items()])

        name: str = conf.pop('name')
        data_dir: Path = path.parent / conf.pop('data_dir')
        meta = conf

        return LambdaCDM(params=ParamList(ps),
                         data_dir=data_dir,
                         meta=meta,
                         name=name)

    @staticmethod
    def from_parameters(params: dict[str, np.ndarray], *,
                        name: str = None,
                        data_dir: Path = None,
                        meta: dict[str, Any] = None,
                        ) -> Self:
        '''
        Examples
        --------
        # The parameters of "737" cosmology
        params = {
            "hubble": 0.7,
            "omega_m0": 0.3,
            "omega_l0": 0.7,
            "omega_b0": 0.045,
            "t_cmb": 2.7255,
        }
        cosm = LambdaCDM.from_parameters(params)
        '''
        ps = ParamList([Param(value=v, name=k) for k, v in params.items()])
        if name is None:
            name = ''
        if data_dir is None:
            data_dir = Path.cwd()
        if meta is None:
            meta = {}
        return LambdaCDM(params=ps, data_dir=data_dir, meta=meta, name=name)

    @staticmethod
    def from_astropy_model(model: astropy.cosmology.FlatLambdaCDM, **kw):
        '''
        @kw: passed to from_parameters().
        '''
        params = {
            'hubble': model.h,
            'omega_m0': model.Om0,
            'omega_l0': model.Ode0,
            'omega_b0': model.Ob0,
            't_cmb': model.Tcmb0,
        }
        return LambdaCDM.from_parameters(params, **kw)

    def to_simple_repr(self) -> dict:
        return {
            'name': self.name,
            'data_dir': str(self.data_dir),
            'meta': self.meta,
            'params': self.params.to_simple_repr(),
        }

    @property
    def baryon_fraction0(self) -> np.ndarray:
        return self.omega_b0 / self.omega_m0

    @property
    def hubble(self) -> np.ndarray:
        return self.params['hubble'].value

    def big_hubble(self, z: np.ndarray) -> np.ndarray:
        u = self.unit_system.u_big_hubble
        return (self.astropy_model.H(z) / u).to(1).value

    @property
    def omega_m0(self) -> np.ndarray:
        return self.params['omega_m0'].value

    def omega_m(self, z: np.ndarray) -> np.ndarray:
        return self.astropy_model.Om(z)

    @property
    def omega_l0(self) -> np.ndarray:
        return self.params['omega_l0'].value

    def omega_l(self, z: np.ndarray) -> np.ndarray:
        return self.astropy_model.Ode(z)

    @property
    def omega_b0(self) -> np.ndarray:
        return self.params['omega_b0'].value

    def omega_b(self, z: np.ndarray) -> np.ndarray:
        return self.astropy_model.Ob(z)

    @property
    def sigma_8(self) -> np.ndarray:
        return self.params['sigma_8'].value

    @property
    def n_spec(self) -> np.ndarray:
        return self.params['n_spec'].value

    @property
    def t_cmb(self) -> np.ndarray:
        return self.params['t_cmb'].value

    def rho_crit(self, z: np.ndarray) -> np.ndarray:
        '''
        In physical volume.
        '''
        rho = self.astropy_model.critical_density(z)
        return (rho / self.unit_system.u_density).to(1).value

    def rho_matter(self, z: np.ndarray) -> np.ndarray:
        '''
        In physical volume.
        '''
        rho_crit = self.rho_crit(z)
        omega_m = self.omega_m(z)
        rho_matter = rho_crit * omega_m
        return rho_matter

    def age(self, z: np.ndarray) -> np.ndarray:
        '''
        In Gyr/h.
        '''
        age = self.astropy_model.age(z)
        return (age / self.unit_system.u_t).to(1).value

    @cached_property
    def halo_theory(self) -> HaloTheory:
        return HaloTheory(self.data_dir/'data.hdf5', self)

    @cached_property
    def distances(self) -> DistanceCalculator:
        return DistanceCalculator(self)

    @cached_property
    def times(self) -> TimeCalculator:
        return TimeCalculator(self)

    @cached_property
    def redshifts(self) -> RedshiftCalculator:
        return RedshiftCalculator(self)


class DistanceCalculator:
    def __init__(self, model: LambdaCDM) -> None:
        self.model = model
        self.hubble = model.hubble
        self.astropy_model = model.astropy_model

    def comoving_at(self, z: np.ndarray) -> np.ndarray:
        '''
        Returned in [Mpc/h].
        '''
        d = self.astropy_model.comoving_distance(z).to('Mpc').value
        return d * self.hubble


class TimeCalculator:
    def __init__(self, model: LambdaCDM) -> None:
        self.model = model
        self.hubble = model.hubble
        self.astropy_model = model.astropy_model

    def lookback_at(self, z: np.ndarray) -> np.ndarray:
        '''
        Returned in [Gyr/h].
        '''
        t_lb = self.astropy_model.lookback_time(z).to('Gyr').value
        return t_lb * self.hubble


class RedshiftCalculator:
    def __init__(self, model: LambdaCDM) -> None:
        self.model = model
        self.hubble = model.hubble
        self.astropy_model = model.astropy_model

    def at_comoving(self, d: np.ndarray, **sol_kw) -> np.ndarray:
        d = dp.Num.bound(d, lo=1.0e-4)
        d = (d / self.hubble) * astropy.units.Mpc
        z = astropy.cosmology.z_at_value(
            self.astropy_model.comoving_distance, d, **sol_kw).value
        return z


@dataclass
class VirialProperties:
    '''
    rho: comoving.
    r: comoving.
    r_phy: physical.
    v: physical.
    '''
    m: np.ndarray
    rho: np.ndarray
    r: np.ndarray
    r_phy: np.ndarray
    v: np.ndarray

    @property
    def t_dyn(self):
        t_dyn = self.r_phy / self.v
        return t_dyn


class HaloTheory(HasSimpleRepr, IsImmutable):
    '''
    The initialization has overhead. So it is embeded into `LambdaCDM` as a 
    cached property. As a result, `LambdaCDM` is not mutable.
    '''

    def __init__(self, data_file: Path, model: LambdaCDM) -> None:
        super().__init__()

        self.data_file = Path(data_file)
        self.model = model

    def to_simple_repr(self) -> dict:
        return {
            'data_file': str(self.data_file),
            '__interp': self.__interp,
        }

    def rho_vir_mean(self, f: np.ndarray = 200.0,
                     z: np.ndarray = 0.0) -> np.ndarray:
        '''
        In comoving unit.
        '''
        a = 1.0 / (1.0 + z)
        rho_mean = self.model.rho_matter(z) * a**3
        return f * rho_mean

    def rho_vir_crit(self, f: np.ndarray = 200.0,
                     z: np.ndarray = 0.0) -> np.ndarray:
        '''
        In comoving unit.
        '''
        a = 1.0 / (1.0 + z)
        rho_crit = self.model.rho_crit(z) * a**3
        return f * rho_crit

    def vir_props_mean(
            self, m_vir: np.ndarray, f: np.ndarray = 200.0,
            z: np.ndarray = 0.0) -> VirialProperties:
        rho = self.rho_vir_mean(f, z)
        return self.__vir_props(m_vir, rho, z)

    def vir_props_crit(
            self, m_vir: np.ndarray, f: np.ndarray = 200.0,
            z: np.ndarray = 0.0) -> VirialProperties:
        rho = self.rho_vir_crit(f, z)
        return self.__vir_props(m_vir, rho, z)

    def r_vir(self, m_vir: np.ndarray, rho_vir: np.ndarray) -> np.ndarray:
        '''
        Expect `rho_vir` in comoving unit, and return `r_vir` also in comoving 
        unit (checked to be consistent with TNG).
        '''
        V = m_vir / rho_vir
        return (V / (4./3.*np.pi))**(1./3.)

    def v_vir(self, m_vir, r_vir, to_kmps=False) -> np.ndarray:
        '''
        Expect `r_vir` in physical unit, and return `v_vir` in physical.
        '''
        us = self.model.unit_system
        v_vir = np.sqrt(us.c_gravity * m_vir / r_vir)
        if to_kmps:
            v_vir *= us.u_v_to_kmps
        return v_vir

    def lg_sigma(self, lg_m: np.ndarray) -> np.ndarray:
        '''
        lg_m: log10(M) [10^10 Msun/h]
        '''
        return self.__interp['f_lg_sigma_at_lg_m'](lg_m)

    def dlg_sigma_dlg_m(self, lg_m: np.ndarray) -> np.ndarray:
        '''
        lg_m: log10(M) [10^10 Msun/h]
        '''
        return self.__interp['f_dlg_sigma_dlg_m_at_lg_m'](lg_m)

    def lg_delta_c(self, z: np.ndarray) -> np.ndarray:
        return self.__interp['f_lg_delta_c_at_z'](z)

    @cached_property
    def __interp(self) -> dict[str, Callable | dict]:
        with h5py.File(str(self.data_file), 'r') as f:
            g = f['LgDeltaC']
            z, lg_delta_c = g['z'][()], g['lg_delta_c'][()]

            g = f['LgSigma']
            lg_m = g['lg_m'][()]
            lg_sigma = g['lg_sigma'][()]
            dlg_sigma_dlg_m = g['dlg_sigma_dlg_m'][()]

        kw = {'kind': 'slinear'}
        f_lg_sigma_at_lg_m = interp1d(lg_m, lg_sigma, **kw)
        f_dlg_sigma_dlg_m_at_lg_m = interp1d(lg_m, dlg_sigma_dlg_m, **kw)
        f_lg_delta_c_at_z = interp1d(z, lg_delta_c, **kw)
        return {
            'z': self.__find_quantity_info(z),
            'lg_delta_c': self.__find_quantity_info(lg_delta_c),
            'lg_m': self.__find_quantity_info(lg_m),
            'lg_sigma': self.__find_quantity_info(lg_sigma),
            'dlg_sigma_dlg_m': self.__find_quantity_info(dlg_sigma_dlg_m),

            'f_lg_sigma_at_lg_m': f_lg_sigma_at_lg_m,
            'f_dlg_sigma_dlg_m_at_lg_m': f_dlg_sigma_dlg_m_at_lg_m,
            'f_lg_delta_c_at_z': f_lg_delta_c_at_z,
        }

    def __find_quantity_info(self, x) -> Dict:
        return {
            'range': (x[0].tolist(), x[-1].tolist()),
            'step': np.diff(x).mean().tolist(),
        }

    def __vir_props(self, m: np.ndarray, rho: np.ndarray, z: np.ndarray) -> VirialProperties:
        r = self.r_vir(m, rho)
        a = 1. / (1. + z)
        r_phy = a * r
        v = self.v_vir(m, r_phy)
        return VirialProperties(m, rho, r, r_phy, v)


class _Predefined(HasSimpleRepr, HasCache):
    def __init__(self) -> None:

        super().__init__()

        self.__resource_data_dir = importlib_resources.files(
            'pyhipp.astro').joinpath('data/cosmologies')

        for name in 'tng', 'eagle':
            self.put_cache(name, self.load(name))

    def __getitem__(self, name) -> LambdaCDM:
        return self.get_cache_or(name, lambda: self.load(name))

    @property
    def data_dir(self) -> Path:
        return importlib_resources.as_file(self.__resource_data_dir)

    def to_simple_repr(self):
        c: dict[str, LambdaCDM] = self.cache
        with self.data_dir as p:
            data_dir = str(p)
        return {
            'data_dir': data_dir,
            'models': {
                n: m.to_simple_repr() for n, m in c.items()
            },
        }

    def load(self, name) -> LambdaCDM:
        with self.data_dir as p:
            out = LambdaCDM.from_conf_file(p / f'{name}.json')
        return out


predefined = _Predefined()
