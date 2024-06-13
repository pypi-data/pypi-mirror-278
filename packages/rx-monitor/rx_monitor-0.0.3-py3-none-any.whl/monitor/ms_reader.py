import os

import numpy
import pandas            as pnd
import utils_noroot      as utnr


from importlib.resources import files
from stats.average       import average  as stav
from rk.scales           import mass     as mscale
from rk.scales           import fraction as fscale
from logzero             import logger   as log

#----------------------------------------
class ms_reader:
    '''
    This class is used to read the mass scales and resolution values stored in JSON files
    '''
    def __init__(self, version=None):
        self._vers = version

        self._l_scale = ['mu', 'sg', 'br', 'mu_g', 'sg_g']
        self._l_trig  = ['MTOS', 'ETOS', 'GTIS'] 
        self._l_year  = ['r1', 'r2p1', '2017', '2018'] 
        self._l_brem  = [0, 1, 2]

        self._cas_dir = os.environ['CASDIR']
        self._dat_dir = files('monitor_data').joinpath(self._vers)
    #----------------------------------------
    def _get_mscale_brem(self, year, trig, brem):
        dat_path = f'{self._cas_dir}/monitor/mass_scales/{self._vers}/{year}_{trig}/pars/cat_{brem}/data.json'
        sim_path = f'{self._cas_dir}/monitor/mass_scales/{self._vers}/{year}_{trig}/pars/cat_{brem}/signal.json'
    
        d_dat = utnr.load_json(dat_path)
        d_sim = utnr.load_json(sim_path)
    
        ms    = mscale(dt=d_dat, mc=d_sim)
    
        return ms 
    #----------------------------------------
    def _get_bscale(self, year, trig):
        '''
        Will return a list with the fraction of brem and the corresponding error, i.e.
    
        [val_br_0, err_br_0, ..., err_br_2]
        '''
        if trig == 'MTOS':
            return [1, 0, 0, 0, 0, 0] 
    
        d_mscale = {}
        for brem in self._l_brem:
            d_mscale[brem] = self._get_mscale_brem(year, trig, brem)
    
        fr   = fscale(d_mscale)
        d_fr = fr.scales
    
        val_z, err_z = d_fr[0]
        val_o, err_o = d_fr[1]
        val_t, err_t = d_fr[2]
    
        return [val_z, err_z, val_o, err_o, val_t, err_t] 
    #----------------------------------------
    def _get_mscale_mrg(self, year, trig):
        '''
        Returns:

        d_scale : {'scale', (val, err, pvl) : 'resolution' : (val, err, pvl)} where pvl is the p-value of
                  the brem combination.
        '''
        l_ms   = []
        l_brem = [0] if trig == 'MTOS' else self._l_brem
    
        for brem in l_brem:
            ms = self._get_mscale_brem(year, trig, brem)
            l_ms.append(ms)
    
        d_scale = {}
        if   len(l_ms) > 1:
            d_scale = l_ms[0].combine(l_ms[1:])
        elif len(l_ms) == 1:
            val, err = l_ms[0].scale
            d_scale['scale']      = val, err, 1
    
            val, err = l_ms[0].resolution
            d_scale['resolution'] = val, err, 1
        else:
            log.error(f'Invalid size of list of mass objects: {len(l_ms)}')
            raise
    
        return d_scale 
    #----------------------------------------
    def _get_mass_scales_mrg(self, scale):
        l_col = []
        for trig in self._l_trig:
            l_col.append(f'v_{trig}')
            l_col.append(f'e_{trig}')
    
        df = pnd.DataFrame(columns=l_col)
        for year in self._l_year:
            l_row = []
            for trig in self._l_trig:
                d_scale = self._get_mscale_mrg(year, trig)
    
                scl_v, scl_e, _ = d_scale['scale']
                res_v, res_e, _ = d_scale['resolution']
    
                if   scale == 'mu':
                    l_row.append(scl_v)
                    l_row.append(scl_e)
                elif scale == 'sg':
                    l_row.append(res_v)
                    l_row.append(res_e)
                else:
                    log.error(f'Invalid scale: {scale}')
                    raise ValueError
    
            df_scl = utnr.add_row_to_df(df, l_row, index=year)
    
        return df
    #----------------------------------------
    def _get_mscale_spt(self, year, trig):
        '''
        Returns:

        l_scale, l_reso : Where l_x = [v_0, e_0, v_1, e_1, v_2, e_2]
        '''
        l_brem = [0] if trig == 'MTOS' else self._l_brem
        l_ms   = [self._get_mscale_brem(year, trig, brem) for brem in l_brem]

        if trig == 'MTOS':
            val, err     = l_ms[0].scale
            l_scale      = [val, err, 0, 0, 0, 0]
    
            val, err     = l_ms[0].resolution
            l_resolution = [val, err, 1, 0, 1, 0]

            return l_scale , l_resolution
    

        val_0, err_0 = l_ms[0].scale
        val_1, err_1 = l_ms[1].scale
        val_2, err_2 = l_ms[2].scale

        l_scale      = [val_0, err_0, val_1, err_1, val_2, err_2]

        val_0, err_0 = l_ms[0].resolution
        val_1, err_1 = l_ms[1].resolution
        val_2, err_2 = l_ms[2].resolution

        l_resolution = [val_0, err_0, val_1, err_1, val_2, err_2]
    
        return l_scale , l_resolution
    #----------------------------------------
    def _get_mass_scales_spt(self, scale):
        l_col = []
        for brem in self._l_brem:
            l_col.append(f'v_{brem}')
            l_col.append(f'e_{brem}')
    
        df = pnd.DataFrame(columns=l_col)
        for year in self._l_year:
            for trig in self._l_trig:
                l_scale, l_reso = self._get_mscale_spt(year, trig)
    
                if   scale == 'mu_g':
                    l_row = l_scale
                elif scale == 'sg_g':
                    l_row = l_reso 
                else:
                    log.error(f'Invalid scale: {scale}')
                    raise ValueError
    
                df = utnr.add_row_to_df(df, l_row, index=f'{trig} {year}')
    
        return df
    #----------------------------------------
    def _get_brem_scales(self, scale):
        l_col = []
        for brem in self._l_brem:
            l_col.append(f'v_{brem}')
            l_col.append(f'e_{brem}')
    
        df = pnd.DataFrame(columns=l_col)
        for year in self._l_year:
            for trig in ['MTOS', 'ETOS', 'GTIS']:
                l_row = self._get_bscale(year, trig)
                utnr.add_row_to_df(df, l_row, index=f'{trig} {year}')
    
        return df
    #----------------------------------------
    def get_scales(self, scale):
        '''
        This function returns a pandas dataframe with the scales and resolution
        information

        Parameters
        ----------------
        scale (str): mu (mass scale), sg (mass resolution), br (Bremsstrahlung correction), mu_g (scale split by brem), sg_g (resolution split by brem)

        Returns 
        ----------------
        Pandas dataframe
        '''
        scl_dir   = utnr.make_dir_path(self._dat_dir)

        if   scale in [  'mu',   'sg']:
            df = self._get_mass_scales_mrg(scale)
        elif scale in ['mu_g', 'sg_g']:
            df = self._get_mass_scales_spt(scale)
        elif scale == 'br':
            df = self._get_brem_scales(scale)
        else:
            log.error(f'Invalid scale: {scale}')
            raise ValueError
    
        json_path = f'{scl_dir}/{scale}.json'
        log.info(f'Saving scales to: {json_path}')
        df.index = df.index.astype(str)
        df.to_json(json_path)

        return df
#----------------------------------------

