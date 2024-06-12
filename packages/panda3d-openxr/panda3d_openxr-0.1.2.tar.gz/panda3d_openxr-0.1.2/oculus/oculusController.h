/**
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * @file oculusController.h
 * @author rdb
 * @date 2016-12-29
 */

#ifndef OCULUSCONTROLLER_H
#define OCULUSCONTROLLER_H

#include "inputDevice.h"

#include "OVR_CAPI.h"

class OculusHmd;

/**
 * Represents the Oculus Touch or Oculus Remote.
 */
class EXPCL_OCULUS OculusController : public InputDevice {
public:
  OculusController(OculusHmd *hmd, const string &name, DeviceClass dev_class);

  void got_pose_state(const ovrPoseStatef &state, unsigned int status);

  virtual void do_poll();

private:
  OculusHmd *const _hmd;

  ovrHandType _hand;
  ovrControllerType _type;
};

#endif
