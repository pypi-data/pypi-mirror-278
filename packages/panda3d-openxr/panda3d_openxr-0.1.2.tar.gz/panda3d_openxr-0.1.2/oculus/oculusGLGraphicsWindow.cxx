/**
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * @file oculusGLGraphicsWindow.cxx
 * @author rdb
 * @date 2014-08-17
 */

#include "oculusGLGraphicsWindow.h"
#include "glgsg.h"
#include "graphicsEngine.h"
#include "throw_event.h"

#if OVR_PRODUCT_VERSION == 0 && OVR_MAJOR_VERSION < 7
#define ovr_BeginEyeRender ovrHmd_BeginEyeRender
#define ovr_BeginFrame ovrHmd_BeginFrame
#define ovr_CreateSwapTextureSetGL ovrHmd_CreateSwapTextureSetGL
#define ovr_DestroySwapTextureSet ovrHmd_DestroySwapTextureSet
#define ovr_EndEyeRender ovrHmd_EndEyeRender
#define ovr_EndFrame ovrHmd_EndFrame
#define ovr_GetRenderDesc ovrHmd_GetRenderDesc
#define ovr_SubmitFrame ovrHmd_SubmitFrame
#endif

#if OVR_PRODUCT_VERSION == 0
#define HmdToEyeOffset HmdToEyeViewOffset
#define ovr_GetTextureSwapChainCurrentIndex(session, chain, index) {\
  *(index) = (chain)->CurrentIndex;\
}
#define ovr_CommitTextureSwapChain(session, chain, index) {\
  (chain)->CurrentIndex = ((chain)->CurrentIndex + 1) % (chain)->TextureCount;\
}
#define ovr_GetTextureSwapChainBufferGL(session, chain, index, out_TexId) {\
  *(out_TexId) = ((ovrGLTexture &)(chain)->Textures[(chain)->CurrentIndex]).OGL.TexId;\
}
#else
// Since SDK 1, right-handed is the default.
#define ovrProjection_RightHanded 0
#endif

TypeHandle OculusGLGraphicsWindow::_type_handle;

/**
 * Creates a window used for rendering to the given HMD.
 */
OculusGLGraphicsWindow::
OculusGLGraphicsWindow(GraphicsEngine *engine, GraphicsPipe *pipe,
                       const string &name,
                       const FrameBufferProperties &fb_prop,
                       const WindowProperties &win_prop,
                       int flags,
                       GraphicsStateGuardian *gsg,
                       GraphicsOutput *host,
                       OculusHmd *hmd) :
  BaseGraphicsWindow(engine, pipe, name, fb_prop, win_prop, flags, gsg, host),
  _hmd(hmd),
  _status(),
  _fbo(0),
  _depth_rbo(0)
{
  WindowProperties initial;
  initial.set_undecorated(true);
  //initial.set_fullscreen(true);
  initial.set_minimized(false);
  initial.set_origin(_hmd->get_windows_pos());
  initial.set_size(_hmd->get_resolution());
  initial.set_fixed_size(true);
  initial.set_foreground(true);

  request_properties(initial);

#ifdef OVR_OS_LINUX
  // Magic flag that basically flips off the window manager, letting us have
  // full control over window positioning.
  _override_redirect = True;
#endif

#if OVR_PRODUCT_VERSION == 0 && OVR_MAJOR_VERSION < 6
  _textures[0].OGL.Header.API = ovrRenderAPI_OpenGL;
  _textures[1].OGL.Header.API = ovrRenderAPI_OpenGL;

  // We are actually drawing into a buffer, not into our window, so we should
  // not draw to GL_BACK.
  _draw_buffer_type = RenderBuffer::T_front;
#endif
}

/**
 *
 */
OculusGLGraphicsWindow::
~OculusGLGraphicsWindow() {
}

/**
 * This function will be called within the draw thread before beginning
 * rendering for a given frame.  It should do whatever setup is required, and
 * return true if the frame should be rendered, or false if it should be
 * skipped.
 */
bool OculusGLGraphicsWindow::
begin_frame(FrameMode mode, Thread *current_thread) {
#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 8
  if (mode == FM_render) {
    // Check whether the Rift is still plugged in.
    ovrSessionStatus status;
    ovrResult result = ovr_GetSessionStatus(_hmd->_session, &status);
    if (result == ovrError_ServiceConnection) {
      // Connection was broken.
      oculus_cat.warning() << "Service connection was lost.\n";
      //ovr_Destroy(_hmd->_session);
      //_hmd->_session = 0;

      //InputDeviceManager *mgr = InputDeviceManager::get_global_ptr();
      //mgr->remove_device(this);
    } else if (result != ovrSuccess) {
      return false;
    }

    // If the status changed, show a helpful message informing us of this.
    if (oculus_cat.is_info()) {
      if (memcmp(&status, &_status, sizeof(ovrSessionStatus)) != 0) {
        oculus_cat.info() << "Session status changed:";
#if OVR_PRODUCT_VERSION > 0
        if (status.IsVisible) {
          oculus_cat.info(false) << " IsVisible";
        }
#else
        if (status.HasVrFocus) {
          oculus_cat.info(false) << " HasVrFocus";
        }
#endif
        if (status.HmdPresent) {
          oculus_cat.info(false) << " HmdPresent";
        }
#if OVR_PRODUCT_VERSION > 0
        if (status.HmdMounted) {
          oculus_cat.info(false) << " HmdMounted";
        }
        if (status.DisplayLost) {
          oculus_cat.info(false) << " DisplayLost";
        }
        if (status.ShouldQuit) {
          oculus_cat.info(false) << " ShouldQuit";
        }
        if (status.ShouldRecenter) {
          oculus_cat.info(false) << " ShouldRecenter";
        }
#endif
        oculus_cat.info(false) << endl;
      }
    }

    if ((status.HmdPresent != 0) != _hmd->is_connected()) {
      InputDeviceManager *mgr = InputDeviceManager::get_global_ptr();
      if (status.HmdPresent) {
        mgr->add_device(_hmd);
        _hmd->set_connected(true);
      } else {
        mgr->remove_device(_hmd);
        _hmd->set_connected(false);
      }
    }

    // Indicate in the WindowProperties whether we have focus in VR.
#if OVR_PRODUCT_VERSION > 0
    if ((status.IsVisible != 0) != _properties.get_foreground()) {
      WindowProperties properties;
      properties.set_foreground(status.IsVisible != 0);
      system_changed_properties(properties);
    }
#else
    if ((status.HasVrFocus != 0) != _properties.get_foreground()) {
      WindowProperties properties;
      properties.set_foreground(status.HasVrFocus != 0);
      system_changed_properties(properties);
    }
#endif

#if OVR_PRODUCT_VERSION >= 1
    if (status.ShouldQuit && !_status.ShouldQuit) {
      oculus_cat.info() << "Received shutdown request.\n";

      // The user has requested to quit the application from Oculus Home.
      // We'll respond to this by closing the window, which will hopefully
      // quit the application (assuming it's the only window).
      close_window();
      WindowProperties properties;
      properties.set_open(false);
      system_changed_properties(properties);
      _status = status;
      return false;
    }
#endif
    _status = status;

#if OVR_PRODUCT_VERSION > 0
    if (!status.IsVisible || !status.HmdMounted || !status.HmdPresent)
#else
    if (!status.HasVrFocus || !status.HmdPresent)
#endif
    {
      // Skip the render if the Panda window is not currently visible or if
      // the user isn't currently wearing the headset.
      return false;
    }
  }
#endif

  GLGraphicsStateGuardian *glgsg;
  DCAST_INTO_R(glgsg, _gsg, false);

  if (!BaseGraphicsWindow::begin_frame(mode, current_thread)) {
    return false;
  }

  if (mode == FM_render) {
    ClockObject *clock = ClockObject::get_global_clock();

    /*if (!_visible) {
      // If we skipped last frame due to the Rift being invisible, resubmit
      // the last frame.  If this succeeds, then we know it's visible again.
      int frame = clock->get_frame_count();
      if (ovr_SubmitFrame(_hmd->_session, frame, NULL, &_layer_ptrs[0], _layer_ptrs.size()) == ovrSuccess) {
        _visible = true;
      } else {
        return false;
      }
    }*/

    glgsg->bind_fbo(_fbo);

#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 6
    // Start with no layers.
    _layer_ptrs.clear();
    _layer_index = -1;

    size_t active_layers = get_num_display_regions();
    if (active_layers > _layers.size()) {
      ovrLayer_Union fill;
      fill.Header.Type = ovrLayerType_Disabled;
      fill.Header.Flags = 0;
      _layers.resize(active_layers, fill);
    }

#else
    // Indicate to LibOVR that we are about to begin drawing.  This
    // is necessary for it to lock in timing information.
    ovr_BeginFrame(_hmd->_session, clock->get_frame_count(current_thread));
#if OVR_MAJOR_VERSION < 4
    ovr_BeginEyeRender(_hmd->_session, ovrEye_Left);
    ovr_BeginEyeRender(_hmd->_session, ovrEye_Right);
#endif
#endif
  }

  return true;
}

/**
 * Clears the entire framebuffer before rendering, according to the settings
 * of get_color_clear_active() and get_depth_clear_active() (inherited from
 * DrawableRegion).
 *
 * This function is called only within the draw thread.
 */
void OculusGLGraphicsWindow::
clear(Thread *current_thread) {
  // The default implementation of clear() prepares the overlay DisplayRegion,
  // but that would not clear the proper thing here.  Do nothing for now.
  return BaseGraphicsWindow::clear(current_thread);
}

/**
 * Called by the GraphicsEngine when the window is about to change to another
 * DisplayRegion.  This exists mainly to provide a callback for switching the
 * cube map face, if we are rendering to the different faces of a cube map.
 */
void OculusGLGraphicsWindow::
change_scenes(DisplayRegionPipelineReader *new_dr) {
  DisplayRegion *region = new_dr->get_object();
  Lens::StereoChannel channel = new_dr->get_stereo_channel();

  ovrLayerType type;
  if (channel == Lens::SC_stereo) {
    type = ovrLayerType_EyeFov;
  } else {
#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 8
    type = ovrLayerType_Quad;
#else
    type = ovrLayerType_QuadHeadLocked;
#endif
  }

  ++_layer_index;
  nassertv(_layer_index < _layers.size());
  ovrLayer_Union &layer = _layers[_layer_index];

  if (type == ovrLayerType_EyeFov) {
    // We need to tell the Rift which pose we used for rendering.  This allows
    // it to perform timewarp: it reprojects the image based on how much the
    // image has moved in the meantime.
    //TODO: make tracking origin configurable.
    CPT(TransformState) tracking_pose = new_dr->get_camera().get_net_transform();
    LPoint3 pos = tracking_pose->get_pos();
    LQuaternion quat = tracking_pose->get_quat();

    ovrPosef pose;
    pose.Orientation.x = quat[1];
    pose.Orientation.y = quat[3];
    pose.Orientation.z = -quat[2];
    pose.Orientation.w = quat[0];

    // It doesn't appear that the position matters, since the Rift appears to
    // ignore these.  However, it's probably good to specify these anyway, in
    // case they ever implement positional timewarp.
    pose.Position.x = pos[0];
    pose.Position.y = pos[2];
    pose.Position.z = -pos[1];

    // I'm not quite sure why the Rift expects two poses - are we supposed to
    // add the hmd-to-eye offsets?
    layer.EyeFov.RenderPose[0] = pose;
    layer.EyeFov.RenderPose[1] = pose;

    // The FOV we used to render the layer.  Right now, we force the
    // recommended FOV ports, so just copy those.
    layer.EyeFov.Fov[0] = _render_desc[0].Fov;
    layer.EyeFov.Fov[1] = _render_desc[1].Fov;

#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 8
    // When we recorded the tracking state - useful for latency tracking.
    layer.EyeFov.SensorSampleTime = _hmd->_sample_time;
#endif
  }

  if (layer.Header.Type != type) {
    // Recreate the texture set for this display region.
    // First destroy the previous, if any.
    if (layer.Header.Type == ovrLayerType_EyeFov) {
      _hmd->destroy_texture_swap_chain(layer.EyeFov.ColorTexture[0]);
      _hmd->destroy_texture_swap_chain(layer.EyeFov.ColorTexture[1]);
    } else if (layer.Header.Type != ovrLayerType_Disabled) {
      _hmd->destroy_texture_swap_chain(layer.Quad.ColorTexture);
    }

    layer.Header.Type = type;
    layer.Header.Flags = ovrLayerFlag_TextureOriginAtBottomLeft;
    int width = int(new_dr->get_pixel_width() * region->get_pixel_factor());
    int height = int(new_dr->get_pixel_height() * region->get_pixel_factor());

    ovrRecti viewport = {0, 0, width, height};
    if (type == ovrLayerType_EyeFov) {
      if (oculus_cat.is_debug()) {
        oculus_cat.debug()
          << "creating " << width << "x" << height << " stereo texture swap chain for layer " << _layer_index << "\n";
      }
      layer.EyeFov.Viewport[0] = viewport;
      layer.EyeFov.Viewport[1] = viewport;
      _hmd->create_texture_swap_chain_gl(width, height, layer.EyeFov.ColorTexture[0]);
      _hmd->create_texture_swap_chain_gl(width, height, layer.EyeFov.ColorTexture[1]);
    } else {
      if (oculus_cat.is_debug()) {
        oculus_cat.debug()
          << "creating " << width << "x" << height << " mono texture swap chain for layer " << _layer_index << "\n";
      }
      layer.Header.Flags |= ovrLayerFlag_HeadLocked;
      layer.Quad.Viewport = viewport;
      layer.Quad.QuadSize.x = new_dr->get_right() - new_dr->get_left();
      layer.Quad.QuadSize.y = new_dr->get_top() - new_dr->get_bottom();
      layer.Quad.QuadPoseCenter.Position.x = 0.00f;
      layer.Quad.QuadPoseCenter.Position.y = 0.0f;
      layer.Quad.QuadPoseCenter.Position.z = -0.50f;
      layer.Quad.QuadPoseCenter.Orientation.x = 0;
      layer.Quad.QuadPoseCenter.Orientation.y = 0;
      layer.Quad.QuadPoseCenter.Orientation.z = 0;
      layer.Quad.QuadPoseCenter.Orientation.w = 1;
      _hmd->create_texture_swap_chain_gl(width, height, layer.Quad.ColorTexture);
    }
  }

  GLGraphicsStateGuardian *glgsg;
  DCAST_INTO_V(glgsg, _gsg);

  if (type == ovrLayerType_EyeFov) {
    int index0, index1;
    ovr_GetTextureSwapChainCurrentIndex(_hmd->_session, layer.EyeFov.ColorTexture[0], &index0);
    ovr_GetTextureSwapChainCurrentIndex(_hmd->_session, layer.EyeFov.ColorTexture[1], &index1);

    // Get the textures we must bind this frame.
    unsigned int tex0, tex1;
    ovr_GetTextureSwapChainBufferGL(_hmd->_session, layer.EyeFov.ColorTexture[0], index0, &tex0);
    ovr_GetTextureSwapChainBufferGL(_hmd->_session, layer.EyeFov.ColorTexture[1], index1, &tex1);

    // Bind the textures to the FBO.
    glgsg->_glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex0, 0);
    glgsg->_glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_TEXTURE_2D, tex1, 0);

    _fb_properties.set_stereo(true);
  } else {
    int index;
    ovr_GetTextureSwapChainCurrentIndex(_hmd->_session, layer.Quad.ColorTexture, &index);

    // Get the textures we must bind this frame.
    unsigned int tex;
    ovr_GetTextureSwapChainBufferGL(_hmd->_session, layer.Quad.ColorTexture, index, &tex);

    // Bind the texture to the FBO.
    glgsg->_glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex, 0);
    glgsg->_glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_TEXTURE_2D, 0, 0);

    _fb_properties.set_stereo(false);
  }

  if (!region->get_clear_color_active()) {
    // If we had no color clear, clear it anyway, but with a transparent
    // color.  This is because unlike in the regular rendering pipeline, each
    // display region here is rendered to a separate texture.

    // This is a hack that should go away soon.
    glgsg->prepare_display_region(new_dr);

    const GLfloat zero[4] = {0.f, 0.f, 0.f, 0.f};
    glgsg->_glClearBufferfv(GL_COLOR, 0, zero);
    glgsg->_glClearBufferfv(GL_COLOR, 1, zero);
  }
}

/**
 * Called between begin_frame() and end_frame() to mark the beginning of
 * drawing commands for a "scene" (usually a particular DisplayRegion) within
 * a frame.  All 3-D drawing commands, except the clear operation, must be
 * enclosed within begin_scene() .. end_scene().
 * This must be called in the draw thread.
 *
 * The return value is true if successful (in which case the scene will be
 * drawn and end_scene() will be called later), or false if unsuccessful (in
 * which case nothing will be drawn and end_scene() will not be called).
 */
bool OculusGLGraphicsWindow::
begin_scene() {
  Lens::StereoChannel channel = _gsg->get_current_stereo_channel();
  nassertr(channel != Lens::SC_stereo, false);

  if (channel == Lens::SC_mono) {
    // For a mono region, we display the render results in a quad, so we
    // should not be creating a projection matrix.
    return BaseGraphicsWindow::begin_scene();
  }

  // For now, we let Oculus calculate the projection matrix of stereo regions.
  // It reduces the possibility of users messing up.
  const Lens *lens = _gsg->get_current_lens();
  PN_stdfloat nearf = lens->get_near();
  PN_stdfloat farf = lens->get_far();

  ovrHmdDesc &desc = _hmd->_desc;

  ovrEyeType eye = (ovrEyeType)(channel - 1);
  ovrMatrix4f m = ovrMatrix4f_Projection(desc.DefaultEyeFov[eye], nearf, farf, ovrProjection_ClipRangeOpenGL | ovrProjection_RightHanded);
  LMatrix4 mat = LMatrix4::translate_mat(-_render_desc[eye].HmdToEyeOffset.x, 0, 0)
               * LMatrix4(
    m.M[0][0], m.M[1][0], m.M[2][0], m.M[3][0],
    m.M[0][1], m.M[1][1], m.M[2][1], m.M[3][1],
    m.M[0][2], m.M[1][2], m.M[2][2], m.M[3][2],
    m.M[0][3], m.M[1][3], m.M[2][3], m.M[3][3]);

  _gsg->set_projection_mat(TransformState::make_mat(mat));

  return _gsg->begin_scene();
}

/**
 * Called between begin_frame() and end_frame() to mark the end of drawing
 * commands for a "scene" (usually a particular DisplayRegion) within a frame.
 * All 3-D drawing commands, except the clear operation, must be enclosed
 * within begin_scene() .. end_scene().
 */
void OculusGLGraphicsWindow::
end_scene() {
  _gsg->end_scene();

  Lens::StereoChannel channel = _gsg->get_current_stereo_channel();
  ovrLayer_Union &layer = _layers[_layer_index];

  // I'm not 100% sure this is required, but it can't hurt.
  GLGraphicsStateGuardian *glgsg;
  DCAST_INTO_V(glgsg, _gsg);
  glgsg->_glTextureBarrier();

  switch (channel) {
  case Lens::SC_mono:
    if (oculus_cat.is_spam()) {
      oculus_cat.spam()
        << "committing layer " << _layer_index << " mono\n";
    }
    ovr_CommitTextureSwapChain(_hmd->_session, layer.Quad.ColorTexture);
    break;

  case Lens::SC_left:
    if (oculus_cat.is_spam()) {
      oculus_cat.spam()
        << "committing layer " << _layer_index << " left\n";
    }
    ovr_CommitTextureSwapChain(_hmd->_session, layer.EyeFov.ColorTexture[0]);
    break;

  case Lens::SC_right:
    if (oculus_cat.is_spam()) {
      oculus_cat.spam()
        << "committing layer " << _layer_index << " right\n";
    }
    ovr_CommitTextureSwapChain(_hmd->_session, layer.EyeFov.ColorTexture[1]);
    break;
  }

  // Push it to the list of layers to submit at the end of the frame.
  if (_layer_ptrs.empty() || _layer_ptrs.back() != &layer.Header) {
    _layer_ptrs.push_back(&layer.Header);
  }
}

/**
 * This function will be called within the draw thread after rendering is
 * completed for a given frame.  It should do whatever finalization is
 * required.
 */
void OculusGLGraphicsWindow::
end_frame(FrameMode mode, Thread *current_thread) {
  if (mode == FM_render) {
    GLGraphicsStateGuardian *glgsg;
    DCAST_INTO_V(glgsg, _gsg);

    int frame = ClockObject::get_global_clock()->get_frame_count();

    // Tell LibOVR that we're done rendering.  It will now render the
    // appropriate distortion to the back buffer of the window and flip it.
#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 6
    if (oculus_cat.is_spam()) {
      oculus_cat.spam()
        << "submitting frame with " << _layer_ptrs.size() << " layers\n";
    }
    ovrResult result = ovr_SubmitFrame(_hmd->_session, frame, nullptr, &_layer_ptrs[0], _layer_ptrs.size());
    if (result != ovrSuccess) {
      //TODO: handle display lost.
      ovrErrorInfo info;
      ovr_GetLastErrorInfo(&info);
      oculus_cat.warning()
        << "submit failed with code " << result << ": " << info.ErrorString << "\n";
    }

#elif OVR_MAJOR_VERSION >= 4
    ovrHmd_EndFrame(_hmd->_session, poses, (ovrTexture *)_textures);

#else
    ovrHmd_EndEyeRender(_hmd->_session, ovrEye_Left, _poses[0], &_textures[0].Texture);
    ovrHmd_EndEyeRender(_hmd->_session, ovrEye_Right, _poses[1], &_textures[1].Texture);
    ovrHmd_EndFrame(_hmd->_session);
#endif
  }

  BaseGraphicsWindow::end_frame(mode, current_thread);
}

/**
 * This function will be called within the draw thread after end_frame() has
 * been called on all windows, to initiate the exchange of the front and back
 * buffers.
 *
 * This should instruct the window to prepare for the flip at the next video
 * sync, but it should not wait.
 *
 * We have the two separate functions, begin_flip() and end_flip(), to make it
 * easier to flip all of the windows at the same time.
 */
void OculusGLGraphicsWindow::
begin_flip() {
  // The Oculus Rift SDK takes care of flip in ovr_EndFrame.
}

/**
 * This function will be called within the draw thread after end_frame() has
 * been called on all windows, to initiate the exchange of the front and back
 * buffers.
 *
 * This should instruct the window to prepare for the flip when it is command
 * but not actually flip
 *
 */
void OculusGLGraphicsWindow::
ready_flip() {
  // The Oculus Rift SDK takes care of flip in ovr_EndFrame.
}

/**
 * This function will be called within the draw thread after begin_flip() has
 * been called on all windows, to finish the exchange of the front and back
 * buffers.
 *
 * This should cause the window to wait for the flip, if necessary.
 */
void OculusGLGraphicsWindow::
end_flip() {
}

/**
 * Returns true if a call to set_pixel_zoom() will be respected, false if it
 * will be ignored.  If this returns false, then get_pixel_factor() will
 * always return 1.0, regardless of what value you specify for
 * set_pixel_zoom().
 *
 * This may return false if the underlying renderer doesn't support pixel
 * zooming, or if you have called this on a DisplayRegion that doesn't have
 * both set_clear_color() and set_clear_depth() enabled.
 */
bool OculusGLGraphicsWindow::
supports_pixel_zoom() const {
  return true;
}

/**
 * Closes the window right now.  Called from the window thread.
 */
void OculusGLGraphicsWindow::
close_window() {
  if (!_gsg.is_null()) {
    GLGraphicsStateGuardian *glgsg;
    DCAST_INTO_V(glgsg, _gsg);
    glgsg->_glDeleteFramebuffers(1, &_fbo);
    _fbo = 0;
  }

  Layers::iterator it;
  for (it = _layers.begin(); it != _layers.end(); ++it) {
    ovrLayer_Union &layer = *it;
    switch (layer.Header.Type) {
    case ovrLayerType_EyeFov:
      _hmd->destroy_texture_swap_chain(layer.EyeFov.ColorTexture[0]);
      _hmd->destroy_texture_swap_chain(layer.EyeFov.ColorTexture[1]);
      break;

#if OVR_PRODUCT_VERSION > 0 || OVR_MAJOR_VERSION >= 8
    case ovrLayerType_Quad:
#else
    case ovrLayerType_QuadInWorld:
    case ovrLayerType_QuadHeadLocked:
#endif
      _hmd->destroy_texture_swap_chain(layer.Quad.ColorTexture);
      break;

    default:
      break;
    }
  }

  BaseGraphicsWindow::close_window();
}

/**
 * Opens the window right now.  Called from the window thread.
 * @return  true if the window is successfully opened, or false if there was a
 *          problem.
 */
bool OculusGLGraphicsWindow::
open_window() {
  // Open the base window first.  This will give us our context.
  if (!BaseGraphicsWindow::open_window()) {
    return false;
  }

  nassertr(!_gsg.is_null(), false);

  GLGraphicsStateGuardian *glgsg;
  DCAST_INTO_R(glgsg, _gsg, false);

  if (!glgsg->_supports_framebuffer_object) {
    oculus_cat.error()
      << "Oculus Rift requires support for framebuffer objects.\n";
    return false;
  }

  if (glgsg->get_max_color_targets() < 2) {
    oculus_cat.error()
      << "Oculus Rift requires support for at least 2 simultaneous render targets.\n";
    return false;
  }

  if (glgsg->_glTextureBarrier == nullptr) {
    oculus_cat.error()
      << "Oculus Rift requires support for texture barriers.\n";
    return false;
  }

  glgsg->_glGenFramebuffers(1, &_fbo);
  nassertr(_fbo != 0, false);

  // Determine the proper size of the texture sets.
  LVecBase2i size_left = _hmd->get_fov_texture_size(0);
  LVecBase2i size_right = _hmd->get_fov_texture_size(1);
  LVecBase2i size(max(size_left[0], size_right[0]),
                  max(size_left[1], size_right[1]));

  ovrHmdDesc &desc = _hmd->_desc;

  // Create and attach a depth buffer.
  if (_fb_properties.get_depth_bits() > 0) {
    glgsg->bind_fbo(_fbo);
    glgsg->_glGenRenderbuffers(1, &_depth_rbo);
    glgsg->_glBindRenderbuffer(GL_RENDERBUFFER, _depth_rbo);
    glgsg->_glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, size[0], size[1]);
    glgsg->_glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, _depth_rbo);

    _fb_properties.set_depth_bits(24);
    _fb_properties.set_stencil_bits(8);
  }

  // Pretend the window has this size.
  system_changed_properties(WindowProperties::size(size[0], size[1]));

  // Set this to force created display regions to be stereo.
  _fb_properties.set_stereo(true);

#if OVR_PRODUCT_VERSION == 0 && OVR_MAJOR_VERSION < 7
  // Oculus versions before 0.7 did not support sRGB correctly.
  _fb_properties.set_srgb_color(false);
#endif

  _render_desc[0] = ovr_GetRenderDesc(_hmd->_session, ovrEye_Left, desc.DefaultEyeFov[0]);
  _render_desc[1] = ovr_GetRenderDesc(_hmd->_session, ovrEye_Right, desc.DefaultEyeFov[1]);

  cerr << "OVR HMD to eye view offsets:\n";
  cerr << _render_desc[0].HmdToEyeOffset.x << ", " << _render_desc[0].HmdToEyeOffset.y << ", " << _render_desc[0].HmdToEyeOffset.z << "\n";
  cerr << _render_desc[1].HmdToEyeOffset.x << ", " << _render_desc[1].HmdToEyeOffset.y << ", " << _render_desc[1].HmdToEyeOffset.z << "\n";

  cerr << "OVR default eye ports:\n";
  cerr << desc.DefaultEyeFov[0].UpTan << ", " << desc.DefaultEyeFov[0].DownTan << ", " << desc.DefaultEyeFov[0].LeftTan << ", " << desc.DefaultEyeFov[0].RightTan << "\n";
  cerr << desc.DefaultEyeFov[1].UpTan << ", " << desc.DefaultEyeFov[1].DownTan << ", " << desc.DefaultEyeFov[1].LeftTan << ", " << desc.DefaultEyeFov[1].RightTan << "\n";

  cerr << "OVR projection matrices:\n";
  cerr << "======================\n";
  ovrMatrix4f m = ovrMatrix4f_Projection(desc.DefaultEyeFov[0], 0.1, 10000, ovrProjection_ClipRangeOpenGL | ovrProjection_RightHanded);
  cerr << m.M[0][0] << ' ' << m.M[1][0] << ' ' << m.M[2][0] << ' ' << m.M[3][0] << '\n'
       << m.M[0][1] << ' ' << m.M[1][1] << ' ' << m.M[2][1] << ' ' << m.M[3][1] << '\n'
       << m.M[0][2] << ' ' << m.M[1][2] << ' ' << m.M[2][2] << ' ' << m.M[3][2] << '\n'
       << m.M[0][3] << ' ' << m.M[1][3] << ' ' << m.M[2][3] << ' ' << m.M[3][3] << '\n';

  cerr << "----------------------\n";
  m = ovrMatrix4f_Projection(desc.DefaultEyeFov[1], 0.1, 10000, ovrProjection_ClipRangeOpenGL | ovrProjection_RightHanded);
  cerr << m.M[0][0] << ' ' << m.M[1][0] << ' ' << m.M[2][0] << ' ' << m.M[3][0] << '\n'
       << m.M[0][1] << ' ' << m.M[1][1] << ' ' << m.M[2][1] << ' ' << m.M[3][1] << '\n'
       << m.M[0][2] << ' ' << m.M[1][2] << ' ' << m.M[2][2] << ' ' << m.M[3][2] << '\n'
       << m.M[0][3] << ' ' << m.M[1][3] << ' ' << m.M[2][3] << ' ' << m.M[3][3] << '\n';
  cerr << "======================\n";

  nassertr(!_side_by_side_stereo, false);

  return true;
}

/**
 * Called from the window thread in response to a request from within the code
 * (via request_properties()) to change the size and/or position of the
 * window.
 * @return  true if the window is successfully changed, or false if there was
 *          a problem.
 */
bool OculusGLGraphicsWindow::
do_reshape_request(int x_origin, int y_origin, bool has_origin,
                   int x_size, int y_size) {

  return !has_origin;
}
