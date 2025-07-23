import math
from uasyncio import sleep_ms as asleep_ms
import time

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














# Hàm 
async def wait_for_async(condition, delay_ms=50):
    while not condition():
        await asleep_ms(delay_ms)  

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
# async def reset_PID():
#     global Kp_motor, Error_M1, Ki_motor, Error_M2, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2
#     # Sử dụng giá trị tùy chỉnh
#     Kp_motor = custom_kp
#     Ki_motor = custom_ki
#     Kd_motor = custom_kd
#     # Phần còn lại giữ nguyên như code gốc
#     P_M1 = 0
#     P_M2 = 0
#     I_M1 = 0
#     I_M2 = 0
#     D_M1 = 0
#     D_M2 = 0
#     PID_M1 = P_M1 + (I_M1 + D_M1)
#     PID_M2 = P_M2 + (I_M2 + D_M2)
#     Error_M1 = 0
#     Error_M2 = 0
#     Last_Error_M1 = 0
#     Last_Error_M2 = 0
#     print(f"PID reset to default values: Kp={Kp_motor}, Ki={Ki_motor}, Kd={Kd_motor}")



async def reset_PID():
    global Kp_motor, Ki_motor, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2, Error_M1, Error_M2
    
    # Sử dụng giá trị tùy chỉnh từ set_custom_pid
    Kp_motor = custom_kp
    Ki_motor = custom_ki
    Kd_motor = custom_kd
    
    # Reset tất cả các biến tích lũy và lỗi
    P_M1 = P_M2 = 0
    I_M1 = I_M2 = 0
    D_M1 = D_M2 = 0
    PID_M1 = PID_M2 = 0
    Error_M1 = Error_M2 = 0
    Last_Error_M1 = Last_Error_M2 = 0
    
    print(f"PID đã reset với các giá trị: Kp={Kp_motor}, Ki={Ki_motor}, Kd={Kd_motor}")







     
    
async def stop():
    if _motor1 is None or _motor2 is None:
        print("Error: Motors not initialized. Call init_motors() first.")
        return
    _motor1.run(0)
    _motor2.run(0)
    print("Motors stopped")
    

async def di_thang(quang_duong):
  await robot_chay_voi_toc_doc(20, 20)
  await asleep_ms(int((quang_duong / 20)*1000))
  await stop()
  
  
  
  
  
  
  
  
  
  
    
    
async def robot_chay_voi_toc_doc(rpm_trai, rpm_phai):
  await set_toc_do_2_motor(-1 * rpm_trai, rpm_phai)

# async def set_toc_do_2_motor(toc_do_mong_muon_motor_1, toc_do_mong_muon_motor_2):
#     if _motor1 is None or _motor2 is None:
#         print("Error: Motors not initialized. Call init_motors() first.")
#         return
#     global Kp_motor, Error_M1, Ki_motor, Error_M2, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2
#     # Trả về tốc độ quay hiện tại của động cơ trong 100ms gần nhất, đơn vị là rpm (revolutions per minute). Chỉ áp dụng với động cơ có cảm biến tốc độ encoder.
#     Error_M1 = toc_do_mong_muon_motor_1 - (_motor1.speed())
#     Error_M2 = toc_do_mong_muon_motor_2 - (_motor2.speed())
#     P_M1 = Error_M1
#     P_M2 = Error_M2
#     I_M1 = I_M1 + Error_M1
#     I_M2 = I_M2 + Error_M2
#     D_M1 = Error_M1 - Last_Error_M1
#     D_M2 = Error_M2 - Last_Error_M2
#     PID_M1 = Kp_motor * P_M1 + (Ki_motor * I_M1 + Kd_motor * D_M1)
#     PID_M2 = Kp_motor * P_M2 + (Ki_motor * I_M2 + Kd_motor * D_M2)
#     if PID_M1 >= 50:
#         toc_do_thuc_te_M1 = 50
#     elif PID_M1 <= -50:
#         toc_do_thuc_te_M1 = -50
#     else:
#         toc_do_thuc_te_M1 = PID_M1
#     if PID_M2 >= 50:
#         toc_do_thuc_te_M2 = 50
#     elif PID_M2 <= -50:
#         toc_do_thuc_te_M2 = -50
#     else:
#         toc_do_thuc_te_M2 = PID_M2
#     Last_Error_M1 = Error_M1
#     Last_Error_M2 = Error_M2
#     _motor1.run(toc_do_thuc_te_M1)
#     _motor2.run(toc_do_thuc_te_M2)
#     print("M1: ", toc_do_thuc_te_M1, "M2: ", toc_do_thuc_te_M2)
    
    
    
async def set_toc_do_2_motor(toc_do_mong_muon_motor_1, toc_do_mong_muon_motor_2):
    if _motor1 is None or _motor2 is None:
        print("Error: Motors not initialized. Call init_motors() first.")
        return
        
    global Kp_motor, Ki_motor, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2, Error_M1, Error_M2
    
    # Đọc tốc độ hiện tại
    current_speed_M1 = _motor1.speed()
    current_speed_M2 = _motor2.speed()
    
    # Tính toán lỗi
    Error_M1 = toc_do_mong_muon_motor_1 - current_speed_M1
    Error_M2 = toc_do_mong_muon_motor_2 - current_speed_M2
    
    # Thành phần P
    P_M1 = Error_M1
    P_M2 = Error_M2
    
    # Thành phần I với anti-windup
    I_MAX = 100  # Giới hạn tích lũy I
    I_M1 += Error_M1
    I_M2 += Error_M2
    
    # Giới hạn I để tránh windup
    I_M1 = max(-I_MAX, min(I_MAX, I_M1))
    I_M2 = max(-I_MAX, min(I_MAX, I_M2))
    
    # Thành phần D với bộ lọc nhiễu
    alpha = 0.8  # Hệ số lọc (0-1), càng gần 1 thì càng gần với giá trị hiện tại
    D_M1 = alpha * (Error_M1 - Last_Error_M1) + (1 - alpha) * D_M1
    D_M2 = alpha * (Error_M2 - Last_Error_M2) + (1 - alpha) * D_M2
    
    # Tính PID
    PID_M1 = Kp_motor * P_M1 + Ki_motor * I_M1 + Kd_motor * D_M1
    PID_M2 = Kp_motor * P_M2 + Ki_motor * I_M2 + Kd_motor * D_M2
    
    # Giới hạn đầu ra
    MAX_SPEED = 50
    
    if PID_M1 >= MAX_SPEED:
        toc_do_thuc_te_M1 = MAX_SPEED
        # Anti-windup: Nếu đầu ra bị bão hòa, giảm tích lũy I
        if abs(Error_M1) > 0.5:  # Chỉ áp dụng khi lỗi đủ lớn
            I_M1 -= Error_M1 * 0.5  # Giảm một phần tích lũy I
    elif PID_M1 <= -MAX_SPEED:
        toc_do_thuc_te_M1 = -MAX_SPEED
        # Anti-windup
        if abs(Error_M1) > 0.5:
            I_M1 -= Error_M1 * 0.5
    else:
        toc_do_thuc_te_M1 = PID_M1
        
    if PID_M2 >= MAX_SPEED:
        toc_do_thuc_te_M2 = MAX_SPEED
        # Anti-windup
        if abs(Error_M2) > 0.5:
            I_M2 -= Error_M2 * 0.5
    elif PID_M2 <= -MAX_SPEED:
        toc_do_thuc_te_M2 = -MAX_SPEED
        # Anti-windup
        if abs(Error_M2) > 0.5:
            I_M2 -= Error_M2 * 0.5
    else:
        toc_do_thuc_te_M2 = PID_M2
    
    # Lưu lỗi trước đó
    Last_Error_M1 = Error_M1
    Last_Error_M2 = Error_M2
    
    # Áp dụng tốc độ
    _motor1.run(toc_do_thuc_te_M1)
    _motor2.run(toc_do_thuc_te_M2)
    
    # Debug info - hiển thị chi tiết hơn để dễ điều chỉnh
    if abs(Error_M1) > 5 or abs(Error_M2) > 5:  # Chỉ in khi có lỗi đáng kể
        print(f"M1: {toc_do_thuc_te_M1:.1f} (E:{Error_M1:.1f} P:{P_M1:.1f} I:{I_M1:.1f} D:{D_M1:.1f}), "
              f"M2: {toc_do_thuc_te_M2:.1f} (E:{Error_M2:.1f} P:{P_M2:.1f} I:{I_M2:.1f} D:{D_M2:.1f})")
    else:
        print(f"M1: {toc_do_thuc_te_M1:.1f}, M2: {toc_do_thuc_te_M2:.1f}")
    
    
    
    
    
    
    
    
    
    
    
    
    
# async def doc_line(huong):
#     if _line_sensor1 is None or _line_sensor2 is None:
#         print("Error: Line sensors not initialized. Call init_linesensors() first.")
#         return
    
#     global n4, chenh_lech_line
#     line1 = 0  
#     line2 = 0  
        
#     line_sensor1_read = _line_sensor1.read()
#     line_sensor2_read = _line_sensor2.read_ss2() 
#     print("line_sensor1_read", line_sensor1_read)
#     print("line_sensor2_read", line_sensor2_read)

#     if line_sensor1_read == (0, 1, 1, 0):
#         line1 = 0
#     elif line_sensor1_read == (0, 0, 1, 0):
#         line1 = -1
#     elif line_sensor1_read == (0, 0, 1, 1):
#         line1 = -2
#     elif line_sensor1_read == (0, 0, 0, 1):
#         line1 = -3
#     elif line_sensor1_read == (0, 1, 0, 0):
#         line1 = 1
#     elif line_sensor1_read == (1, 1, 0, 0):
#         line1 = 2
#     elif line_sensor1_read == (1, 0, 0, 0):
#         line1 = 3
#     elif line_sensor1_read == (1, 1, 1, 1):
#         if huong == 1:
#             n4 += 1
#             await wait_for_async(lambda: (not (_line_sensor1.read() == (1, 1, 1, 1))))
#     if line_sensor2_read == (0, 1, 1, 0):
#         line2 = 0
#     elif line_sensor2_read == (0, 0, 1, 0):
#         line2 = 1
#     elif line_sensor2_read == (0, 0, 1, 1):
#         line2 = 2
#     elif line_sensor2_read == (0, 0, 0, 1):
#         line2 = 3
#     elif line_sensor2_read == (0, 1, 0, 0):
#         line2 = -1
#     elif line_sensor2_read == (1, 1, 0, 0):
#         line2 = -2
#     elif line_sensor2_read == (1, 0, 0, 0):
#         line2 = -3
#     elif line_sensor2_read == (1, 1, 1, 1):
#         if huong == 0:
#             n4 += 1
#             await wait_for_async(lambda: (not (_line_sensor2.read_ss2() == (1, 1, 1, 1))))
#     if huong == 1:
#         # lech ben trai < 0
#         # lech ben phai > 0
#         chenh_lech_line = (line1 - line2) + 0.2 * (line1 + line2)
#     elif huong == 0:
#         # lech ben trai < 0
#         # lech ben phai > 0
#         chenh_lech_line = (line1 - line2) - 0.2 * (line1 + line2)
#     print("doc_line. chenh lech line", chenh_lech_line)


async def doc_line(huong):
    if _line_sensor1 is None or _line_sensor2 is None:
        print("Error: Line sensors not initialized. Call init_linesensors() first.")
        return
    
    global n4, chenh_lech_line
    line1 = 0  
    line2 = 0  
        
    # Đọc giá trị cảm biến
    try:
        line_sensor1_read = _line_sensor1.read()
        line_sensor2_read = _line_sensor2.read_ss2() 
        print("line_sensor1_read", line_sensor1_read)
        print("line_sensor2_read", line_sensor2_read)
    except Exception as e:
        print(f"Lỗi khi đọc cảm biến: {e}")
        return

    # Xử lý đọc cảm biến 1
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
            print(f"Phát hiện ngã tư thứ {n4} (sensor 1)")
            await wait_for_async(lambda: (not (_line_sensor1.read() == (1, 1, 1, 1))))
    
    # Xử lý đọc cảm biến 2
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
            print(f"Phát hiện ngã tư thứ {n4} (sensor 2)")
            await wait_for_async(lambda: (not (_line_sensor2.read_ss2() == (1, 1, 1, 1))))
    
    # Tính toán chênh lệch line dựa vào hướng
    if huong == 1:
        # lech ben trai < 0
        # lech ben phai > 0
        chenh_lech_line = (line1 - line2) + 0.2 * (line1 + line2)
    elif huong == 0:
        # lech ben trai < 0
        # lech ben phai > 0
        chenh_lech_line = (line1 - line2) - 0.2 * (line1 + line2)
    
    print(f"doc_line: huong={huong}, chenh_lech_line={chenh_lech_line:.2f}, line1={line1}, line2={line2}")



# async def chinh_thang_line(huong):
#   global n4, chenh_lech_line
#   await doc_line(huong)  # Truyền huong 
#   while math.fabs(chenh_lech_line) >= 3:
#     await doc_line(huong)  # Truyền huong
#     if huong == 1:
#       await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
#     elif huong == 0:
#       await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
#   await stop()
#   await asleep_ms(100)
#   while math.fabs(chenh_lech_line) >= 2:
#     await doc_line(huong)  # Truyền huong
#     if huong == 1:
#       await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
#     elif huong == 0:
#       await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
#   await stop()
#   await asleep_ms(100)
#   while math.fabs(chenh_lech_line) >= 2:
#     await doc_line(huong)  # Truyền huong
#     if huong == 1:
#       await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
#     elif huong == 0:
#       await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
#   await stop()
#   print("chinh_thang_line. huong:", huong, "chenh lech line:", chenh_lech_line)



async def chinh_thang_line(huong):
    global n4, chenh_lech_line
    await doc_line(huong)
    
    # Thêm timeout để tránh mắc kẹt trong vòng lặp
    max_attempts = 20
    attempt_count = 0
    
    # Lặp 1: Chỉnh thẳng khi lệch nhiều
    while math.fabs(chenh_lech_line) >= 3 and attempt_count < max_attempts:
        await doc_line(huong)
        await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
        attempt_count += 1
    
    await stop()
    await asleep_ms(100)
    
    # Reset biến đếm cho vòng lặp tiếp theo
    attempt_count = 0
    
    # Lặp 2: Tiếp tục chỉnh thẳng với mức lệch trung bình
    while math.fabs(chenh_lech_line) >= 2 and attempt_count < max_attempts:
        await doc_line(huong)
        await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
        attempt_count += 1
    
    await stop()
    await asleep_ms(100)
    
    # Reset biến đếm cho vòng lặp tiếp theo
    attempt_count = 0
    
    # Lặp 3: Chỉnh thẳng lần cuối
    while math.fabs(chenh_lech_line) >= 2 and attempt_count < max_attempts:
        await doc_line(huong)
        await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
        attempt_count += 1
    
    await stop()
    
    # Kiểm tra xem đã chỉnh thẳng thành công chưa
    if math.fabs(chenh_lech_line) >= 2:
        print(f"Cảnh báo: Không thể chỉnh thẳng hoàn toàn, chenh_lech_line = {chenh_lech_line:.2f}")
    else:
        print(f"Đã chỉnh thẳng thành công, chenh_lech_line = {chenh_lech_line:.2f}")












# # line sensor 0 1 2 3 có 1 cái phát hiện thì dừng lại
# async def xoay_trai(huong):
#   while (_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3)))) > 0 or (_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3)))) > 0:
#     await robot_chay_voi_toc_doc(-45, 45)
#   while (_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3)))) == 0 or (_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3)))) == 0:
#     await robot_chay_voi_toc_doc(-45, 45)
#   await chinh_thang_line(huong)
#   print("xoay_trai. huong:", huong)


# async def xoay_phai(huong):
#   while (_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3)))) > 0 or (_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3)))) > 0:
#     await robot_chay_voi_toc_doc(45, -45)
#   while (_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3)))) == 0 or (_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3)))) == 0:
#     await robot_chay_voi_toc_doc(45, -45)
#   await chinh_thang_line(huong)
#   print("xoay_phai. huong:", huong)
  
  
async def xoay_trai(huong):
    # Reset PID trước khi xoay
    await reset_PID()
    
    # Thêm timeout để tránh mắc kẹt
    max_time_ms = 5000  # Tối đa 5 giây cho xoay
    start_time = time.ticks_ms()
    
    # Vòng lặp 1: Xoay cho đến khi không còn phát hiện line
    while (((_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3))))) > 0 or 
          ((_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3))))) > 0):
        await robot_chay_voi_toc_doc(-45, 45)
        
        # Kiểm tra timeout
        if time.ticks_diff(time.ticks_ms(), start_time) > max_time_ms:
            print("Cảnh báo: Timeout khi xoay trái (vòng lặp 1)")
            break
    
    # Vòng lặp 2: Tiếp tục xoay cho đến khi phát hiện line
    while (((_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3))))) == 0 or 
          ((_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3))))) == 0):
        await robot_chay_voi_toc_doc(-45, 45)
        
        # Kiểm tra timeout
        if time.ticks_diff(time.ticks_ms(), start_time) > max_time_ms:
            print("Cảnh báo: Timeout khi xoay trái (vòng lặp 2)")
            break
    
    # Dừng động cơ trước khi chỉnh thẳng
    await stop()
    await asleep_ms(100)
    
    # Chỉnh thẳng sau khi xoay
    await chinh_thang_line(huong)
    print(f"xoay_trai hoàn thành: huong={huong}")
    
    
    
    
async def xoay_phai(huong):
    # Reset PID trước khi xoay
    await reset_PID()
    
    # Thêm timeout để tránh mắc kẹt
    max_time_ms = 5000  # Tối đa 5 giây cho xoay
    start_time = time.ticks_ms()
    
    # Vòng lặp 1: Xoay cho đến khi không còn phát hiện line
    while (((_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3))))) > 0 or 
          ((_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3))))) > 0):
        await robot_chay_voi_toc_doc(45, -45)
        
        # Kiểm tra timeout
        if time.ticks_diff(time.ticks_ms(), start_time) > max_time_ms:
            print("Cảnh báo: Timeout khi xoay phải (vòng lặp 1)")
            break
    
    # Vòng lặp 2: Tiếp tục xoay cho đến khi phát hiện line
    while (((_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3))))) == 0 or 
          ((_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3))))) == 0):
        await robot_chay_voi_toc_doc(45, -45)
        
        # Kiểm tra timeout
        if time.ticks_diff(time.ticks_ms(), start_time) > max_time_ms:
            print("Cảnh báo: Timeout khi xoay phải (vòng lặp 2)")
            break
    
    # Dừng động cơ trước khi chỉnh thẳng
    await stop()
    await asleep_ms(100)
    
    # Chỉnh thẳng sau khi xoay
    await chinh_thang_line(huong)
    print(f"xoay_phai hoàn thành: huong={huong}")  
  
  








# Hàm này cần gọi lại liên tục để có thể bám line
# async def bam_line(huong, toc_do = 70, he_so_chenh_lech = 30):
#   global chenh_lech_line
#   await doc_line(huong)
#   if huong == 1:
#     await robot_chay_voi_toc_doc(toc_do - he_so_chenh_lech * chenh_lech_line, toc_do + he_so_chenh_lech * chenh_lech_line)
#     print("bam_line. huong: ", huong)
#   elif huong == 0:
#     await robot_chay_voi_toc_doc(- toc_do - he_so_chenh_lech * chenh_lech_line, - toc_do + he_so_chenh_lech * chenh_lech_line)
#     print("bam_line. huong: ", huong)


async def bam_line(huong, toc_do = 70, he_so_chenh_lech = 30):
    global chenh_lech_line
    
    # Đọc giá trị cảm biến và tính toán chênh lệch
    await doc_line(huong)
    
    # Nếu lệch quá lớn, reset PID để tránh tích lũy lỗi
    if abs(chenh_lech_line) > 4:
        await reset_PID()
    
    # Điều chỉnh tốc độ dựa vào hướng và chênh lệch
    if huong == 1:
        await robot_chay_voi_toc_doc(toc_do - he_so_chenh_lech * chenh_lech_line, 
                                    toc_do + he_so_chenh_lech * chenh_lech_line)
        print(f"bam_line: huong={huong}, toc_do={toc_do}, he_so={he_so_chenh_lech}, chenh_lech={chenh_lech_line:.2f}")
    elif huong == 0:
        await robot_chay_voi_toc_doc(- toc_do - he_so_chenh_lech * chenh_lech_line, 
                                    - toc_do + he_so_chenh_lech * chenh_lech_line)
        print(f"bam_line: huong={huong}, toc_do={toc_do}, he_so={he_so_chenh_lech}, chenh_lech={chenh_lech_line:.2f}")


# async def di_den_n4(h, k, hanh_dong):
#   global n4
#   n4 = 0
# #   huong = h
#   await chinh_thang_line(h)
#   while n4 < k:
#     await bam_line(h)
#   await stop()
#   await chinh_thang_line(h)

#   if hanh_dong == 'D':
#     await stop()
#   elif hanh_dong == 'T':
#     await xoay_trai(h)
#   elif hanh_dong == 'P':
#     await xoay_phai(h)

#   await chinh_thang_line(h)
#   print("di_den_n4. h: ", h, "k: ", k, "hanh_dong: ", hanh_dong)
  
  
  
  
async def di_den_n4(h, k, hanh_dong):
    global n4
    n4 = 0
    
    # Reset PID và thiết lập cho giai đoạn bám line
    await reset_PID()
    await set_custom_pid(1.5, 0.05, 0.5)
    
    # Chỉnh thẳng trước khi di chuyển
    await chinh_thang_line(h)
    
    # Di chuyển đến ngã tư thứ k với cơ chế thoát an toàn
    bam_count = 0
    max_bam = 150  # Giới hạn để tránh vòng lặp vô hạn
    
    while n4 < k and bam_count < max_bam:
        # Nếu gần đến ngã tư mục tiêu, giảm tốc độ
        if n4 == k-1:
            await bam_line(h, 50, 30)  # Tốc độ chậm hơn khi gần đến
        else:
            await bam_line(h)
        
        bam_count += 1
        
        # Reset PID định kỳ nếu di chuyển quá lâu
        if bam_count % 30 == 0:
            await reset_PID()
            await set_custom_pid(1.5, 0.05, 0.5)
    
    # Kiểm tra xem đã đến ngã tư mục tiêu chưa
    if n4 < k:
        print(f"Cảnh báo: Không tìm thấy đủ {k} ngã tư sau {bam_count} lần bám line")
    
    await stop()
    
    # Reset PID và thiết lập cho giai đoạn xoay
    await reset_PID()
    
    # Thiết lập PID khác cho việc xoay
    if hanh_dong in ['T', 'P']:
        await set_custom_pid(2.0, 0.02, 0.8)
    
    # Chỉnh thẳng line
    await chinh_thang_line(h)
    
    # Thực hiện hành động
    if hanh_dong == 'D':
        await stop()
    elif hanh_dong == 'T':
        await xoay_trai(h)
    elif hanh_dong == 'P':
        await xoay_phai(h)
    
    # Reset PID và thiết lập cho di chuyển tiếp theo
    await reset_PID()
    await set_custom_pid(1.5, 0.07, 0.5)
    
    # Chỉnh thẳng lại sau khi thực hiện hành động
    await chinh_thang_line(h)
    
    print(f"di_den_n4 hoàn thành. h: {h}, k: {k}, hanh_dong: {hanh_dong}, bam_count: {bam_count}")  