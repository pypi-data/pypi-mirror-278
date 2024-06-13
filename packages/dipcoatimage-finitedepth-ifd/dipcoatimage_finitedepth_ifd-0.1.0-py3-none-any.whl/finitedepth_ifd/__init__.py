"""Finite depth dip coating uniformity measurement using integral Fréchet distance.

To reproduce the examples, run the following code first::

    import cv2
    from finitedepth import *
    from finitedepth_ifd import *
"""

import abc
import dataclasses
from functools import partial

import cv2
import numpy as np
import numpy.typing as npt
from curvesimilarities import afd_owp, qafd_owp  # type: ignore[import-untyped]
from finitedepth import CoatingLayerBase, RectSubstrate
from finitedepth.cache import attrcache
from finitedepth.coatinglayer import DataTypeVar, SubstTypeVar, parallel_curve
from scipy.interpolate import splev, splprep  # type: ignore
from scipy.optimize import root  # type: ignore

__all__ = [
    "IfdRoughnessBase",
    "RectIfdRoughness",
    "RectIfdRoughnessData",
]


ROUGHNESS_TYPES = (
    "arithmetic",
    "quadratic",
)


class IfdRoughnessBase(CoatingLayerBase[SubstTypeVar, DataTypeVar]):
    """Base class to measure layer surface roughness with integral Fréchet distance.

    The following types of roughness are supported:

    - Arithmetic roughness :math:`R_a`
    - Quadratic mean roughness :math:`R_q`

    Parameters
    ----------
    image, substrate
        See :class:`CoatingLayerBase <finitedepth.CoatingLayerBase>`.
    roughness_type : {'arithmetic', 'quadratic'}
    delta : double
        The maximum distance between the Steiner points to compute the roughness.
        Refer to :meth:`roughness` for more explanation.

    Other Parameters
    ----------------
    tempmatch : tuple, optional
        See :class:`CoatingLayerBase <finitedepth.CoatingLayerBase>`.
    """

    def __init__(
        self,
        image: npt.NDArray[np.uint8],
        substrate: SubstTypeVar,
        roughness_type: str,
        delta: float,
        *,
        tempmatch: tuple[tuple[int, int], float] | None = None,
    ):
        if roughness_type not in ROUGHNESS_TYPES:
            raise ValueError("Unknown type of roughness: %s" % roughness_type)
        if not isinstance(delta, float):
            raise TypeError("delta must be a double-precision float.")
        if not delta > 0:
            raise TypeError("delta must be a positive number.")
        super().__init__(image, substrate, tempmatch=tempmatch)
        self.roughness_type = roughness_type
        self.delta = delta

    @abc.abstractmethod
    def surface(self) -> npt.NDArray[np.int32]:
        """Coating layer surface points.

        Returns
        -------
        ndarray
            An :math:`N` by :math:`2` array containing the :math:`xy`-coordinates
            of :math:`N` points which constitute the coating layer surface profile.
        """
        ...

    @abc.abstractmethod
    def uniform_layer(self) -> npt.NDArray[np.float_]:
        """Imaginary uniform layer points.

        Returns
        -------
        thickness : double
            Thickness of the uniform layer.
        ndarray
            An :math:`M` by :math:`2` array containing the :math:`xy`-coordinates
            of :math:`M` points which constitute the uniform layer profile.
        """
        ...

    @attrcache("_roughness")
    def roughness(self) -> tuple[float, npt.NDArray[np.float_]]:
        """Surface roughness of the coating layer.

        Returns
        -------
        roughness : double
            Roughness value.
        path : ndarray
            An :math:`P` by :math:`2` array representing the optimal warping path
            in the parameter space.

        See Also
        --------
        curvesimilarities.averagefrechet.afd : Average Fréchet distance.
        curvesimilarities.averagefrechet.qafd : Quadratic average Fréchet distance.

        Notes
        -----
        The roughness is acquired by computing the similarity between :meth:`surface`
        and :meth:`uniform_layer`.
        """
        if self.roughness_type == "arithmetic":
            roughness, path = afd_owp(self.surface(), self.uniform_layer(), self.delta)
        elif self.roughness_type == "quadratic":
            roughness, path = qafd_owp(self.surface(), self.uniform_layer(), self.delta)
        else:
            roughness, path = np.nan, np.empty((0, 2), dtype=np.float_)
        return float(roughness), path


@dataclasses.dataclass
class RectIfdRoughnessData:
    """Analysis data for :class:`RectIfdRoughness`.

    Attributes
    ----------
    Roughness : float
        Coating layer roughness.
    """

    Roughness: float


class RectIfdRoughness(IfdRoughnessBase[RectSubstrate, RectIfdRoughnessData]):
    """Measure layer surface roughness over rectangular substrate.

    Parameters
    ----------
    image
        See :class:`CoatingLayerBase <finitedepth.CoatingLayerBase>`.
    substrate : :class:`RectSubstrate <finitedepth.RectSubstrate>`.
        Substrate instance.
    roughness_type, delta
        See :class:`IfdRoughnessBase`.
    opening_ksize : tuple of int
        Kernel size for morphological opening operation. Must be zero or odd.
    reconstruct_radius : int
        Radius of the safe zone for noise removal.
        Two imaginary circles with this radius are drawn on bottom corners of the
        substrate. When extracting the coating layer, connected components not spanning
        over any of these circles are regarded as noise.

    Other Parameters
    ----------------
    tempmatch : tuple, optional
        See :class:`CoatingLayerBase <finitedepth.CoatingLayerBase>`.

    Examples
    --------
    Construct the substrate instance first.

    >>> ref_img = cv2.imread(get_sample_path("ref.png"), cv2.IMREAD_GRAYSCALE)
    >>> ref = Reference(
    ...     cv2.threshold(ref_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
    ...     (10, 10, 1250, 200),
    ...     (100, 100, 1200, 500),
    ... )
    >>> subst = RectSubstrate(ref, 3.0, 1.0, 0.01)

    Construct the coating layer instance.

    >>> target_img = cv2.imread(get_sample_path("coat.png"), cv2.IMREAD_GRAYSCALE)
    >>> coat = RectIfdRoughness(
    ...     cv2.threshold(target_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1],
    ...     subst,
    ...     "arithmetic",
    ...     5.0,
    ...     (1, 1),
    ...     50,
    ... )

    Visualize the coating layer.

    >>> import matplotlib.pyplot as plt #doctest: +SKIP
    >>> plt.imshow(coat.draw()) #doctest: +SKIP
    """

    DataType = RectIfdRoughnessData

    def __init__(
        self,
        image: npt.NDArray[np.uint8],
        substrate: RectSubstrate,
        roughness_type: str,
        delta: float,
        opening_ksize: tuple[int, int],
        reconstruct_radius: int,
        *,
        tempmatch: tuple[tuple[int, int], float] | None = None,
    ):
        if not all(i == 0 or (i > 0 and i % 2 == 1) for i in opening_ksize):
            raise ValueError("Kernel size must be zero or odd.")
        if reconstruct_radius < 0:
            raise ValueError("Reconstruct radius must be zero or positive.")
        super().__init__(image, substrate, roughness_type, delta, tempmatch=tempmatch)
        self.opening_ksize = opening_ksize
        self.reconstruct_radius = reconstruct_radius

    def valid(self) -> bool:
        """Check if the coating layer is valid.

        The coating layer is invalid if the capillary bridge is not ruptured.

        Returns
        -------
        bool
        """
        p0 = self.substrate_point()
        _, bl, br, _ = self.substrate.contour()[self.substrate.vertices()]
        (B,) = p0 + bl
        (C,) = p0 + br
        top = np.max([B[1], C[1]])
        bot = self.image.shape[0]
        if top > bot:
            # substrate is located outside of the frame
            return False
        left = B[0]
        right = C[0]
        roi_binimg = self.image[top:bot, left:right]
        return bool(np.any(np.all(roi_binimg, axis=1)))

    @attrcache("_extracted_layer")
    def extract_layer(self) -> npt.NDArray[np.bool_]:
        """Extract the coating layer region from the target image.

        Returns
        -------
        ndarray of bool
            An array where the coating layer region is True. Has the same shape as
            :attr:`image`.

        Notes
        -----
        The following operations are performed to remove the error pixels:

        - Image opening with :attr:`opening_ksize` attribute.
        - Reconstruct connected components using :attr:`reconstruct_radius` and
          and substrate vertices.
        """
        # Perform opening to remove error pixels. We named the parameter as
        # "closing" because the coating layer is black in original image, but
        # in fact we do opening since the layer is True in extracted layer.
        ksize = self.opening_ksize
        if any(i == 0 for i in ksize):
            img = super().extract_layer().astype(np.uint8) * 255
        else:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize)
            img = cv2.morphologyEx(
                super().extract_layer().astype(np.uint8) * 255,
                cv2.MORPH_OPEN,
                kernel,
            )

        # closed image may still have error pixels, and at least we have to
        # remove the errors that are disconnected to the layer.
        # we identify the layer pixels as the connected components that are
        # close to the lower vertices.
        vicinity_mask = np.zeros(img.shape, np.uint8)
        p0 = self.substrate_point()
        _, bl, br, _ = self.substrate.contour()[self.substrate.vertices()]
        (B,) = p0 + bl
        (C,) = p0 + br
        R = self.reconstruct_radius
        cv2.circle(
            vicinity_mask, B.astype(np.int32), R, 1, -1
        )  # type: ignore[call-overload]
        cv2.circle(
            vicinity_mask, C.astype(np.int32), R, 1, -1
        )  # type: ignore[call-overload]
        n = np.dot((C - B) / np.linalg.norm((C - B)), np.array([[0, 1], [-1, 0]]))
        pts = np.stack([B, B + R * n, C + R * n, C]).astype(np.int32)
        cv2.fillPoly(vicinity_mask, [pts], 1)  # type: ignore[call-overload]
        _, labels = cv2.connectedComponents(img)
        layer_comps = np.unique(labels[np.where(vicinity_mask.astype(bool))])
        layer_mask = np.isin(labels, layer_comps[layer_comps != 0])

        return layer_mask

    def substrate_contour(self) -> npt.NDArray[np.int_]:
        """Return :attr:`substrate`'s contour in :attr:`image`."""
        return self.substrate.contour() + self.substrate_point()

    @attrcache("_interface_indices")
    def interface_indices(self) -> npt.NDArray[np.int_]:
        """Return indices of the substrate contour for the solid-liquid interface.

        The interface points can be retrieved by slicing the substrate contour with
        there indices.

        Returns
        -------
        ndarray
            Starting and ending indices for the solid-liquid interface, empty if the
            interface does not exist.

        See Also
        --------
        substrate_contour : The substrate contour which can be sliced.

        Notes
        -----
        The interface is detected by finding the points on the substrate contour which
        are adjacent to the points in :meth:`extract_layer`.
        """
        layer_dil = cv2.dilate(self.extract_layer().astype(np.uint8), np.ones((3, 3)))
        x, y = self.substrate_contour().transpose(2, 0, 1)
        H, W = self.image.shape[:2]
        mask = layer_dil[np.clip(y, 0, H - 1), np.clip(x, 0, W - 1)]
        idx = np.nonzero(mask[:, 0])[0]
        if len(idx) > 0:
            idx = idx[[0, -1]]
        return idx

    @attrcache("_surface")
    def surface(self) -> npt.NDArray[np.int32]:
        """See :meth:`IfdRoughnessBase.surface`."""
        idxs = self.interface_indices()
        if len(idxs) == 0:
            return np.empty((0, 2), dtype=np.int32)
        boundary_pts = self.substrate_contour()[idxs]

        (cnt,), _ = cv2.findContours(
            self.coated_substrate().astype(np.uint8),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        vec = cnt - boundary_pts.transpose(1, 0, 2)
        (I0, I1) = np.argmin(np.linalg.norm(vec, axis=-1), axis=0)

        return np.squeeze(cnt[I0 : I1 + 1], axis=1)

    @attrcache("_uniform_layer")
    def uniform_layer(self) -> npt.NDArray[np.float_]:
        """See :meth:`IfdRoughnessBase.uniform_layer`."""
        idxs = self.interface_indices()
        if len(idxs) == 0:
            return np.empty((0, 2), dtype=np.int32)
        i0, i1 = idxs
        subst_cnt = self.substrate_contour()[i0:i1]

        A = np.count_nonzero(self.extract_layer())
        (t,) = root(partial(_uniform_layer_area, subst=subst_cnt, x0=A), [0]).x
        return np.squeeze(parallel_curve(subst_cnt, t), axis=1)

    def analyze(self) -> RectIfdRoughnessData:
        """Return analysis result.

        Returns
        -------
        :class:`RectIfdRoughnessData`
        """
        return self.DataType(self.roughness()[0])

    def draw(self, pairs_dist: float = 20.0) -> npt.NDArray[np.uint8]:
        """Visualize the analysis result.

        Draws the surface, the uniform layer, and the roughness pairs.

        Parameters
        ----------
        pairs_dist : float
            Distance between the roughness pairs in the IFD parameter space.
            Decreasing this value increases the density of pairs.
        """
        image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB).astype(np.uint8)
        if not self.valid():
            return image

        image[self.extract_layer()] = 255

        cv2.polylines(
            image,
            [self.surface().reshape(-1, 1, 2).astype(np.int32)],
            isClosed=False,
            color=(0, 0, 255),
            thickness=1,
        )
        cv2.polylines(
            image,
            [self.uniform_layer().reshape(-1, 1, 2).astype(np.int32)],
            isClosed=False,
            color=(255, 0, 0),
            thickness=1,
        )

        _, path = self.roughness()
        path_len = np.sum(np.linalg.norm(np.diff(path, axis=0), axis=-1), axis=0)
        tck, _ = splprep(path.T, k=1, s=0)
        u = np.linspace(0, 1, int(path_len // pairs_dist))
        pairs = np.stack(splev(u, tck)).T

        surf_seg_vec = np.diff(self.surface(), axis=0)
        surf_seg_len = np.linalg.norm(surf_seg_vec, axis=-1)
        surf_seg_unitvec = surf_seg_vec / surf_seg_len[..., np.newaxis]
        surf_vert = np.cumsum(surf_seg_len)
        pairs_surf_vert_idx = np.searchsorted(surf_vert, pairs[:, 0])

        p = self.surface()[pairs_surf_vert_idx]
        t = pairs[:, 0] - np.insert(surf_vert, 0, 0)[pairs_surf_vert_idx]
        u = surf_seg_unitvec[pairs_surf_vert_idx]
        pairs_surf_pt = (p + t[..., np.newaxis] * u).astype(np.int32)

        ul_seg_vec = np.diff(self.uniform_layer(), axis=0)
        ul_seg_len = np.linalg.norm(ul_seg_vec, axis=-1)
        ul_seg_unitvec = ul_seg_vec / ul_seg_len[..., np.newaxis]
        ul_vert = np.cumsum(ul_seg_len)
        pairs_ul_vert_idx = np.searchsorted(ul_vert, pairs[:, 1])

        q = self.uniform_layer()[pairs_ul_vert_idx]
        s = pairs[:, 1] - np.insert(ul_vert, 0, 0)[pairs_ul_vert_idx]
        v = ul_seg_unitvec[pairs_ul_vert_idx]
        pairs_ul_pt = (q + s[..., np.newaxis] * v).astype(np.int32)

        pairs_pts = np.stack([pairs_surf_pt, pairs_ul_pt])[np.newaxis, ...]

        cv2.polylines(
            image,
            pairs_pts.transpose(2, 1, 0, 3),
            isClosed=False,
            color=(0, 255, 0),
            thickness=1,
        )

        return image


def _uniform_layer_area(thickness, subst, x0):
    cnt = np.concatenate([subst, np.flip(parallel_curve(subst, thickness[0]), axis=0)])
    return cv2.contourArea(cnt.astype(np.float32)) - x0
