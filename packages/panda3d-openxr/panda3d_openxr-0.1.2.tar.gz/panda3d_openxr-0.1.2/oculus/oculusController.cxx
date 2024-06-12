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

#include "oculusController.h"
#include "oculusHmd.h"
#include "gamepadButton.h"

/**
 *
 */
OculusController::
OculusController(OculusHmd *hmd, const string &name, DeviceClass dev_class)
 : InputDevice(name, dev_class, 0),
   _hmd(hmd) {

  // Set the mappings and initial state of the hand controllers.
  if (dev_class == DC_right_hand) {
    _hand = ovrHand_Right;
    _type = ovrControllerType_RTouch;
    _flags |= IDF_has_tracker | IDF_has_vibration;

    _buttons.resize(3);
    _buttons[0].handle = GamepadButton::action_a();
    _buttons[1].handle = GamepadButton::action_b();
    _buttons[2].handle = GamepadButton::rstick();

    _controls.resize(4);
    _controls[0].axis = C_right_x;
    _controls[0].known = true;
    _controls[1].axis = C_right_y;
    _controls[1].known = true;
    _controls[2].axis = C_right_trigger;
    _controls[2].known = true;
    _controls[3].axis = C_right_grip;
    _controls[3].known = true;

  } else if (dev_class == DC_left_hand) {
    _hand = ovrHand_Left;
    _type = ovrControllerType_LTouch;
    _flags |= IDF_has_tracker | IDF_has_vibration;

    _buttons.resize(4);
    _buttons[0].handle = GamepadButton::action_x();
    _buttons[1].handle = GamepadButton::action_y();
    _buttons[2].handle = GamepadButton::lstick();
    _buttons[3].handle = GamepadButton::start();

    _controls.resize(4);
    _controls[0].axis = C_left_x;
    _controls[0].known = true;
    _controls[1].axis = C_left_y;
    _controls[1].known = true;
    _controls[2].axis = C_left_trigger;
    _controls[2].known = true;
    _controls[3].axis = C_left_grip;
    _controls[3].known = true;
  }
}

/**
 * Called by OculusHmd when there is a new pose state available.
 */
void OculusController::
got_pose_state(const ovrPoseStatef &state, unsigned int status) {
  LightMutexHolder holder(_lock);
  ovrPosef pose = state.ThePose;

  // Don't forget to convert to Panda's coordinate system.
  LPoint3 pos(pose.Position.x, -pose.Position.z, pose.Position.y);
  LOrientation orient(pose.Orientation.w, pose.Orientation.x,
                     -pose.Orientation.z, pose.Orientation.y);
  set_tracker(pos, orient, state.TimeInSeconds);
}

/**
 * Polls the input device for new activity, to ensure it contains the latest
 * events.  This will only have any effect for some types of input devices;
 * others may be updated automatically, and this method will be a no-op.
 */
void OculusController::
do_poll() {
  ovrSession session = _hmd->_session;
  nassertv(session != NULL);

  ovrInputState state;
  if (ovr_GetInputState(session, _type, &state) == ovrSuccess_DeviceUnavailable) {
    _is_connected = false;
  }

  if (_hand == ovrHand_Right) {
    set_control_state(C_right_x, state.Thumbstick[ovrHand_Right].x);
    set_control_state(C_right_y, state.Thumbstick[ovrHand_Right].y);
    set_control_state(C_right_trigger, state.IndexTrigger[ovrHand_Right]);
    set_control_state(C_right_grip, state.HandTrigger[ovrHand_Right]);

    set_button_state(0, (state.Buttons & ovrButton_A) != 0);
    set_button_state(1, (state.Buttons & ovrButton_B) != 0);
    set_button_state(2, (state.Buttons & ovrButton_RThumb) != 0);
  } else {
    set_control_state(C_left_x, state.Thumbstick[ovrHand_Left].x);
    set_control_state(C_left_y, state.Thumbstick[ovrHand_Left].y);
    set_control_state(C_left_trigger, state.IndexTrigger[ovrHand_Left]);
    set_control_state(C_left_grip, state.HandTrigger[ovrHand_Left]);

    set_button_state(0, (state.Buttons & ovrButton_X) != 0);
    set_button_state(1, (state.Buttons & ovrButton_Y) != 0);
    set_button_state(2, (state.Buttons & ovrButton_LThumb) != 0);
    set_button_state(3, (state.Buttons & ovrButton_Enter) != 0);
  }
}
