/**
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * @file oculusGLGraphicsWindow.h
 * @author rdb
 * @date 2014-08-17
 */

#ifndef OCULUSGLGRAPHICSWINDOW_H
#define OCULUSGLGRAPHICSWINDOW_H

#include "pandabase.h"
#include "config_oculus.h"
#include "luse.h"
#include "graphicsBuffer.h"
#include "oculusHmd.h"

#if defined(OVR_OS_WIN32)
#include "wglGraphicsWindow.h"
typedef wglGraphicsWindow BaseGraphicsWindow;
#elif defined(OVR_OS_LINUX)
#include "glxGraphicsWindow.h"
typedef glxGraphicsWindow BaseGraphicsWindow;
#elif defined(OVR_OS_MAC)
#include "cocoaGraphicsWindow.h"
typedef CocoaGraphicsWindow BaseGraphicsWindow;
#else
#error Unsupported operating system for OculusVR library!
#endif

#ifdef OVR_OS_LINUX
#include "pre_x11_include.h"
#endif
#include "OVR_CAPI.h"
#include "OVR_CAPI_GL.h"
#ifdef OVR_OS_LINUX
#include "post_x11_include.h"
#endif

#include <GL/gl.h>

/**
 * This window represents a single Oculus Rift display rendered to via OpenGL.
 */
class EXPCL_OCULUS OculusGLGraphicsWindow : public BaseGraphicsWindow {
public:
  OculusGLGraphicsWindow(GraphicsEngine *engine, GraphicsPipe *pipe,
                         const string &name,
                         const FrameBufferProperties &fb_prop,
                         const WindowProperties &win_prop,
                         int flags, GraphicsStateGuardian *gsg,
                         GraphicsOutput *host, OculusHmd *hmd);
  virtual ~OculusGLGraphicsWindow();

  virtual bool begin_frame(FrameMode mode, Thread *current_thread);
  virtual void clear(Thread *current_thread);
  virtual void change_scenes(DisplayRegionPipelineReader *new_dr);
  virtual bool begin_scene();
  virtual void end_scene();
  virtual void end_frame(FrameMode mode, Thread *current_thread);

  virtual void begin_flip();
  virtual void ready_flip();
  virtual void end_flip();

  virtual bool supports_pixel_zoom() const;

protected:
  virtual void close_window();
  virtual bool open_window();

  virtual bool do_reshape_request(int x_origin, int y_origin, bool has_origin,
                                  int x_size, int y_size);

private:
  PT(OculusHmd) _hmd;
  GLuint _fbo;
  GLuint _depth_rbo;

  ovrEyeRenderDesc _render_desc[2];

#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 8
  // Stores the current status.
  ovrSessionStatus _status;
#endif

#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 6
  typedef pvector<ovrLayer_Union> Layers;
  Layers _layers;
  size_t _layer_index;
  pvector<ovrLayerHeader *> _layer_ptrs;
#else
  ovrGLTexture _textures[2];
#endif

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    BaseGraphicsWindow::init_type();
    register_type(_type_handle, "OculusGLGraphicsWindow",
                  BaseGraphicsWindow::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#endif
