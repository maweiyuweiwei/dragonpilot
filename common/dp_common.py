#!/usr/bin/env python3.7
import subprocess
from cereal import car
from common.params import Params
params = Params()

def is_online():
  try:
    return not subprocess.call(["ping", "-W", "4", "-c", "1", "117.28.245.92"])
  except ProcessLookupError:
    return False

def common_controller_ctrl(enabled, dragon_lat_ctrl, dragon_enable_steering_on_signal, blinker_on, steer_req):
  if enabled:
    if (dragon_enable_steering_on_signal and blinker_on) or not dragon_lat_ctrl:
      steer_req = 0 if isinstance(steer_req, int) else False
  return steer_req

def common_interface_atl(ret, atl):
  # dp
  enable_acc = ret.cruiseState.enabled
  if atl and ret.cruiseState.available:
    enable_acc = True
    if ret.gearShifter in [car.CarState.GearShifter.reverse, car.CarState.GearShifter.park]:
      enable_acc = False
    if ret.seatbeltUnlatched or ret.doorOpen:
      enable_acc = False
  return enable_acc

def common_interface_get_params_lqr(ret):
  if params.get('dp_lqr') == b'1':
    ret.lateralTuning.init('lqr')
    ret.lateralTuning.lqr.scale = 1500.0
    ret.lateralTuning.lqr.ki = 0.05

    ret.lateralTuning.lqr.a = [0., 1., -0.22619643, 1.21822268]
    ret.lateralTuning.lqr.b = [-1.92006585e-04, 3.95603032e-05]
    ret.lateralTuning.lqr.c = [1., 0.]
    ret.lateralTuning.lqr.k = [-110.73572306, 451.22718255]
    ret.lateralTuning.lqr.l = [0.3233671, 0.3185757]
    ret.lateralTuning.lqr.dcGain = 0.002237852961363602
  return ret
