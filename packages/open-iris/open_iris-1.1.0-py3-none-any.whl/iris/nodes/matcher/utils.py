from typing import List, Optional, Tuple

import numpy as np

from iris.io.dataclasses import IrisTemplate
from iris.io.errors import MatcherError


def normalized_HD(irisbitcount: int, maskbitcount: int, sqrt_totalbitcount: float, nm_dist: float) -> float:
    """Perform normalized HD calculation.

    Args:
        irisbitcount (int): nonmatched iriscode bit count.
        maskbitcount (int): common maskcode bit count.
        sqrt_totalbitcount (float): square root of bit counts.
        nm_dist (float): nonmatch distance used for normalized HD.

    Returns:
        float: normalized Hamming distance.
    """
    norm_HD = max(
        0, nm_dist - (nm_dist - irisbitcount / maskbitcount) * min(1.0, np.sqrt(maskbitcount) / sqrt_totalbitcount)
    )
    return norm_HD


def count_sqrt_totalbits(
    toal_codesize: int,
    half_width: List[int],
    weights: Optional[List[np.ndarray]] = None,
) -> Tuple[float, float, float]:
    """Count total amount of sqrt bits.

    Args:
        toal_codesizes (int): total size of iriscodes.
        half_width (List[int]): half width of iriscodes.
        weights (Optional[List[np.ndarray]] = None): list of weights table. Optional paremeter for weighted HD. Defaults to None.

    Returns:
        Tuple[float, float, float]: square root of bit counts from whole iris, top iris and bottom iris.
    """
    sqrt_totalbitcount = np.sqrt(np.sum([np.sum(w) for w in weights])) if weights else np.sqrt(toal_codesize * 3 / 4)

    sqrt_totalbitcount_bot = (
        np.sqrt(np.sum([np.sum(w[:, :hw, ...]) for w, hw in zip(weights, half_width)]))
        if weights
        else sqrt_totalbitcount / np.sqrt(2)
    )

    sqrt_totalbitcount_top = (
        np.sqrt(np.sum([np.sum(w[:, hw:, ...]) for w, hw in zip(weights, half_width)]))
        if weights
        else sqrt_totalbitcount / np.sqrt(2)
    )

    return sqrt_totalbitcount, sqrt_totalbitcount_top, sqrt_totalbitcount_bot


def count_nonmatchbits(
    irisbits: np.ndarray,
    maskbits: np.ndarray,
    half_width: List[int],
    weights: Optional[List[np.ndarray]] = None,
) -> Tuple[int, int, int, int]:
    """Count nonmatch bits for Hammming distance.

    Args:
        irisbits (np.ndarray): nonmatch irisbits.
        maskbits (np.ndarray): common maskbits.
        half_width (List[int]): list of half of code width.
        weights (Optional[np.ndarray] = None): list of weights table. Optional paremeter for weighted HD. Defaults to None.

    Returns:
        Tuple[int, int, int, int]: nonmatch iriscode bit count and common maskcode bit count from top iris and bottom iris.
    """
    if weights:
        irisbitcount_top = np.sum(
            [
                np.sum(np.multiply(x[:, hw:, ...] & y[:, hw:, ...], z[:, hw:, ...]))
                for x, y, hw, z in zip(irisbits, maskbits, half_width, weights)
            ]
        )
        maskbitcount_top = np.sum(
            [np.sum(np.multiply(x[:, hw:, ...], z[:, hw:, ...])) for x, hw, z in zip(maskbits, half_width, weights)]
        )
        irisbitcount_bot = np.sum(
            [
                np.sum(np.multiply(x[:, :hw, ...] & y[:, :hw, ...], z[:, :hw, ...]))
                for x, y, hw, z in zip(irisbits, maskbits, half_width, weights)
            ]
        )
        maskbitcount_bot = np.sum(
            [np.sum(np.multiply(x[:, :hw, ...], z[:, :hw, ...])) for x, hw, z in zip(maskbits, half_width, weights)]
        )
    else:
        irisbitcount_top = np.sum(
            [np.sum(x[:, hw:, ...] & y[:, hw:, ...]) for x, y, hw in zip(irisbits, maskbits, half_width)]
        )
        maskbitcount_top = np.sum([np.sum(x[:, hw:, ...]) for x, hw in zip(maskbits, half_width)])
        irisbitcount_bot = np.sum(
            [np.sum(x[:, :hw, ...] & y[:, :hw, ...]) for x, y, hw in zip(irisbits, maskbits, half_width)]
        )
        maskbitcount_bot = np.sum([np.sum(x[:, :hw, ...]) for x, hw in zip(maskbits, half_width)])

    return irisbitcount_top, maskbitcount_top, irisbitcount_bot, maskbitcount_bot


def hamming_distance(
    template_probe: IrisTemplate,
    template_gallery: IrisTemplate,
    rotation_shift: int,
    nm_dist: Optional[float] = None,
    weights: Optional[List[np.ndarray]] = None,
) -> Tuple[float, int]:
    """Compute Hamming distance.

    Args:
        template_probe (IrisTemplate): Iris template from probe.
        template_gallery (IrisTemplate): Iris template from gallery.
        rotation_shift (int): rotation allowed in matching, converted to columns.
        nm_dist (Optional[float] = None): nonmatch distance, Optional paremeter for normalized HD. Defaults to None.
        weights (Optional[List[np.ndarray]]= None): list of weights table. Optional paremeter for weighted HD. Defaults to None.

    Returns:
        Tuple[float, int]: miminum Hamming distance and corresonding rotation shift.
    """
    half_codewidth = []

    for probe_code, gallery_code in zip(template_probe.iris_codes, template_gallery.iris_codes):
        if probe_code.shape != gallery_code.shape:
            raise MatcherError("probe and gallery iris codes are of different sizes")
        if (probe_code.shape[1] % 2) != 0:
            raise MatcherError("number of columns of iris codes need to be even")
        half_codewidth.append(int(probe_code.shape[1] / 2))

    if weights:
        for probe_code, w in zip(template_probe.iris_codes, weights):
            if probe_code.shape != w.shape:
                raise MatcherError("weights table and iris codes are of different sizes")

    if nm_dist:
        if weights:
            sqrt_totalbitcount, sqrt_totalbitcount_top, sqrt_totalbitcount_bot = count_sqrt_totalbits(
                np.sum([np.size(a) for a in template_probe.iris_codes]), half_codewidth, weights
            )
        else:
            sqrt_totalbitcount, sqrt_totalbitcount_top, sqrt_totalbitcount_bot = count_sqrt_totalbits(
                np.sum([np.size(a) for a in template_probe.iris_codes]), half_codewidth
            )

    # Calculate the Hamming distance between probe and gallery template.
    match_dist = 1
    match_rot = 0
    for shiftby in range(-rotation_shift, rotation_shift + 1):
        irisbits = [
            np.roll(probe_code, shiftby, axis=1) != gallery_code
            for probe_code, gallery_code in zip(template_probe.iris_codes, template_gallery.iris_codes)
        ]
        maskbits = [
            np.roll(probe_code, shiftby, axis=1) & gallery_code
            for probe_code, gallery_code in zip(template_probe.mask_codes, template_gallery.mask_codes)
        ]

        if weights:
            irisbitcount_top, maskbitcount_top, irisbitcount_bot, maskbitcount_bot = count_nonmatchbits(
                irisbits, maskbits, half_codewidth, weights
            )
        else:
            irisbitcount_top, maskbitcount_top, irisbitcount_bot, maskbitcount_bot = count_nonmatchbits(
                irisbits, maskbits, half_codewidth
            )
        maskbitcount = maskbitcount_top + maskbitcount_bot

        if maskbitcount == 0:
            continue

        if nm_dist:
            normdist_top = (
                normalized_HD(irisbitcount_top, maskbitcount_top, sqrt_totalbitcount_top, nm_dist)
                if maskbitcount_top > 0
                else 1
            )
            normdist_bot = (
                normalized_HD(irisbitcount_bot, maskbitcount_bot, sqrt_totalbitcount_bot, nm_dist)
                if maskbitcount_bot > 0
                else 1
            )
            w_top = np.sqrt(maskbitcount_top)
            w_bot = np.sqrt(maskbitcount_bot)
            Hdist = (
                normalized_HD((irisbitcount_top + irisbitcount_bot), maskbitcount, sqrt_totalbitcount, nm_dist) / 2
                + (normdist_top * w_top + normdist_bot * w_bot) / (w_top + w_bot) / 2
            )
        else:
            Hdist = (irisbitcount_top + irisbitcount_bot) / maskbitcount

        if (Hdist < match_dist) or (Hdist == match_dist and shiftby == 0):
            match_dist = Hdist
            match_rot = shiftby

    return match_dist, match_rot
