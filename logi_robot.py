import math
from uasyncio import sleep_ms as asleep_ms


# Global variables, khởi tạo giá trị ban đầu
Kp_motor = 0
Ki_motor = 0
Kd_motor = 0
n4 = 0
Error_M1 = 0
# huong = 1
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
# Biến lưu trữ giá trị PID tùy chỉnh
custom_kp = 1.5  # Giá trị mặc định
custom_ki = 0.07  # Giá trị mặc định
custom_kd = 0.5  # Giá trị mặc định

# Biến để lưu trữ các đối tượng motor
_motor1 = None
_motor2 = None
# Biến toàn cục để lưu các đối tượng cảm biến
_line_sensor1 = None
_line_sensor2 = None

# Hàm khởi tạo motor
def init_motors(motor1, motor2):
    global _motor1, _motor2
    _motor1 = motor1
    _motor2 = motor2
    print("Motors initialized")
    
# Hàm khởi tạo cảm biến
def init_linesensors(line_sensor1, line_sensor2):
    global _line_sensor1, _line_sensor2
    _line_sensor1 = line_sensor1
    _line_sensor2 = line_sensor2
    print("Line sensors initialized")
    


# Hàm thiết lập giá trị PID tùy chỉnh
def set_custom_pid(kp, ki, kd):
    global custom_kp, custom_ki, custom_kd
    custom_kp = kp
    custom_ki = ki
    custom_kd = kd
    print(f"Custom PID values set to: Kp={kp}, Ki={ki}, Kd={kd}")
    
# Reset PID - GIỮ NGUYÊN THUẬT TOÁN GỐC
async def reset_PID():
    global Kp_motor, Error_M1, Ki_motor, Error_M2, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2
    # Sử dụng giá trị tùy chỉnh
    Kp_motor = custom_kp
    Ki_motor = custom_ki
    Kd_motor = custom_kd
    # Phần còn lại giữ nguyên như code gốc
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
    print(f"PID reset to default values: Kp={Kp_motor}, Ki={Ki_motor}, Kd={Kd_motor}")
    
    
async def stop():
    if _motor1 is None or _motor2 is None:
        print("Error: Motors not initialized. Call init_motors() first.")
        return
    _motor1.run(0)
    _motor2.run(0)
    print("Motors stopped")
    
async def wait_for_async(condition, delay_ms=50):
    while not condition():
        await asleep_ms(delay_ms)    
    
async def di_thang(quang_duong):
  await robot_chay_voi_toc_doc(20, 20)
  await asleep_ms(int((quang_duong / 20)*1000))
  await stop()
    
    
async def robot_chay_voi_toc_doc(rpm_trai, rpm_phai):
  await set_toc_do_2_motor(-1 * rpm_trai, rpm_phai)

async def set_toc_do_2_motor(toc_do_mong_muon_motor_1, toc_do_mong_muon_motor_2):
    if _motor1 is None or _motor2 is None:
        print("Error: Motors not initialized. Call init_motors() first.")
        return
    global Kp_motor, Error_M1, Ki_motor, Error_M2, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2
    # Trả về tốc độ quay hiện tại của động cơ trong 100ms gần nhất, đơn vị là rpm (revolutions per minute). Chỉ áp dụng với động cơ có cảm biến tốc độ encoder.
    Error_M1 = toc_do_mong_muon_motor_1 - (_motor1.speed())
    Error_M2 = toc_do_mong_muon_motor_2 - (_motor2.speed())
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
    _motor1.run(toc_do_thuc_te_M1)
    _motor2.run(toc_do_thuc_te_M2)
    
    
async def doc_line(huong):
    if _line_sensor1 is None or _line_sensor2 is None:
        print("Error: Line sensors not initialized. Call init_linesensors() first.")
        return
    
    global n4, chenh_lech_line
    line1 = 0  
    line2 = 0  
        
    line_sensor1_read = _line_sensor1.read()
    line_sensor2_read = _line_sensor2.read_ss2() 
    print("line_sensor1_read", line_sensor1_read)
    print("line_sensor2_read", line_sensor2_read)

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
            await wait_for_async(lambda: (not (_line_sensor1.read() == (1, 1, 1, 1))))
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
            await wait_for_async(lambda: (not (_line_sensor2.read_ss2() == (1, 1, 1, 1))))
    if huong == 1:
        # lech ben trai < 0
        # lech ben phai > 0
        chenh_lech_line = (line1 - line2) + 0.2 * (line1 + line2)
    elif huong == 0:
        # lech ben trai < 0
        # lech ben phai > 0
        chenh_lech_line = (line1 - line2) - 0.2 * (line1 + line2)


async def chinh_thang_line(huong):
  global n4, chenh_lech_line
  await doc_line(huong)  # Truyền huong 
  while math.fabs(chenh_lech_line) >= 3:
    await doc_line(huong)  # Truyền huong
    if huong == 1:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
    elif huong == 0:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
  await stop()
  await asleep_ms(100)
  while math.fabs(chenh_lech_line) >= 2:
    await doc_line(huong)  # Truyền huong
    if huong == 1:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
    elif huong == 0:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
  await stop()
  await asleep_ms(100)
  while math.fabs(chenh_lech_line) >= 2:
    await doc_line(huong)  # Truyền huong
    if huong == 1:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
    elif huong == 0:
      await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
  await stop()



