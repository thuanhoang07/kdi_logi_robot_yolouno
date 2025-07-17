# kdi_unoarm.py
# Python library for UnoArm control
# from remote_control import *
from servo import servo
import math
import time


# Default dimensions
_d1 = 10.25
_d2 = 15
_d3 = 16
_d4 = 4.64
_d5 = 7.5


# khai bao vi tri ban dau
r_now = 28  # tam xa
h_now = 9  # tam cao

S2_now = 90  # goc
S3_now = 90  # goc

phi_now = 90  # goc
topic_hut = None
step = 0.1
# khai bao cac hang so khac
pause = 0.01
pause2 = 0.01
cong_suat_hut = 100


def set_dimensions(d1, d2, d3, d4, d5):
    global _d1, _d2, _d3, _d4, _d5
    _d1 = d1
    _d2 = d2
    _d3 = d3
    _d4 = d4
    _d5 = d5


def kiem_tra_tinh_hop_le(check_S2, check_S3):
    hop_le = True
    if check_S3 > 170:
        hop_le = False
    elif check_S2 > 180:
        hop_le = False
    elif (15 / 16) * check_S2 + check_S3 < 129.375:
        hop_le = False
    elif check_S3 < check_S2 / 2:
        hop_le = False
    elif check_S3 > (check_S2 * 5) / 8 + 113.75:
        hop_le = False
    print("Kiem tra hop le:", hop_le)
    return hop_le


def go_to_S2_S3(to_S2, to_S3):
    global S2_now, S3_now
    print(("".join([str(x2) for x2 in ["di den goc: ", to_S2, " , ", to_S3]])))
    if kiem_tra_tinh_hop_le(to_S2, to_S3):
        S2_now = to_S2
        S3_now = to_S3
        init_S2 = servo.position(1)
        init_S3 = servo.position(2)
        current_S2 = servo.position(1)
        current_S3 = servo.position(2)
        q = math.sqrt(
            (init_S2 - to_S2) * (init_S2 - to_S2)
            + (init_S3 - to_S3) * (init_S3 - to_S3)
        )
        if q != 0:
            buoc_S2 = 2 * ((to_S2 - init_S2) / q)
            buoc_S3 = 2 * ((to_S3 - init_S3) / q)
            if init_S2 < to_S2:
                while current_S2 <= to_S2:
                    current_S2 = (
                        current_S2 if isinstance(current_S2, (int, float)) else 0
                    ) + buoc_S2
                    current_S3 = (
                        current_S3 if isinstance(current_S3, (int, float)) else 0
                    ) + buoc_S3
                    servo.position(1, (round(current_S2)))
                    time.sleep(pause)
                    servo.position(2, (round(current_S3)))
                    time.sleep(pause)
            else:
                while current_S2 >= to_S2:
                    current_S2 = (
                        current_S2 if isinstance(current_S2, (int, float)) else 0
                    ) + buoc_S2
                    current_S3 = (
                        current_S3 if isinstance(current_S3, (int, float)) else 0
                    ) + buoc_S3
                    servo.position(1, (round(current_S2)))
                    time.sleep(pause)
                    servo.position(2, (round(current_S3)))
                    time.sleep(pause)
            print(
                (
                    "".join(
                        [
                            str(x3)
                            for x3 in [
                                "S2 va S3 moi duoc cap nhat: ",
                                servo.position(1),
                                " , ",
                                servo.position(2),
                            ]
                        ]
                    )
                )
            )
    else:
        print("khong hop le")


def go_to_r_h(r, h):
  global r_now, h_now
  print("-----------------")
  print("di den vi tri: r = ",r," ,h = ",h)
  y1 = r - _d4
  z1 = h + _d5
  d6 = math.sqrt(y1 * y1 + (z1 - _d1) * (z1 - _d1))
  phi2 = math.acos((_d2 * _d2 + (_d3 * _d3 - d6 * d6)) / (2 * (_d2 * _d3))) / math.pi * 180
  phi3 = math.acos((_d2 * _d2 + (d6 * d6 - _d3 * _d3)) / (2 * (_d2 * d6))) / math.pi * 180
  if z1 > _d1:
    phi4 = 180 - math.asin(y1 / d6) / math.pi * 180
  else:
    phi4 = math.asin(y1 / d6) / math.pi * 180
  phi1 = phi3 + phi4
  to_S2 = 2 * phi1 - 190
  to_S3 = (phi2 + to_S2 / 2) - 25
  #print((''.join([str(x4) for x4 in ['S2 = ', to_S2, ', S3 = ', to_S3, ', phi2 = ', phi2, ', phi1 = ', phi1, ', phi3 = ', phi3, ', phi4 = ', phi4, ', d6 = ', d6, ', y = ', y, ', z = ', z, ', y1 = ', y1, ', z1 = ', z1, ', i = ', i]])))
  
  go_to_S2_S3(to_S2, to_S3)
  
  if kiem_tra_tinh_hop_le(to_S2, to_S3):
    r_now = r
    h_now = h
  
  print("r_now = ", r_now, ", h_now = ", h_now)
