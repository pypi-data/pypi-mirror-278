"""Camera wrapper"""
from typing import Any, Optional, Callable, Union, Dict, cast, Tuple
import logging
from dataclasses import dataclass, field
import functools
import ctypes

from .hiklibs.MvCameraControl_class import MvCamera
from .hiklibs.CameraParams_header import PixelType_Gvsp_BGR8_Packed, PixelType_Gvsp_RGB8_Packed
from .hiklibs.CameraParams_const import MV_ACCESS_Exclusive
from .hiklibs.CameraParams_header import MVCC_INTVALUE, MVCC_FLOATVALUE, MVCC_ENUMVALUE, MV_CC_PIXEL_CONVERT_PARAM
from .types import DeviceInfo, Frame, FrameCallbackType, DeviceTransport, MV_PIXEL_TYPES, MV_TRIG_TYPES
from .errors import (
    HIKException,
    HandleCreateError,
    HandleDestroyError,
    mv_errstr,
    CamCloseError,
    CamOpenError,
    CamClosed,
    CamStateError,
    CamSettingsError,
    CamCommandError,
    CamReadError,
    ConvertError,
)


LOGGER = logging.getLogger(__name__)


@dataclass
class Camera:  # pylint: disable=R0904
    """Wrap the camera pointer to a more pythonic api"""

    info: DeviceInfo = field()
    frame_callback: Optional[Callable[[Frame, "Camera"], None]] = field(default=None)

    raise_on_setting_failure: bool = field(default=True)

    _mvcam: MvCamera = field(init=False, repr=False)
    _open: bool = field(init=False, default=False)
    _grabbing: bool = field(init=False, default=False)
    _mv_callback: Optional[Callable[..., None]] = field(init=False, default=None)
    settings_cache: Dict[str, Union[int, float, str]] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        """init special properties"""
        self._mvcam = MvCamera()  # type: ignore[no-untyped-call]
        ret = self._mvcam.MV_CC_CreateHandle(self.info.mvcamhandle)  # type: ignore[no-untyped-call]
        if ret != 0:
            raise HandleCreateError(mv_errstr(ret))

    def __del__(self) -> None:
        """Release the handle"""
        if self._open:
            LOGGER.error("Deleting still open camera")
            try:
                self.close()
            except HIKException as exc:
                LOGGER.error("Got {} when closing".format(exc))
        ret = self._mvcam.MV_CC_DestroyHandle()  # type: ignore[no-untyped-call]
        if ret != 0:
            raise HandleDestroyError(mv_errstr(ret))

    @property
    def closed(self) -> bool:
        """Is the camera closed"""
        return not self._open

    def trigger_enable(self, enabled: bool = True) -> bool:
        """Enable or disable trigger"""
        if not self._open:
            raise CamClosed()
        mode = "On"
        if not enabled:
            mode = "Off"
        ret = self.set_enum("TriggerMode", mode)
        self.settings_cache["triggermode"] = enabled
        return ret

    def set_trigger_source(self, sourcename: str) -> bool:
        """Set the trigger source, generally "Software" or "Line0"."""
        ret = self.set_enum("TriggerSource", sourcename)
        self.settings_cache["triggersource"] = self.get_trigger_source()
        return ret

    def get_trigger_source(self) -> str:
        """Get the trigger source"""
        return MV_TRIG_TYPES[self.get_enum("TriggerSource")]

    def send_trigger(self) -> None:
        """Send SW trigger to camera"""
        self.send_command("TriggerSoftware")

    def send_command(self, command: str) -> None:
        """Send a command to the camera"""
        ret = self._mvcam.MV_CC_SetCommandValue(command)  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamCommandError(mv_errstr(ret))

    def set_framerate(self, value: float) -> bool:
        """Set the camera framerate"""
        if not self.set_bool("AcquisitionFrameRateEnable", True):
            return False
        return self.set_float("AcquisitionFrameRate", value)

    def optimize_gige_packetsize(self) -> bool:
        """There is a magical helper to determine best packet size, use it and set to cameera"""
        if self.info.transport != DeviceTransport.GIGE:
            LOGGER.error("Not a gige camera")
            return False
        size = self._mvcam.MV_CC_GetOptimalPacketSize()  # type: ignore[no-untyped-call]
        LOGGER.info("Optimal packet size is {}".format(size))
        return self.set_gige_packetsize(size)

    def set_gige_packetsize(self, size: int) -> bool:
        """Set the packet size"""
        if self.info.transport != DeviceTransport.GIGE:
            LOGGER.error("Not a gige camera")
            return False
        return self.set_int("GevSCPSPacketSize", size)

    def set_exposure(self, value: Union[float, int]) -> bool:
        """Set the exposure time and set exposure to timed.
        value on camera is float but it's uSec so floats don't make too much sense"""
        self.set_enum("ExposureMode", "Timed")
        ret = self.set_float("ExposureTime", float(value))
        self.settings_cache["exposure"] = float(value)
        return ret

    def start(self) -> None:
        """Start grabbing"""
        if not self._open:
            raise CamClosed()
        self._mv_callback = FrameCallbackType(functools.partial(frame_callback, wrapper=self))
        ret = self._mvcam.MV_CC_RegisterImageCallBackEx(self._mv_callback, None)  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamStateError(mv_errstr(ret))

        ret = self._mvcam.MV_CC_StartGrabbing()  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamStateError(mv_errstr(ret))
        self._grabbing = True

    def stop(self) -> None:
        """Stop grabbing"""
        if not self._grabbing:
            LOGGER.warning("Not grabbing")
            return
        ret = self._mvcam.MV_CC_StopGrabbing()  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamStateError(mv_errstr(ret))
        self._grabbing = False

    def open(self) -> None:
        """Open the camera (we only support exclusive mode)"""
        if self._open:
            LOGGER.warning("Already open")
            return
        ret = self._mvcam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamOpenError(mv_errstr(ret))
        self._open = True
        self.settings_cache["exposure"] = self.get_float("ExposureTime")
        self.settings_cache["triggermode"] = bool(self.get_enum("TriggerMode"))
        self.settings_cache["triggersource"] = self.get_trigger_source()

    def close(self) -> None:
        """Close the camera"""
        if not self._open:
            LOGGER.warning("Already closed")
            return
        if self._grabbing:
            LOGGER.error("Closing camera that is grabbing")
            try:
                self.stop()
            except HIKException as exc:
                LOGGER.error("Got {} when stopping".format(exc))
        ret = self._mvcam.MV_CC_CloseDevice()  # type: ignore[no-untyped-call]
        if ret != 0:
            raise CamCloseError(mv_errstr(ret))
        self._open = False

    def set_int(self, varname: str, value: int) -> bool:
        """Set integer value on the camera"""
        ret = self._mvcam.MV_CC_SetIntValue(varname, value)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to set {}, error {}".format(varname, mv_errstr(ret)))
            if self.raise_on_setting_failure:
                raise CamSettingsError(mv_errstr(ret))
            return False
        return True

    def get_int(self, varname: str) -> int:
        """Get integer value by name from camera"""
        dataptr = MVCC_INTVALUE()
        ctypes.memset(ctypes.byref(dataptr), 0, ctypes.sizeof(MVCC_INTVALUE))
        ret = self._mvcam.MV_CC_GetIntValue(varname, dataptr)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to read {}, error {}".format(varname, mv_errstr(ret)))
            raise CamReadError(mv_errstr(ret))
        return int(dataptr.nCurValue)

    def set_enum(self, varname: str, value: str) -> bool:
        """Set an enum filed value byt it's string name"""
        ret = self._mvcam.MV_CC_SetEnumValueByString(varname, value)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to set {}, error {}".format(varname, mv_errstr(ret)))
            if self.raise_on_setting_failure:
                raise CamSettingsError(mv_errstr(ret))
            return False
        return True

    def get_enum(self, varname: str) -> int:
        """Get enum value"""
        dataptr = MVCC_ENUMVALUE()
        ret = self._mvcam.MV_CC_GetEnumValue(varname, dataptr)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to read {}, error {}".format(varname, mv_errstr(ret)))
            raise CamReadError(mv_errstr(ret))
        return int(dataptr.nCurValue)

    def get_pixelformat(self) -> str:
        """Get pixelformat as string"""
        return MV_PIXEL_TYPES[self.get_enum("PixelFormat")]

    def set_float(self, varname: str, value: float) -> bool:
        """Set float value on the camera"""
        ret = self._mvcam.MV_CC_SetFloatValue(varname, value)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to set {}, error {}".format(varname, mv_errstr(ret)))
            if self.raise_on_setting_failure:
                raise CamSettingsError(mv_errstr(ret))
            return False
        return True

    def get_float(self, varname: str) -> float:
        """Get float value by name from camera"""
        dataptr = MVCC_FLOATVALUE()
        ctypes.memset(ctypes.byref(dataptr), 0, ctypes.sizeof(MVCC_FLOATVALUE))
        ret = self._mvcam.MV_CC_GetFloatValue(varname, dataptr)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to read {}, error {}".format(varname, mv_errstr(ret)))
            raise CamReadError(mv_errstr(ret))
        return float(dataptr.fCurValue)

    def set_bool(self, varname: str, value: bool) -> bool:
        """Set boolean value on the camera"""
        ret = self._mvcam.MV_CC_SetBoolValue(varname, value)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to set {}, error {}".format(varname, mv_errstr(ret)))
            if self.raise_on_setting_failure:
                raise CamSettingsError(mv_errstr(ret))
            return False
        return True

    def pxformat_convert(self, frame: Frame, tgtformat: int, tgtbpp: int) -> Tuple[str, bytes]:
        """Convert pixel format, tgtbpp is **bytes** per pixel, tgtformat must be on one of the
        PixelType_ values from .hiklibs.CameraParams_header"""
        tgt_size = frame.size[0] * frame.size[1] * tgtbpp
        params = MV_CC_PIXEL_CONVERT_PARAM()
        ctypes.memset(ctypes.byref(params), 0, ctypes.sizeof(params))
        params.nWidth = frame.infoptrcts.nWidth
        params.nHeight = frame.infoptrcts.nHeight
        params.pSrcData = frame.dataptr
        params.nSrcDataLen = frame.infoptrcts.nFrameLen
        params.enSrcPixelType = frame.infoptrcts.enPixelType
        params.enDstPixelType = tgtformat
        params.pDstBuffer = (ctypes.c_ubyte * tgt_size)()
        params.nDstBufferSize = tgt_size
        dest_type = MV_PIXEL_TYPES[params.enDstPixelType]

        ret = self._mvcam.MV_CC_ConvertPixelType(params)  # type: ignore[no-untyped-call]
        if ret != 0:
            LOGGER.error("Failed to convert from {} to {}, error {}".format(frame.type, dest_type, mv_errstr(ret)))
            raise ConvertError(mv_errstr(ret))

        # Copy the new buffer
        img_buff = (ctypes.c_ubyte * params.nDstLen)()
        ctypes.memmove(ctypes.byref(img_buff), params.pDstBuffer, params.nDstLen)
        return dest_type, bytes(img_buff)

    def debayer(self, frame: Frame) -> Tuple[str, bytes]:
        """debayer the data, return str describing new format (rgb8 or bgr8) and the raw data"""
        if frame.type == "BayerRG8":
            tgtformat = PixelType_Gvsp_RGB8_Packed
        elif frame.type == "BayerBG8":
            tgtformat = PixelType_Gvsp_BGR8_Packed
        else:
            raise ConvertError(f"Don't know what to ddo with {frame.type}")
        return self.pxformat_convert(frame, tgtformat, 3)


def frame_callback(dataptr: Any, infoptr: Any, userptr: ctypes.c_void_p, *, wrapper: Camera) -> None:
    """Handle a frame from the C grabber loop"""
    _ = userptr
    frame = Frame(infoptr, dataptr)
    if frame.exposure == 0.0:  # if frame does not have exposure overwrite with cached value
        frame.exposure = cast(float, wrapper.settings_cache["exposure"])
    if wrapper.frame_callback:
        wrapper.frame_callback(frame, wrapper)
