/**
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * @file oculusHmd.cxx
 * @author rdb
 * @date 2014-03-26
 */

#include "oculusHmd.h"
#include "inputDeviceManager.h"

#if OVR_PRODUCT_VERSION == 0 && OVR_MAJOR_VERSION < 7
#define ovr_ConfigureTracking ovrHmd_ConfigureTracking
#define ovr_Destroy ovrHmd_Destroy
#define ovr_DismissHSWDisplay ovrHmd_DismissHSWDisplay
#define ovr_GetFovTextureSize ovrHmd_GetFovTextureSize
#define ovr_GetFrameTiming ovrHmd_GetFrameTiming
#define ovr_GetTrackingState ovrHmd_GetTrackingState
#endif

TypeHandle OculusHmd::_type_handle;

/**
 *
 */
OculusHmd::
OculusHmd() :
  InputDevice("Oculus Rift", DC_hmd, IDF_has_tracker),
  _session(0),
  _connected_types(0)
{
  // It's tempting to call ovr_GetHmdDesc to initialize the device properties.
  // However, this causes the Rift to wake up from sleep, and the Runtime will
  // start showing a loading screen for this application, even though the user
  // may not have committed yet to using it.  Very annoying, and arguably a
  // bug in the Oculus Runtime.
  _desc = ovr_GetHmdDesc(NULL);
  _is_connected = (_desc.Type != ovrHmd_None);
  _name = _desc.ProductName;
  _product_id = _desc.ProductId;
  _vendor_id = _desc.VendorId;
  _manufacturer = _desc.Manufacturer;
  _serial_number = _desc.SerialNumber;
}

/**
 *
 */
OculusHmd::
OculusHmd(ovrSession session) :
  InputDevice(string(), DC_hmd, IDF_has_tracker),
  _session(session),
  _connected_types(0)
{
#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 7
  _desc = ovr_GetHmdDesc(session);
#else
  _desc = *session;
#endif
  _name = _desc.ProductName;
  _product_id = _desc.ProductId;
  _vendor_id = _desc.VendorId;
  _manufacturer = _desc.Manufacturer;
  _serial_number = _desc.SerialNumber;

#if OVR_PRODUCT_VERSION == 0
  ovr_ConfigureTracking(_session, ovrTrackingCap_Orientation |
                                  ovrTrackingCap_MagYawCorrection |
                                  ovrTrackingCap_Position, 0);
#endif

  cerr << hex << "connected controller types: 0x" << ovr_GetConnectedControllerTypes(_session) << dec << "\n";
}

/**
 *
 */
OculusHmd::
~OculusHmd() {
  cerr << "destroynig session\n";
  ovr_Destroy(_session);
}

/**
 * Ensures the library has been initialized.
 */
bool OculusHmd::
initialize() {
  static bool initialized = false;
  if (initialized) {
    return true;
  }

  ovrInitParams params;
  params.Flags = ovrInit_Debug;
  params.RequestedMinorVersion = 0;
  params.LogCallback = &oculus_log;
  params.ConnectionTimeoutMS = 0;

#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 6
  ovrResult result = ovr_Initialize(&params);
  initialized = OVR_SUCCESS(result);

  if (!initialized) {
    ovrErrorInfo info;
    ovr_GetLastErrorInfo(&info);
    oculus_cat.error() << "Initialization failed: " << info.ErrorString
                       << " (" << result << ")\n";
  }
#else
  initialized = (ovr_Initialize(&params) != 0);
#endif
  return initialized;
}

/**
 * Creates the session object.  Returns true on success.
 */
bool OculusHmd::
create_session() {
  ovrGraphicsLuid luid;
  if (!OVR_SUCCESS(ovr_Create(&_session, &luid))) {
    oculus_cat.error()
      << "poll: failed to create Oculus session.\n";
    return false;
  }
  nassertr(_session != NULL, false);

  _desc = ovr_GetHmdDesc(_session);
  _name = _desc.ProductName;
  _product_id = _desc.ProductId;
  _vendor_id = _desc.VendorId;
  _manufacturer = _desc.Manufacturer;
  _serial_number = _desc.SerialNumber;

  ovr_SetTrackingOriginType(_session, ovrTrackingOrigin_FloorLevel);
  return true;
}

/**
 * Detects and returns the number of HMDs.
 */
int OculusHmd::
detect() {
#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 8
   ovrDetectResult result = ovr_Detect(0);
   return (int)result.IsOculusHMDConnected;

#elif OVR_MAJOR_VERSION >= 7
  if (!initialize()) {
    return 0;
  }
  ovrHmdDesc desc = ovr_GetHmdDesc(NULL);
  return (desc.Type != 0);

#else
  if (!initialize()) {
    return 0;
  }
  return ovrHmd_Detect();
#endif
}

/**
 * Returns the HMD with the given index, which is a number in the range
 * [0...detect()-1].
 */
OculusHmd *OculusHmd::
create(int index) {
  if (!initialize()) {
    return 0;
  }

#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 7
#if OVR_PRODUCT_VERSION >= 1
  ovrSession hmd;
#else
  ovrHmd hmd;
#endif
  ovrGraphicsLuid luid;
  if (index != 0 || OVR_FAILURE(ovr_Create(&hmd, &luid))) {
    return false;
  }
#elif OVR_MAJOR_VERSION >= 6
  ovrHmd hmd;
  if (!OVR_SUCCESS(ovrHmd_Create(index, &hmd))) {
    return false;
  }
#else
  ovrHmd hmd = ovrHmd_Create(index);
  if (hmd == NULL) {
    return NULL;
  }
#endif
  return new OculusHmd(hmd);
}

/**
 * Returns a new 'fake' HMD, useful for debugging.
 */
OculusHmd *OculusHmd::
create_debug(HmdType type) {
#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 7
  // This functionality is no longer available.
  return NULL;

#elif OVR_MAJOR_VERSION >= 6
  ovrHmd hmd;
  if (!OVR_SUCCESS(ovrHmd_Create((ovrHmdType) type, &hmd))) {
    return NULL;
  }
  return new OculusHmd(hmd);

#else
  ovrHmd hmd = ovrHmd_CreateDebug((ovrHmdType) type);
  if (hmd == NULL) {
    return NULL;
  }

  return new OculusHmd(hmd);
#endif
}

/**
 * Polls the input device for new activity, to ensure it contains the latest
 * events.  This will only have any effect for some types of input devices;
 * others may be updated automatically, and this method will be a no-op.
 */
void OculusHmd::
do_poll() {
  //nassertv(_session != NULL);
  if (_session == NULL) {
    ovrGraphicsLuid luid;
    if (!OVR_SUCCESS(ovr_Create(&_session, &luid))) {
      oculus_cat.error()
        << "poll: failed to create Oculus session.\n";
      return;
    }
    nassertv(_session != NULL);
    _desc = ovr_GetHmdDesc(_session);
    ovr_SetTrackingOriginType(_session, ovrTrackingOrigin_FloorLevel);
    cerr << "CREATING OVR SESSION WAS OKAY!\n";
  }

  // Check whether we are still connected.
  ovrSessionStatus status;
  ovrResult result = ovr_GetSessionStatus(_session, &status);
  if ((status.HmdPresent != 0) != _is_connected) {
    InputDeviceManager *mgr = InputDeviceManager::get_global_ptr();

    if (status.HmdPresent != 0) {
      mgr->add_device(this);
      _is_connected = true;
    } else {
      mgr->remove_device(this);
      _is_connected = false;
    }
  }

  if (!_is_connected) {
    return;
  }

  // When do we expect to display this frame?
  int frame = ClockObject::get_global_clock()->get_frame_count();

#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 8
  double time = ovr_GetPredictedDisplayTime(_session, frame);
#elif OVR_MAJOR_VERSION >= 6
  double time = ovr_GetFrameTiming(_session, frame).DisplayMidpointSeconds;
#else
  double time = ovr_GetFrameTiming(_session, frame).ScanoutMidpointSeconds;
#endif

  // Obtain the predicted pose.
#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 8
  _tracking_state = ovr_GetTrackingState(_session, time, ovrFalse);
#else
  _tracking_state = ovr_GetTrackingState(_session, time);
#endif

  //cerr << "tracking: 0x" << hex << _tracking_state.StatusFlags << dec << "\n";

  _sample_time = ovr_GetTimeInSeconds();
  ovrPosef pose = _tracking_state.HeadPose.ThePose;

  // Don't forget to convert to Panda's coordinate system.
  LPoint3 pos(pose.Position.x, -pose.Position.z, pose.Position.y);
  LOrientation orient(pose.Orientation.w, pose.Orientation.x,
                     -pose.Orientation.z, pose.Orientation.y);
  set_tracker(pos, orient, _tracking_state.HeadPose.TimeInSeconds);

  // Check if any of the peripherals were connected or disconnected.
  unsigned int connected = ovr_GetConnectedControllerTypes(_session);
  if (connected != _connected_types) {
    unsigned int changed = connected ^ _connected_types;
    _connected_types = connected;

    InputDeviceManager *mgr = InputDeviceManager::get_global_ptr();

    if (changed & ovrControllerType_Remote) {
      if (connected & ovrControllerType_Remote) {
        // The remote was just connected.
        if (_remote.is_null()) {
          // If we don't already have one, create a fake device to represent
          // the Oculus remote.
          _remote = new InputDevice("Oculus Remote", DC_remote_control, 0);
        }
        mgr->add_device(_remote);
      } else {
        mgr->remove_device(_remote);
      }
    }

    if (changed & ovrControllerType_LTouch) {
      if (connected & ovrControllerType_LTouch) {
        // The left touch controller was just connected.
        if (_left_touch.is_null()) {
          _left_touch = new OculusController(this, "Oculus Touch (Left)", DC_left_hand);
        }
        mgr->add_device(_left_touch);
      } else {
        mgr->remove_device(_left_touch);
      }
    }

    if (changed & ovrControllerType_RTouch) {
      if (connected & ovrControllerType_RTouch) {
        if (_right_touch.is_null()) {
          _right_touch = new OculusController(this, "Oculus Touch (Right)", DC_right_hand);
        }
        mgr->add_device(_right_touch);
      } else {
        mgr->remove_device(_right_touch);
      }
    }
  }

  if (connected & ovrControllerType_LTouch) {
    _left_touch->got_pose_state(_tracking_state.HandPoses[ovrHand_Left],
                                _tracking_state.HandStatusFlags[ovrHand_Left]);
  }

  if (connected & ovrControllerType_RTouch) {
    _right_touch->got_pose_state(_tracking_state.HandPoses[ovrHand_Right],
                                 _tracking_state.HandStatusFlags[ovrHand_Right]);
  }
}

/**
 * Opens a window that can be used to render into this head-mounted display.
 */
GraphicsWindow *OculusHmd::
open_window(GraphicsEngine *engine, GraphicsPipe *pipe,
            const string &name, int sort,
            const FrameBufferProperties &fb_prop,
            const WindowProperties &win_prop) {

  // Make sure we have a session.
  if (_session == NULL) {
    ovrGraphicsLuid luid;
    if (OVR_FAILURE(ovr_Create(&_session, &luid))) {
      oculus_cat.error()
        << "Failed to create Oculus session.\n";
      return NULL;
    }
    nassertr(_session != NULL, NULL);
    _desc = ovr_GetHmdDesc(_session);
    ovr_SetTrackingOriginType(_session, ovrTrackingOrigin_FloorLevel);
  }

  //FrameBufferProperties new_fbp(fb_prop);
  //new_fbp.set_back_buffers(1);

  PT(GraphicsWindow) win = new OculusGLGraphicsWindow(engine, pipe, name, fb_prop,
    win_prop, GraphicsPipe::BF_require_window, NULL, NULL, this);

  if (win != NULL) {
    engine->add_window(win, 0);
  }

  return win;
}

/**
 *
 */
LVecBase2i OculusHmd::
get_fov_texture_size(int i) const {
  const ovrEyeType eyes[2] = {ovrEye_Left, ovrEye_Right};
  ovrSizei size = ovr_GetFovTextureSize(_session, eyes[i], get_default_eye_fov(i), 1.0f);
  return LVecBase2i(size.w, size.h);
}

/**
 * Requests to dismiss the health and safety warning at the earliest possible
 * time, which may be seconds into the future due to display longevity
 * requirements.  This should only be called based on user interaction.
 *
 * This method will probably go away soon, as the Oculus 0.6.0 SDK automates
 * the closing of the HSW display and removes this method.
 */
bool OculusHmd::
dismiss_hsw_display() {
#if OVR_PRODUCT_VERSION == 0 && OVR_MAJOR_VERSION < 6
  return (ovr_DismissHSWDisplay(_session) != ovrFalse);
#else
  return true;
#endif
}

/**
 * Cycles between layer HUD modes.  Useful for binding to a key for debugging.
 */
void OculusHmd::
cycle_layer_hud() {
  int mode = ovr_GetInt(_session, OVR_LAYER_HUD_MODE, (int)ovrLayerHud_Off);

  if (mode == (int)ovrLayerHud_Off) {
    // Enable the layer HUD.
    ovr_SetInt(_session, OVR_LAYER_HUD_MODE, (int)ovrLayerHud_Info);
    ovr_SetInt(_session, OVR_LAYER_HUD_CURRENT_LAYER, 0);
  } else {
    // Cycle through the layers until we get to layer 16.
    int layer = ovr_GetInt(_session, OVR_LAYER_HUD_CURRENT_LAYER, 0);
    ++layer;
    if (layer >= (int)ovrMaxLayerCount) {
      ovr_SetInt(_session, OVR_LAYER_HUD_MODE, (int)ovrLayerHud_Off);
      ovr_SetInt(_session, OVR_LAYER_HUD_CURRENT_LAYER, 0);
    } else {
      ovr_SetInt(_session, OVR_LAYER_HUD_CURRENT_LAYER, layer);
    }
  }
}

/**
 * Returns a render description for the given eye and FOV port.
 */
ovrEyeRenderDesc OculusHmd::
get_render_desc(ovrEyeType eye_type, ovrFovPort fov) const {
  return ovr_GetRenderDesc(_session, eye_type, fov);
}

/**
 * Returns the current performance HUD mode.
 */
int OculusHmd::
get_perf_hud_mode() const {
  return ovr_GetInt(_session, OVR_PERF_HUD_MODE, (int)ovrPerfHud_Off);
}

/**
 * Returns the current layer HUD mode.
 */
int OculusHmd::
get_layer_hud_mode() const {
  return ovr_GetInt(_session, OVR_LAYER_HUD_MODE, (int)ovrLayerHud_Off);
}

/**
 * Returns the current layer HUD index.
 */
int OculusHmd::
get_layer_hud_current_layer() const {
  return ovr_GetInt(_session, OVR_LAYER_HUD_CURRENT_LAYER, 0);
}

/**
 * Returns the current debug HUD stereo mode.
 */
int OculusHmd::
get_debug_hud_stereo_mode() const {
  return ovr_GetInt(_session, OVR_DEBUG_HUD_STEREO_MODE, (int)ovrDebugHudStereo_Off);
}

/**
 * Sets the current performance HUD mode.
 */
void OculusHmd::
set_perf_hud_mode(int mode) {
  ovr_SetInt(_session, OVR_PERF_HUD_MODE, mode);
}

/**
 * Sets the current layer HUD mode.
 */
void OculusHmd::
set_layer_hud_mode(int mode) {
  ovr_SetInt(_session, OVR_LAYER_HUD_MODE, mode);
}

/**
 * Sets the current layer HUD index.
 */
void OculusHmd::
set_layer_hud_current_layer(int current_layer) {
  ovr_SetInt(_session, OVR_LAYER_HUD_CURRENT_LAYER, current_layer);
}

/**
 * Sets the current debug HUD stereo mode.
 */
void OculusHmd::
set_debug_hud_stereo_mode(int mode) {
  ovr_SetInt(_session, OVR_DEBUG_HUD_STEREO_MODE, mode);
}

/**
 * Creates a swap chain with the given size.
 */
bool OculusHmd::
create_texture_swap_chain_gl(int width, int height, ovrTextureSwapChain &chain) {
#if OVR_PRODUCT_VERSION >= 1
  ovrTextureFormat format = OVR_FORMAT_R8G8B8A8_UNORM_SRGB;
#elif OVR_MAJOR_VERSION >= 7
  GLenum format = GL_SRGB8_ALPHA8;
#else
  GLenum format = GL_RGBA8;
#endif

#if OVR_PRODUCT_VERSION >= 1
  ovrTextureSwapChainDesc desc = {};
  desc.Type = ovrTexture_2D;
  desc.ArraySize = 1;
  desc.Format = format;
  desc.Width = width;
  desc.Height = height;
  desc.MipLevels = 1;
  desc.SampleCount = 1;
  desc.StaticImage = ovrFalse;
  return OVR_SUCCESS(ovr_CreateTextureSwapChainGL(_session, &desc, &chain));
#else
  return OVR_SUCCESS(ovr_CreateSwapTextureSetGL(_session, format, width, height, &chain));
#endif
}

/**
 * Destroys a swap chain previously created using create_texture_swap_chain_gl.
 */
void OculusHmd::
destroy_texture_swap_chain(ovrTextureSwapChain &chain) {
#if OVR_PRODUCT_VERSION >= 1
  ovr_DestroyTextureSwapChain(_session, chain);
#else
  ovr_DestroySwapTextureSet(_session, chain);
#endif
}
