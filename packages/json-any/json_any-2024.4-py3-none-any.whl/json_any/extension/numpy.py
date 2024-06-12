# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import json
from typing import Any, Callable

from json_any.catalog.module import blsc, nmpy, pcst
from json_any.catalog.type import io_bytes_t
from json_any.catalog.type import np_array_t as array_t

BLOSC = "blosc"
BLOSC_BYTES = "blosc.bytes"
NUMPY = "numpy"
NUMPY_COMPRESSED = "numpy.compressed"
PCA_B_STREAM = "pca_b_stream"

_NUMPY_NDARRAY_FROM_VERSIONS = {}
_NUMPY_NDARRAY_TO_VERSIONS = {}

if nmpy is None:

    def _RaiseException() -> None:
        """"""
        raise NotImplementedError(f"Numpy module not installed or importable.")

    def IsNumpyScalar(*_, **__) -> Any:
        _RaiseException()

    def AsScalarRepresentation(*_, **__) -> Any:
        _RaiseException()

    def AsMostConciseRepresentation(*_, **__) -> Any:
        _RaiseException()

    def AsNumpyArray(*_, **__) -> Any:
        _RaiseException()

    def AddNumpyNDArrayRepresentation(*_, **__) -> None:
        _RaiseException()

    def RemoveNumpyNDArrayRepresentation(*_, **__) -> None:
        _RaiseException()

else:
    _SCALAR_META_TYPES = (nmpy.bool_, nmpy.number, nmpy.character)

    def IsNumpyScalar(type_: type, /) -> bool:
        """"""
        return nmpy.issubclass_(type_, _SCALAR_META_TYPES)

    def AsScalarRepresentation(instance: Any, type_: type, /) -> Any:
        """"""
        if nmpy.issubclass_(type_, nmpy.bool_):
            output = bool(instance)
        elif nmpy.issubclass_(type_, nmpy.integer):
            output = int(instance)
        elif nmpy.issubclass_(type_, nmpy.floating):
            output = float(instance)
        elif nmpy.issubclass_(type_, complex):
            # Use list (instead of tuple) since tuples seem to be unJSONed as list, so...
            output = [float(nmpy.real(instance)), float(nmpy.imag(instance))]
        else:
            output = str(instance)

        return output

    def AsMostConciseRepresentation(array: array_t, /) -> tuple[str, str]:
        """"""
        version = (array.tolist(), array.dtype.char)
        try:
            min_length = json.dumps(version).__len__()
            output = (NUMPY, version)
        except TypeError:
            min_length = None
            output = ("None", None)

        fake_file = io_bytes_t()
        nmpy.savez_compressed(fake_file, array=array)
        version = fake_file.getvalue().decode(encoding="iso-8859-1")
        fake_file.close()
        length = version.__len__()
        if (min_length is None) or (length < min_length):
            output, min_length = (NUMPY_COMPRESSED, version), length

        for ToVersion in _NUMPY_NDARRAY_TO_VERSIONS.values():
            version = ToVersion(array)
            if version is None:
                continue
            length = version[1].__len__()
            if length < min_length:
                output, min_length = version, length

        return output

    def AsNumpyArray(how: str, what: str) -> array_t:
        """"""
        if how == NUMPY:
            data, dtype = what
            return nmpy.array(data, dtype=dtype)
        elif how == NUMPY_COMPRESSED:
            fake_file = io_bytes_t(what.encode(encoding="iso-8859-1"))
            output = nmpy.load(fake_file)["array"]
            fake_file.close()
            return output

        return _NUMPY_NDARRAY_FROM_VERSIONS[how](what)

    def AddNumpyNDArrayRepresentation(
        name: str,
        /,
        *,
        ToVersion: Callable[[array_t], tuple[int, str, str]] = None,
        FromVersion: Callable[[str], array_t] = None,
    ) -> None:
        """"""
        global _NUMPY_NDARRAY_TO_VERSIONS, _NUMPY_NDARRAY_FROM_VERSIONS

        if name in (NUMPY, NUMPY_COMPRESSED):
            raise ValueError(
                f"{NUMPY}, {NUMPY_COMPRESSED}: Reserved representation names"
            )

        if name == BLOSC:
            if blsc is None:
                raise ModuleNotFoundError('Module "blosc" not installed or unfoundable')
            _NUMPY_NDARRAY_TO_VERSIONS[BLOSC] = _BloscVersion
            _NUMPY_NDARRAY_FROM_VERSIONS[BLOSC] = _FromBloscVersion
            _NUMPY_NDARRAY_FROM_VERSIONS[BLOSC_BYTES] = _FromBloscBytesVersion
        elif name == PCA_B_STREAM:
            if pcst is None:
                raise ModuleNotFoundError(
                    'Module "pca_b_stream" not installed or unfoundable'
                )
            _NUMPY_NDARRAY_TO_VERSIONS[PCA_B_STREAM] = _PCABStreamVersion
            _NUMPY_NDARRAY_FROM_VERSIONS[PCA_B_STREAM] = _FromPCABStreamVersion
        else:
            if (ToVersion is None) or (FromVersion is None):
                raise ValueError(
                    f'{name}: Invalid keyword-only arguments "ToVersion" and/or "FromVersion". '
                    f"Actual={ToVersion}/{FromVersion}. Expected=Both non-None."
                )
            _NUMPY_NDARRAY_TO_VERSIONS[name] = ToVersion
            _NUMPY_NDARRAY_FROM_VERSIONS[name] = FromVersion

    def RemoveNumpyNDArrayRepresentation(name: str, /) -> None:
        """"""
        global _NUMPY_NDARRAY_TO_VERSIONS, _NUMPY_NDARRAY_FROM_VERSIONS

        if name in (NUMPY, NUMPY_COMPRESSED):
            raise ValueError(
                f"{NUMPY}, {NUMPY_COMPRESSED}: Default representations cannot be removed"
            )

        del _NUMPY_NDARRAY_TO_VERSIONS[name]
        del _NUMPY_NDARRAY_FROM_VERSIONS[name]
        if name == BLOSC:
            del _NUMPY_NDARRAY_FROM_VERSIONS[BLOSC_BYTES]

    def _BloscVersion(array: array_t, /) -> tuple[str, str] | None:
        """"""
        # Do not compare packed instances of an array since blsc.pack_array(array) !=_{can be} blsc.pack_array(array)
        packed = blsc.pack_array(array)
        if isinstance(packed, bytes):
            packed = packed.decode(encoding="iso-8859-1")
            how = BLOSC_BYTES
        else:
            how = BLOSC

        return how, packed

    def _FromBloscVersion(blosc: str, /) -> array_t:
        """"""
        return blsc.unpack_array(blosc)

    def _FromBloscBytesVersion(blosc: str, /) -> array_t:
        """"""
        return blsc.unpack_array(blosc.encode(encoding="iso-8859-1"))

    def _PCABStreamVersion(array: array_t, /) -> tuple[str, str] | None:
        """"""
        if nmpy.issubclass_(
            array.dtype, (bool, nmpy.bool_, int, nmpy.integer, float, nmpy.floating)
        ):
            stream = pcst.PCA2BStream(array).decode(encoding="iso-8859-1")
            return PCA_B_STREAM, stream

        return None

    def _FromPCABStreamVersion(pca_b_stream: str, /) -> array_t:
        """"""
        return pcst.BStream2PCA(pca_b_stream.encode(encoding="iso-8859-1"))
