/**
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * @file oculusHmd.I
 * @author rdb
 * @date 2014-03-26
 */

/**
 * Returns the major version of the sensor firmware.
 */
INLINE short OculusHmd::
get_firmware_major() const {
  return _desc.FirmwareMajor;
}

/**
 * Returns the minor version of the sensor firmware.
 */
INLINE short OculusHmd::
get_firmware_minor() const {
  return _desc.FirmwareMinor;
}

/**
 * Returns the recommended optical field of view for the given eye.
 */
INLINE ovrFovPort OculusHmd::
get_default_eye_fov(int i) const {
  return _desc.DefaultEyeFov[i];
}

/**
 * Returns the maximum optical field of view that can practically be rendered
 * for the given eye.
 */
INLINE ovrFovPort OculusHmd::
get_max_eye_fov(int i) const {
  return _desc.MaxEyeFov[i];
}

/**
 * Returns the resolution of the full HMD screen (both eyes) in pixels.
 */
INLINE LVecBase2i OculusHmd::
get_resolution() const {
  const ovrSizei &size = _desc.Resolution;
  return LVecBase2i(size.w, size.h);
}

/**
 * Returns the location of the monitor window on the screen.  Set to (0, 0) if
 * not supported.
 */
INLINE LVecBase2i OculusHmd::
get_windows_pos() const {
#if OVR_PRODUCT_VERSION == 0 && OVR_MAJOR_VERSION < 6
  const ovrVector2i &pos = _desc.WindowsPos;
  return LVecBase2i(pos.x, pos.y);
#else
  return LVecBase2i::zero();
#endif
}
