/**
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * @file oculusHmd.h
 * @author rdb
 * @date 2014-03-26
 */

#ifndef OCULUSHMD_H
#define OCULUSHMD_H

#include "pandabase.h"
#include "config_oculus.h"
#include "inputDevice.h"
#include "frameBufferProperties.h"
#include "graphicsEngine.h"
#include "graphicsPipe.h"
#include "graphicsWindow.h"
#include "windowProperties.h"
#include "inputDevice.h"
#include "oculusController.h"

#include "OVR_CAPI.h"

#if OVR_PRODUCT_VERSION < 1
typedef ovrSwapTextureSet *ovrTextureSwapChain;
#endif

/**
 * Represents an Oculus Rift head-mounted display.
 */
class EXPCL_OCULUS OculusHmd : public InputDevice {
protected:
  OculusHmd();

#if OVR_PRODUCT_VERSION >= 1
  OculusHmd(ovrSession session);
#else
  OculusHmd(ovrHmd hmd);
#endif

  static bool initialize();

  bool create_session();

PUBLISHED:
  ~OculusHmd();

  typedef int HmdType;
  //typedef ovrHmdCaps HmdCaps;
  //typedef ovrDistortionCaps HmdDistortionCaps;

  static int detect();
  static OculusHmd *create(int index);
  static OculusHmd *create_debug(HmdType type);

  virtual void do_poll();

  GraphicsWindow *open_window(GraphicsEngine *engine, GraphicsPipe *pipe,
                              const string &name, int sort,
                              const FrameBufferProperties &fb_prop,
                              const WindowProperties &win_prop);

  LVecBase2i get_fov_texture_size(int i) const;

  bool dismiss_hsw_display();
  void cycle_layer_hud();

public:
  INLINE short get_firmware_major() const;
  INLINE short get_firmware_minor() const;

  INLINE ovrFovPort get_default_eye_fov(int i) const;
  INLINE ovrFovPort get_max_eye_fov(int i) const;
  ovrEyeRenderDesc get_render_desc(ovrEyeType eye_type, ovrFovPort fov) const;

  INLINE LVecBase2i get_resolution() const;
  INLINE LVecBase2i get_windows_pos() const;

  int get_perf_hud_mode() const;
  int get_layer_hud_mode() const;
  int get_layer_hud_current_layer() const;
  int get_debug_hud_stereo_mode() const;

  void set_perf_hud_mode(int mode);
  void set_layer_hud_mode(int mode);
  void set_layer_hud_current_layer(int layer);
  void set_debug_hud_stereo_mode(int mode);

PUBLISHED:
  MAKE_PROPERTY(firmware_major, get_firmware_major);
  MAKE_PROPERTY(firmware_minor, get_firmware_minor);

  MAKE_PROPERTY(resolution, get_resolution);

  MAKE_PROPERTY(perf_hud_mode, get_perf_hud_mode, set_perf_hud_mode);
  MAKE_PROPERTY(layer_hud_mode, get_layer_hud_mode, set_layer_hud_mode);
  MAKE_PROPERTY(layer_hud_current_layer, get_layer_hud_current_layer, set_layer_hud_current_layer);
  MAKE_PROPERTY(debug_hud_stereo_mode, get_debug_hud_stereo_mode, set_debug_hud_stereo_mode);

/*
  INLINE int get_hmd_caps() const;
  INLINE int get_tracking_caps() const;
  INLINE int get_distortion_caps() const;


  INLINE const char *get_last_error();
  INLINE int get_enabled_caps();
  INLINE void set_enabled_caps(int hmd_caps);
*/

private:
  bool create_texture_swap_chain_gl(int width, int height, ovrTextureSwapChain &chain);
  void destroy_texture_swap_chain(ovrTextureSwapChain &chain);

protected:
#if OVR_PRODUCT_VERSION >= 1
  ovrSession _session;
#else
  ovrHmd _session;
#endif
  ovrHmdDesc _desc;
  ovrTrackingState _tracking_state;
  double _sample_time;
  unsigned int _connected_types;
  PT(InputDevice) _remote;
  PT(OculusController) _left_touch;
  PT(OculusController) _right_touch;

  friend EXPCL_OCULUS int scan_devices_p3oculus();
  friend class OculusController;
  friend class OculusGLGraphicsWindow;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    InputDevice::init_type();
    register_type(_type_handle, "OculusHmd",
                  InputDevice::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

INLINE ostream &operator << (ostream &out, const OculusHmd &hmd) {
  hmd.output(out);
  return out;
}

#include "oculusHmd.I"

#endif
