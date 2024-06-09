# -*- coding: utf-8 -*-
"""
    v1 201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    v2 202101, Dr. Jie Zheng & Dr./Prof. Linqiao Jiang
    v3 202201, Zheng & Jiang
    v4 202304, Upgrade, restructure, Zheng & Jiang
    Quick_Light_Curve_Pipeline
"""


# import os
from .u_conf import config, workmode
# from .u_log import init_logger
from .q_mklist import mklist
from .q_biascomb import biascomb
from .q_flatcomb import flatcomb
from .q_imgcorr import imgcorr
from .q_offset import offset
from .q_phot import phot
from .q_pick import pick
from .q_wcs import wcs
from .q_cata import cata
from .q_cali import cali
from .q_graph import graph


def do_all(
        ini_file:str|tuple[str]|list[str],
        raw_dir:str,
        red_dir:str,
        steps:str="lbfiopwkcdg",
        obj:str=None,
        band:str=None,
        alt_bias:str=None,
        alt_flat:str=None,
        alt_coord:dict|tuple[str]=None,
        base_img:str=None,
        se_cmd:str="source-extractor",
        aper:float|list[float]=None,
        starxy:list[list[float]]=None,
        ind_tgt:int|list[int]=None,
        ind_ref:int|list[int]=None,
        ind_chk:int|list[int]=None,
        mode:workmode=workmode(workmode.MISS_SKIP+workmode.EXIST_APPEND),
        **kwargs
) -> None:
    """
    A general steps caller
    :param ini_file: extra ini file(s)
    :param raw_dir: raw data dir
    :param red_dir: reduce result dir
    :param steps: steps, each char stands for one step
        l = List
        b = Bias comb
        f = Flat comb
        i = Image correct
        o = Offset
        p = find stars and Photometry
        w = Ecs
        k = picK ref stars
        c = Catalog
        d = Differential flux
        g = Graph
    :param obj: object to reduce, if none, reduce all
    :param band: band to reduce, if none or *, all
    :param alt_bias: if specified, use this bias but not today
    :param alt_flat: if specified, use this flat but bot today,
                     the number and order of flats must be the same of the bands
    :param alt_coord: coordination of object, if not provided in fits header
                      if dict, key is object name and value is coordination
                      if tuple, 2 str for RA (hms) and Dec (dms)
    :param base_img: if none, use image 0, int as index, or str as filename
    :param se_cmd: command of source-extractor, if empty or None, use sep package
    :param aper: one or multi aperture(s) for photometry
    :param starxy: a list contains xy of star, if not, auto pick
    :param ind_tgt: index of target star, if not, use 0
    :param ind_ref: index of reference star, if not, use 1:n-1
    :param ind_chk: index of check star, if not, use 1:n-1
    :param mode: working mode for file exists or missing
    :param kwargs: extra config
    """

    # make config
    conf = config(ini_file=ini_file, extra_conf=kwargs)

    # make List
    list_all = mklist(
        conf,
        raw_dir, red_dir,
        obj, band,
        mode, "l" in steps
    )
    # print(list_all)

    # Bias combine
    if "b" in steps:
        biascomb(
            conf,
            raw_dir, red_dir,
            mode
        )

    # Flat combine
    if "f" in steps:
        for b in list_all:  # each band
            if "flat" in list_all[b]:
                flatcomb(
                    conf,
                    raw_dir, red_dir, b,
                    alt_bias,
                    mode
                )

    for b in list_all:  # each band
        for o in list_all[b]: # each object
            if o in ("bias", "flat"):
                continue

            # Image correction
            if "i" in steps:
                # check alt-coord
                ac = alt_coord.get(o, None) if isinstance(alt_coord, dict) else alt_coord
                imgcorr(
                    conf,
                    raw_dir, red_dir, o, b,
                    alt_bias, alt_flat, ac,
                    mode
                )

            # Offset
            if "o" in steps:
                offset(
                    conf,
                    raw_dir, red_dir, o, b,
                    base_img,
                    mode
                )

            # Photometry
            if "p" in steps:
                phot(
                    conf,
                    red_dir, o, b,
                    se_cmd, aper,
                    mode
                )

            # WCS
            # if "w" in steps:
            #     wcs(
            #         conf,
            #         red_dir, o, b,
            #         mode
            #     )

            # picK target, ref, check stars
            # if k specified, or c required but starxy not given or only one,
            # if "k" in steps or ("c" in steps and (not starxy or len(starxy) == 1)):
            #     starxy = pick(
            #         conf,
            #         red_dir, o, b,
            #         mode
            #     )

            # collect general catalog of stars at xy
            if "c" in steps:
                cata(
                    conf,
                    raw_dir, red_dir, o, b,
                    starxy,
                    base_img,
                    mode
                )

            # differential flux/mag calibration
            if "d" in steps:
                cali(
                    conf,
                    raw_dir, red_dir, o, b,
                    ind_tgt, ind_ref, ind_chk,
                    mode
                )

            # graph plotting
            if "g" in steps:
                graph(
                    conf,
                    raw_dir, red_dir, o, b,
                    mode
                )
