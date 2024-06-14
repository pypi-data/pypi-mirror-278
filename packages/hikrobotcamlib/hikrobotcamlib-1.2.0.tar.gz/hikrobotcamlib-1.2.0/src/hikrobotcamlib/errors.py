"""Errors"""
from typing import Optional

from .hiklibs import MvErrorDefine_const

MV_ERROR_CODES = {
    getattr(MvErrorDefine_const, name): name for name in dir(MvErrorDefine_const) if name.startswith("MV_")
}


class HIKException(Exception):
    """Generic baseclass for catching things"""


class EnumerationError(HIKException, RuntimeError):
    """Failure to enumerate cameras"""


class CamHandleError(HIKException, RuntimeError):
    """Errors related to camera handles"""


class HandleCreateError(CamHandleError):
    """Failure to create a handle for the camera"""


class HandleDestroyError(CamHandleError):
    """Failure to destroy a handle for the camera"""


class CamStateError(HIKException, RuntimeError):
    """Errors related to camera state, like open/close"""


class CamOpenError(CamStateError):
    """Could not open camera"""


class CamCloseError(CamStateError):
    """Could not close camera"""


class CamSettingsError(CamStateError):
    """Could not not set some camera value"""


class CamClosed(CamStateError):
    """Camera is closed and action needs it to be open"""


class InvalidTransport(HIKException, ValueError):
    """A problem with the transport value"""


class FrameError(HIKException, RuntimeError):
    """A problem with frames"""


class ConvertError(FrameError):
    """Frame conversion errors"""


class CamCommandError(HIKException, RuntimeError):
    """Errors related to sending commands to camera, like SW trigger"""


class CamReadError(HIKException, RuntimeError):
    """Errors related to reading values from the camera"""


def mv_errstr(code: int) -> Optional[str]:
    """Return the constant name that matches the error code"""
    if code not in MV_ERROR_CODES:
        return None
    return MV_ERROR_CODES[code]
