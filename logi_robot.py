import math

# Global variables
Kp_motor = 0
Ki_motor = 0
Kd_motor = 0

n4 = 0
Error_M1 = 0
huong = 1
Error_M2 = 0
P_M1 = 0
chenh_lech_line = 0
P_M2 = 0
I_M1 = 0
I_M2 = 0
D_M1 = 0
D_M2 = 0
Last_Error_M1 = 0
PID_M1 = 0
Last_Error_M2 = 0
PID_M2 = 0

# Tham chiếu đến các đối tượng bên ngoài
line_sensor = None
line_sensor1 = None
line_sensor2 = None
motor1 = None
motor2 = None
robot = None

# Hàm thiết lập tham chiếu
def set_references(ls1=None, ls2=None, m1=None, m2=None):
    global line_sensor1, line_sensor2, motor1, motor2
    if ls1 is not None:
        line_sensor1 = ls1
    if ls2 is not None:
        line_sensor2 = ls2
    if m1 is not None:
        motor1 = m1
    if m2 is not None:
        motor2 = m2

# EXTENSION
# Reset PID
async def reset_PID():
  global Kp_motor, Error_M1, Ki_motor, Error_M2, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2
  Kp_motor = 1.5
  Ki_motor = 0.07
  Kd_motor = 0.5
  P_M1 = 0
  P_M2 = 0
  I_M1 = 0
  I_M2 = 0
  D_M1 = 0
  D_M2 = 0
  PID_M1 = P_M1 + (I_M1 + D_M1)
  PID_M2 = P_M2 + (I_M2 + D_M2)
  Error_M1 = 0
  Error_M2 = 0
  Last_Error_M1 = 0
  Last_Error_M2 = 0

# Stop the robot
async def stop():
  motor1.run(0)
  motor2.run(0)

# Di thang quang duong
async def di_thang(quang_duong):
  await robot_chay_voi_toc_doc(20, 20)
  await asleep_ms(int((quang_duong / 20)*1000))
  await stop()

# EXTENSION

# h : huong, 1= di toi, 0 = di lui
# k : nga 4 so k
# hanh dong = D : dung, T : xoay trai, P : xoay phai
async def di_den_n4(h, k, hanh_dong):
  global huong, n4
  n4 = 0
  huong = h
  await chinh_thang_line()
  while n4 < k:
    await bam_line()
  await stop()
  await chinh_thang_line()

  if hanh_dong == 'D':
    await stop()
  elif hanh_dong == 'T':
    await xoay_trai()
  elif hanh_dong == 'P':
    await xoay_phai()

  await chinh_thang_line()

# EXTENSION

# Mô tả hàm này...
async def chinh_thang_line():
  global huong, n4, chenh_lech_line
  await doc_line()
  while math.fabs(chenh_lech_line) >= 3:
    await doc_line()
    if huong == 1:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
    elif huong == 0:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
  await stop()
  await asleep_ms(100)
  while math.fabs(chenh_lech_line) >= 2:
    await doc_line()
    if huong == 1:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
    elif huong == 0:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
  await stop()
  await asleep_ms(100)
  while math.fabs(chenh_lech_line) >= 2:
    await doc_line()
    if huong == 1:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
    elif huong == 0:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
  await stop()

# EXTENSION

# Mô tả hàm này...
async def bam_line(toc_do = 70, he_so_chenh_lech = 30):
  global huong, chenh_lech_line
  await doc_line()
  if huong == 1:
    await robot_chay_voi_toc_doc(toc_do - he_so_chenh_lech * chenh_lech_line, toc_do + he_so_chenh_lech * chenh_lech_line)
  elif huong == 0:
    await robot_chay_voi_toc_doc(- toc_do - he_so_chenh_lech * chenh_lech_line, - toc_do + he_so_chenh_lech * chenh_lech_line)

# EXTENSION

# Mô tả hàm này...
async def doc_line():
  global huong, n4, chenh_lech_line
  line1 = 0
  line2 = 0
  line_sensor1_read = line_sensor1.read()
  line_sensor2_read = line_sensor2.read()
  if line_sensor1_read == (0, 1, 1, 0):
    line1 = 0
  elif line_sensor1_read == (0, 0, 1, 0):
    line1 = -1
  elif line_sensor1_read == (0, 0, 1, 1):
    line1 = -2
  elif line_sensor1_read == (0, 0, 0, 1):
    line1 = -3
  elif line_sensor1_read == (0, 1, 0, 0):
    line1 = 1
  elif line_sensor1_read == (1, 1, 0, 0):
    line1 = 2
  elif line_sensor1_read == (1, 0, 0, 0):
    line1 = 3
  elif line_sensor1_read == (1, 1, 1, 1):
    if huong == 1:
      n4 += 1
      await wait_for_async(lambda: (not (line_sensor1.read() == (1, 1, 1, 1))))
  if line_sensor2_read == (0, 1, 1, 0):
    line2 = 0
  elif line_sensor2_read == (0, 0, 1, 0):
    line2 = 1
  elif line_sensor2_read == (0, 0, 1, 1):
    line2 = 2
  elif line_sensor2_read == (0, 0, 0, 1):
    line2 = 3
  elif line_sensor2_read == (0, 1, 0, 0):
    line2 = -1
  elif line_sensor2_read == (1, 1, 0, 0):
    line2 = -2
  elif line_sensor2_read == (1, 0, 0, 0):
    line2 = -3
  elif line_sensor2_read == (1, 1, 1, 1):
    if huong == 0:
      n4 += 1
      await wait_for_async(lambda: (not (line_sensor2.read() == (1, 1, 1, 1))))
  if huong == 1:
    # lech ben trai < 0
    # lech ben phai > 0
    chenh_lech_line = (line1 - line2) + 0.2 * (line1 + line2)
  elif huong == 0:
    # lech ben trai < 0
    # lech ben phai > 0
    chenh_lech_line = (line1 - line2) - 0.2 * (line1 + line2)

# EXTENSION

# Mô tả hàm này...
async def xoay_trai():
  while (line_sensor1.read(1)) + ((line_sensor1.read(1)) + ((line_sensor1.read(2)) + (line_sensor1.read(3)))) > 0 or (line_sensor2.read(1)) + ((line_sensor2.read(1)) + ((line_sensor2.read(2)) + (line_sensor2.read(3)))) > 0:
    await robot_chay_voi_toc_doc(-45, 45)
  while (line_sensor1.read(1)) + ((line_sensor1.read(1)) + ((line_sensor1.read(2)) + (line_sensor1.read(3)))) == 0 or (line_sensor2.read(1)) + ((line_sensor2.read(1)) + ((line_sensor2.read(2)) + (line_sensor2.read(3)))) == 0:
    await robot_chay_voi_toc_doc(-45, 45)
  
  await chinh_thang_line()

# EXTENSION

# Mô tả hàm này...
async def xoay_phai():
  while (line_sensor1.read(1)) + ((line_sensor1.read(1)) + ((line_sensor1.read(2)) + (line_sensor1.read(3)))) > 0 or (line_sensor2.read(1)) + ((line_sensor2.read(1)) + ((line_sensor2.read(2)) + (line_sensor2.read(3)))) > 0:
    await robot_chay_voi_toc_doc(45, -45)
  while (line_sensor1.read(1)) + ((line_sensor1.read(1)) + ((line_sensor1.read(2)) + (line_sensor1.read(3)))) == 0 or (line_sensor2.read(1)) + ((line_sensor2.read(1)) + ((line_sensor2.read(2)) + (line_sensor2.read(3)))) == 0:
    await robot_chay_voi_toc_doc(45, -45)
  await chinh_thang_line()

# EXTENSION
# Mô tả hàm này...
async def robot_chay_voi_toc_doc(rpm_trai, rpm_phai):
  await set_toc_do_2_motor(-1 * rpm_trai, rpm_phai)

# EXTENSION
# Mô tả hàm này...
async def set_toc_do_2_motor(toc_do_mong_muon_motor_1, toc_do_mong_muon_motor_2):
  global Kp_motor, Error_M1, Ki_motor, Error_M2, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2
  # Trả về tốc độ quay hiện tại của động cơ trong 100ms gần nhất, đơn vị là rpm (revolutions per minute). Chỉ áp dụng với động cơ có cảm biến tốc độ encoder.
  Error_M1 = toc_do_mong_muon_motor_1 - (motor1.speed())
  Error_M2 = toc_do_mong_muon_motor_2 - (motor2.speed())
  P_M1 = Error_M1
  P_M2 = Error_M2
  I_M1 = I_M1 + Error_M1
  I_M2 = I_M2 + Error_M2
  D_M1 = Error_M1 - Last_Error_M1
  D_M2 = Error_M2 - Last_Error_M2
  PID_M1 = Kp_motor * P_M1 + (Ki_motor * I_M1 + Kd_motor * D_M1)
  PID_M2 = Kp_motor * P_M2 + (Ki_motor * I_M2 + Kd_motor * D_M2)
  if PID_M1 >= 50:
    toc_do_thuc_te_M1 = 50
  elif PID_M1 <= -50:
    toc_do_thuc_te_M1 = -50
  else:
    toc_do_thuc_te_M1 = PID_M1
  if PID_M2 >= 50:
    toc_do_thuc_te_M2 = 50
  elif PID_M2 <= -50:
    toc_do_thuc_te_M2 = -50
  else:
    toc_do_thuc_te_M2 = PID_M2
  Last_Error_M1 = Error_M1
  Last_Error_M2 = Error_M2
  motor1.run(toc_do_thuc_te_M1)
  motor2.run(toc_do_thuc_te_M2)

def deinit():
  if robot is not None:
    robot.stop()