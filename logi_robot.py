import math
from uasyncio import sleep_ms as asleep_ms


Kp_motor = 0
Ki_motor = 0
Kd_motor = 0

n4 = 0
Error_M1 = 0
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

# PID motor
custom_kp = 1.5  # Giá trị mặc định 1.5
custom_ki = 0.07  # Giá trị mặc định
custom_kd = 0.5  # Giá trị mặc định 0.5

# motor
_motor1 = None
_motor2 = None
# cảm biến
_line_sensor1 = None
_line_sensor2 = None


MAX_I_LIMIT = 400  # Giới hạn I term
MAX_PID_OUTPUT = 60  # Giới hạn output PID


# PID line following
Error_Line = 0
Last_Error_Line = 0  
I_Line = 0
PID_Line = 0
P_Line = 0
D_Line = 0

# PID line following
Kp_line = 10.0  # Tương đương he_so_chenh_lech cũ
Ki_line = 0.02  # Nhỏ để tránh overshoot
Kd_line = 5.0   # Giúp giảm oscillation


MAX_I_LINE_LIMIT = 60   # Giới hạn I term
MAX_LINE_CORRECTION = 40  # Giới hạn correction output
INTERSECTION_REDUCTION_FACTOR = 0.3  # Giảm correction tại ngã tư



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
    



# Lấy giá trị nhập vào
def set_custom_pid(kp, ki, kd):
    global custom_kp, custom_ki, custom_kd
    custom_kp = kp
    custom_ki = ki
    custom_kd = kd
    print(f"Custom PID values set to: Kp={kp}, Ki={ki}, Kd={kd}")
    
# # Reset PID - GIỮ NGUYÊN THUẬT TOÁN GỐC
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
    global Kp_motor, Error_M1, Ki_motor, Error_M2, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2
    # Sử dụng giá trị tùy chỉnh
    Kp_motor = custom_kp
    Ki_motor = custom_ki
    Kd_motor = custom_kd
    P_M1 = 0
    P_M2 = 0
    I_M1 = 0
    I_M2 = 0
    D_M1 = 0
    D_M2 = 0
    Error_M1 = 0
    Error_M2 = 0
    Last_Error_M1 = 0
    Last_Error_M2 = 0
    PID_M1 = 0
    PID_M2 = 0
    # print(f"PID reset: Kp={Kp_motor}, Ki={Ki_motor}, Kd={Kd_motor}")



     
    
async def stop():
    if _motor1 is None or _motor2 is None:
        print("Error: Motors not initialized. Call init_motors() first.")
        return
    _motor1.run(0)
    _motor2.run(0)
    await reset_PID()
    await reset_line_PID()
    print("Motors stopped")
    

async def di_thang(quang_duong):
  await robot_chay_voi_toc_doc(20, 20)
  await asleep_ms(int((quang_duong / 20)*1000))
  await stop()
  
  
  
  
  
  
  
  
  
  
    
    
async def robot_chay_voi_toc_doc(rpm_trai, rpm_phai):
  # left_compensation = 1.05  # Tăng 5% cho motor trái
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
#     print("M1 PID:", PID_M1, "speed1:", _motor1.speed(), "Error1:", Error_M1, "I1:", I_M1)
#     print("M2 PID:", PID_M2, "Speed2:", _motor2.speed(), "Error2:", Error_M2, "I2:", I_M2)

    
    
async def set_toc_do_2_motor(toc_do_mong_muon_motor_1, toc_do_mong_muon_motor_2):
    if _motor1 is None or _motor2 is None:
        print("Error: Motors not initialized. Call init_motors() first.")
        return
    
    global Kp_motor, Error_M1, Ki_motor, Error_M2, Kd_motor, P_M1, P_M2, I_M1, I_M2, D_M1, D_M2, Last_Error_M1, PID_M1, Last_Error_M2, PID_M2
    
    Error_M1 = toc_do_mong_muon_motor_1 - (_motor1.speed())
    Error_M2 = toc_do_mong_muon_motor_2 - (_motor2.speed())
    
    P_M1 = Error_M1
    P_M2 = Error_M2
    
    I_M1 = I_M1 + Error_M1
    I_M2 = I_M2 + Error_M2
    
    I_M1 = max(-MAX_I_LIMIT, min(MAX_I_LIMIT, I_M1))
    I_M2 = max(-MAX_I_LIMIT, min(MAX_I_LIMIT, I_M2))
    # print("I_M1:", I_M1, "I_M2:", I_M2)  # Debug info
    
    D_M1 = Error_M1 - Last_Error_M1
    D_M2 = Error_M2 - Last_Error_M2
    
    PID_M1 = Kp_motor * P_M1 + Ki_motor * I_M1 + Kd_motor * D_M1
    PID_M2 = Kp_motor * P_M2 + Ki_motor * I_M2 + Kd_motor * D_M2
    
    if PID_M1 >= MAX_PID_OUTPUT:
        toc_do_thuc_te_M1 = MAX_PID_OUTPUT
    elif PID_M1 <= -MAX_PID_OUTPUT:
        toc_do_thuc_te_M1 = -MAX_PID_OUTPUT
    else:
        toc_do_thuc_te_M1 = PID_M1
        
    if PID_M2 >= MAX_PID_OUTPUT:
        toc_do_thuc_te_M2 = MAX_PID_OUTPUT
    elif PID_M2 <= -MAX_PID_OUTPUT:
        toc_do_thuc_te_M2 = -MAX_PID_OUTPUT
    else:
        toc_do_thuc_te_M2 = PID_M2
    
    # Lưu error cho lần sau
    Last_Error_M1 = Error_M1
    Last_Error_M2 = Error_M2
    
    # Chạy motor
    _motor1.run(toc_do_thuc_te_M1)
    _motor2.run(toc_do_thuc_te_M2)
    
    # Debug info
    # print("M1:", toc_do_thuc_te_M1, "M2:", toc_do_thuc_te_M2)
    # print("M1 PID:", PID_M1, "speed1:", _motor1.speed(), "Error1:", Error_M1, "I1:", I_M1)
    # print("M2 PID:", PID_M2, "Speed2:", _motor2.speed(), "Error2:", Error_M2, "I2:", I_M2)    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
async def doc_line(huong):
    if _line_sensor1 is None or _line_sensor2 is None:
        print("Error: Line sensors not initialized. Call init_linesensors() first.")
        return
      
    intersection_patterns = [
        (1, 1, 1, 1),  # 4 mắt - hoàn hảo
        (1, 1, 1, 0),  # thiếu mắt cuối
        (0, 1, 1, 1),  # thiếu mắt đầu  
        (1, 1, 0, 1),  # thiếu mắt thứ 3
        (1, 0, 1, 1),  # thiếu mắt thứ 2
    ]

    
    global n4, chenh_lech_line
    line1 = 0  
    line2 = 0  
        
    line_sensor1_read = _line_sensor1.read()
    line_sensor2_read = _line_sensor2.read_ss2() 
    # print("line_sensor1_read", line_sensor1_read)
    # print("line_sensor2_read", line_sensor2_read)

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
    elif line_sensor1_read in intersection_patterns:
        if huong == 1:
            n4 += 1
            # print(f"Intersection detected: {line_sensor1_read}")
            await wait_for_async(lambda: (_line_sensor1.read() not in intersection_patterns))

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
    elif line_sensor2_read in intersection_patterns:
        if huong == 0:
            n4 += 1
            # print(f"Intersection detected: {line_sensor2_read}")
            await wait_for_async(lambda: (_line_sensor2.read_ss2() not in intersection_patterns))
    if huong == 1:
        # lech ben trai < 0
        # lech ben phai > 0
        chenh_lech_line = (line1 - line2) + 0.2 * (line1 + line2)
    elif huong == 0:
        # lech ben trai < 0
        # lech ben phai > 0
        chenh_lech_line = (line1 - line2) - 0.2 * (line1 + line2)
    # print("doc_line. chenh lech line", chenh_lech_line)


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
#   while math.fabs(chenh_lech_line) >= 1:
#     await doc_line(huong)  # Truyền huong
#     if huong == 1:
#       await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
#     elif huong == 0:
#       await robot_chay_voi_toc_doc(0 - 15 * chenh_lech_line, 0 + 15 * chenh_lech_line)
#   await stop()
#   print("chinh_thang_line. huong:", huong, "chenh lech line:", chenh_lech_line)















# # line sensor 0 1 2 3 có 1 cái phát hiện thì dừng lại
# # async def xoay_trai(huong):
# #   while (_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3)))) > 0 or (_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3)))) > 0:
# #     await robot_chay_voi_toc_doc(-45, 45)
# #     await asleep_ms(10) 
# #   while (_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3)))) == 0 or (_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3)))) == 0:
# #     await robot_chay_voi_toc_doc(-45, 45)
# #     await asleep_ms(10) 
# #   await chinh_thang_line(huong)
# #   print("xoay_trai. huong:", huong)


# async def xoay_trai(huong):
#   await reset_PID()
#   await reset_line_PID()
#   while True:
#     value1 = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
#     value2 = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
#     if value1 == 0 and value2 == 0: # Đang ở ngã tư, nên đang phát hiện có line(1 trong 4 cái sẽ lên 1). Khi có line sẽ quay qua, đến khi ko còn line thì dừng lại(tức là tất cả là 0 )
#       break
#     await robot_chay_voi_toc_doc(-45, 45)
#     await asleep_ms(10)
    
#   while True:
#     if huong == 1: #tiến
#       value1 = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
#       if value1 > 0:
#         break
#     if huong == 0: #lùi
#       value2 = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
#       if value2 > 0:
#         break
    
#     await robot_chay_voi_toc_doc(-45, 45)
#     await asleep_ms(10)
    
#   await stop()  
#   await asleep_ms(50)                  
#   await chinh_thang_line(huong)      
#   print("xoay_trai. huong:", huong)


# # async def xoay_phai(huong):
# #   while (_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3)))) > 0 or (_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3)))) > 0:
# #     await robot_chay_voi_toc_doc(45, -45)
# #     await asleep_ms(10) 

# #   while (_line_sensor1.read(0)) + ((_line_sensor1.read(1)) + ((_line_sensor1.read(2)) + (_line_sensor1.read(3)))) == 0 or (_line_sensor2.read_ss2(0)) + ((_line_sensor2.read_ss2(1)) + ((_line_sensor2.read_ss2(2)) + (_line_sensor2.read_ss2(3)))) == 0:
# #     await robot_chay_voi_toc_doc(45, -45)
# #     await asleep_ms(10) 

# #   await chinh_thang_line(huong)
# #   print("xoay_phai. huong:", huong)
  
# async def xoay_phai(huong):
#   await reset_PID()
#   await reset_line_PID()
#   while True:
#     value1 = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
#     value2 = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
#     if value1 == 0 and value2 == 0: # Đang ở ngã tư, nên đang phát hiện có line(1 trong 4 cái sẽ lên 1). Khi có line sẽ quay qua, đến khi ko còn line thì dừng lại(tức là tất cả là 0 )
#       break
#     await robot_chay_voi_toc_doc(45, -45)
#     await asleep_ms(10)
    
#   while True:
#     if huong == 1: #tiến
#       value1 = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
#       if value1 > 0:
#         break
#     if huong == 0: #lùi
#       value2 = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
#       if value2 > 0:
#         break
    
#     await robot_chay_voi_toc_doc(45, -45)
#     await asleep_ms(10)
    
#   await stop()  
#   await asleep_ms(50)                  
#   await chinh_thang_line(huong)      
#   print("xoay_phai. huong:", huong)  
  








# # Hàm này cần gọi lại liên tục để có thể bám line
# async def bam_line(huong, toc_do = 80, he_so_chenh_lech = 30):
#   global chenh_lech_line
#   await doc_line(huong)
#   if huong == 1:
#     await robot_chay_voi_toc_doc(toc_do - he_so_chenh_lech * chenh_lech_line, toc_do + he_so_chenh_lech * chenh_lech_line)
#     print("bam_line. huong: ", huong)
#   elif huong == 0:
#     await robot_chay_voi_toc_doc(- toc_do - he_so_chenh_lech * chenh_lech_line, - toc_do + he_so_chenh_lech * chenh_lech_line)
#     print("bam_line. huong: ", huong)


# async def bam_line(huong, toc_do=80, he_so_chenh_lech=10):
#     global chenh_lech_line
#     await doc_line(huong)
    
#     #  THÊM: Kiểm tra có phải đang ở ngã tư không
#     if _line_sensor1 is not None and _line_sensor2 is not None:
#         # Đếm số cảm biến đang phát hiện line
#         line1_count = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
#         line2_count = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
        
#         # Nếu có quá nhiều cảm biến phát hiện line (có thể là ngã tư)
#         if line1_count >= 3 or line2_count >= 3:
#             # Giảm độ nhạy để tránh dao động
#             he_so_chenh_lech = 5  # 
#             print("Possible intersection detected - reducing sensitivity")
    
#     if huong == 1:
#         await robot_chay_voi_toc_doc(toc_do + 5 - he_so_chenh_lech * chenh_lech_line, toc_do + 5 + he_so_chenh_lech * chenh_lech_line)
#     elif huong == 0:
#         await robot_chay_voi_toc_doc(-toc_do - he_so_chenh_lech * chenh_lech_line, -toc_do + he_so_chenh_lech * chenh_lech_line)
    
#     print("bam_line. huong:", huong, "he_so:", he_so_chenh_lech)


def set_line_pid(kp, ki, kd):
    global Kp_line, Ki_line, Kd_line
    Kp_line = kp
    Ki_line = ki
    Kd_line = kd
    print(f"Line PID values set to: Kp={kp}, Ki={ki}, Kd={kd}")


async def reset_line_PID():
    global Error_Line, Last_Error_Line, I_Line, PID_Line
    Error_Line = 0
    Last_Error_Line = 0
    I_Line = 0
    PID_Line = 0
    print("Line PID reset")

# Hàm bam_line() với PID controller - FIXED VERSION
# async def bam_line(huong, toc_do=80, enable_pid=True):
#     global chenh_lech_line, Error_Line, Last_Error_Line, I_Line, PID_Line
    
#     #  Validate inputs
#     if huong not in [0, 1]:
#         print("Error: huong must be 0 or 1")
#         return
    
#     if not (10 <= toc_do <= 100):
#         print("Error: toc_do must be between 10 and 100")
#         return
    
#     #  Check sensors initialization
#     if _line_sensor1 is None or _line_sensor2 is None:
#         print("Error: Line sensors not initialized. Call init_linesensors() first.")
#         return
    
#     #  Initialize variables (fix variable scope issue)
#     left_speed = 0
#     right_speed = 0
#     correction = 0
    
#     await doc_line(huong)
    
#     # Kiểm tra có phải đang ở ngã tư không
#     intersection_detected = False
#     try:
#         line1_count = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
#         line2_count = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
        
#         if line1_count >= 3 or line2_count >= 3:
#             intersection_detected = True
#             # Reset I term khi phát hiện ngã tư để tránh windup
#             I_Line = 0
#             print("Intersection detected - I term reset")
#     except Exception as e:
#         print(f"Error reading sensors: {e}")
#         # Fallback: không detect intersection
#         intersection_detected = False
    
#     if enable_pid:
#         # PID Controller cho line following
#         Error_Line = chenh_lech_line
        
#         # P term
#         P_Line = Error_Line
        
#         # I term với anti-windup
#         I_Line = I_Line + Error_Line
#         I_Line = max(-MAX_I_LINE_LIMIT, min(MAX_I_LINE_LIMIT, I_Line))
        
#         # D term
#         D_Line = Error_Line - Last_Error_Line
        
#         # Tính PID output
#         PID_Line = Kp_line * P_Line + Ki_line * I_Line + Kd_line * D_Line
        
#         # Giới hạn correction output
#         correction = max(-MAX_LINE_CORRECTION, min(MAX_LINE_CORRECTION, PID_Line))
        
#         # Lưu error cho lần sau
#         Last_Error_Line = Error_Line
        
#         # Giảm độ nhạy khi ở ngã tư
#         if intersection_detected:
#             correction = correction * INTERSECTION_REDUCTION_FACTOR
            
#     else:
#         # Fallback về P controller cũ nếu disable PID
#         he_so_chenh_lech = 5 if intersection_detected else 10
#         correction = he_so_chenh_lech * chenh_lech_line
    
#     #  Tính toán speeds một cách nhất quán
#     base_speed = toc_do if huong == 1 else -toc_do
    
#     if huong == 1:  # Tiến
#         left_speed = base_speed - correction
#         right_speed = base_speed + correction
#     elif huong == 0:  # Lùi
#         left_speed = base_speed - correction
#         right_speed = base_speed + correction
    
#     left_speed = max(-100, min(100, left_speed))
#     right_speed = max(-100, min(100, right_speed))
    
#     await robot_chay_voi_toc_doc(left_speed, right_speed)
    
#     if enable_pid:
#         print(f"bam_line PID: E={Error_Line:.1f}, P={P_Line:.1f}, I={I_Line:.1f}, D={D_Line:.1f}, Corr={correction:.1f}")
#     else:
#         print(f"bam_line P-only: Error={chenh_lech_line:.1f}, Correction={correction:.1f}")
    
#     print(f"bam_line: huong={huong}, speeds=L{left_speed:.0f}/R{right_speed:.0f}, intersection={intersection_detected}")

# async def di_den_n4(h, k, hanh_dong):
#   global n4
#   n4 = 0
# #   huong = h
#   await chinh_thang_line(h)
#   while n4 < k:
#     await bam_line(h, 80)
    
#   await chinh_thang_line(h)
#   await asleep_ms(100)
#   await stop()
#   await asleep_ms(50) 
#   # await chinh_thang_line(h)
#   # await asleep_ms(100)

#   # hành động khi đến n4

#   if hanh_dong == 'D':
#     await reset_PID()
#     await reset_line_PID()
    
#     await chinh_thang_line(h)
#     await asleep_ms(100)
#     await chinh_thang_line(h)
#     await asleep_ms(100)
#     await stop()
#     await asleep_ms(10) 
    
#   elif hanh_dong == 'T':
#     await reset_PID()
#     await reset_line_PID()
    
#     await xoay_trai(h)
    
#   elif hanh_dong == 'P':
#     await reset_PID()
#     await reset_line_PID()
    
#     await xoay_phai(h)

#   #await chinh_thang_line(h)
#   print("di_den_n4. h: ", h, "k: ", k, "hanh_dong: ", hanh_dong)
  
  
async def bam_line(huong, toc_do=80, enable_pid=True):
    global chenh_lech_line, Error_Line, Last_Error_Line, I_Line, PID_Line, filtered_D_Line
    
    if huong not in [0, 1]:
        print("Error: huong must be 0 or 1")
        return
    
    if not (10 <= toc_do <= 100):
        print("Error: toc_do must be between 10 and 100")
        return
    
    if _line_sensor1 is None or _line_sensor2 is None:
        print("Error: Line sensors not initialized. Call init_linesensors() first.")
        return
    
    await doc_line(huong)
    
    intersection_detected = False
    try:
        line1_count = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
        line2_count = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
        
        #   Chỉ detect intersection khi chắc chắn
        if (line1_count >= 4) or (line2_count >= 4) or (line1_count >= 3 and line2_count >= 3):
            intersection_detected = True
    except Exception as e:
        intersection_detected = False
    
    if enable_pid:
        Error_Line = chenh_lech_line
        
        current_Kp = Kp_line
        current_Ki = Ki_line  
        current_Kd = Kd_line
        
        # Gentle adjustment tại intersection
        if intersection_detected:
            current_Kp *= 0.75  # Ít aggressive hơn
            current_Ki *= 0.6   
            current_Kd *= 1.1   # Ít damping hơn
        
        # Smooth error-based adaptation
        error_magnitude = abs(Error_Line)
        if error_magnitude > 1.5:  # Large error
            current_Kp *= (1.0 + 0.1 * min(error_magnitude, 3.0))  # Gradual increase
            current_Ki *= 0.9
        elif error_magnitude < 0.3:  # Very small error
            current_Kp *= 0.95
            current_Ki *= 1.05
        
        P_Line = Error_Line
        I_Line = I_Line + Error_Line
        
        # Gentle I-term management
        if intersection_detected:
            I_Line *= 0.9  # Gentle decay
        
        # Anti-windup với smooth limiting
        if I_Line > MAX_I_LINE_LIMIT:
            I_Line = MAX_I_LINE_LIMIT * 0.95
        elif I_Line < -MAX_I_LINE_LIMIT:
            I_Line = -MAX_I_LINE_LIMIT * 0.95
        
        # Filtered D term để giảm noise
        raw_D = Error_Line - Last_Error_Line
        # Low-pass filter cho D term
        alpha = 0.7  # Filter strength
        if 'filtered_D_Line' not in globals():
            filtered_D_Line = raw_D
        else:
            filtered_D_Line = alpha * raw_D + (1 - alpha) * filtered_D_Line
        
        D_Line = filtered_D_Line
        
        PID_Line = current_Kp * P_Line + current_Ki * I_Line + current_Kd * D_Line
        
        if PID_Line > MAX_LINE_CORRECTION:
            correction = MAX_LINE_CORRECTION * 0.98
        elif PID_Line < -MAX_LINE_CORRECTION:
            correction = -MAX_LINE_CORRECTION * 0.98
        else:
            correction = PID_Line
        
        Last_Error_Line = Error_Line
            
    else:
        # Fallback với smoother response
        he_so_chenh_lech = 6 if intersection_detected else 10
        correction = he_so_chenh_lech * chenh_lech_line
    
    # Smoother speed calculation
    if huong == 1:  # Tiến
        base_speed = toc_do
    elif huong == 0:  # Lùi
        base_speed = -toc_do
    
    # Apply correction với smooth transition
    left_speed = base_speed - correction
    right_speed = base_speed + correction
    
    # Progressive speed limiting thay vì hard limiting
    max_speed_diff = toc_do * 0.6  # Increase từ 0.5 to 0.6
    speed_diff = abs(left_speed - right_speed)
    
    if speed_diff > max_speed_diff:
        # Smooth speed balancing
        excess_ratio = max_speed_diff / speed_diff
        adjustment = (1.0 - excess_ratio) * 0.5
        
        if left_speed > right_speed:
            left_speed -= adjustment * speed_diff
            right_speed += adjustment * speed_diff
        else:
            right_speed -= adjustment * speed_diff
            left_speed += adjustment * speed_diff
    
    # Final gentle speed limiting
    left_speed = max(-95, min(95, left_speed))   # 95 thay vì 100
    right_speed = max(-95, min(95, right_speed))
    
    await robot_chay_voi_toc_doc(left_speed, right_speed)
    
    print(f"bam_line: huong={huong}, speeds=L{left_speed:.1f}/R{right_speed:.1f}, error={Error_Line:.2f}")


async def chinh_thang_line(huong):
    global n4, chenh_lech_line
    await doc_line(huong)
    
    #Progressive alignment với multiple stages mượt mà hơn
    alignment_stages = [
        (2.5, 12, 150),  # (threshold, gain, duration) - Gentle first stage
        (1.5, 15, 120),  # Medium precision 
        (0.8, 18, 100),  # Fine precision
        (0.3, 20, 80)    # Ultra fine
    ]
    
    for threshold, gain, max_duration in alignment_stages:
        start_time = 0
        while abs(chenh_lech_line) >= threshold and start_time < max_duration:
            await doc_line(huong)
            
            correction_factor = min(abs(chenh_lech_line) / threshold, 1.0)
            effective_gain = gain * correction_factor
            
            correction_speed = effective_gain * chenh_lech_line
            # Limit correction speed để tránh jerky movement
            correction_speed = max(-25, min(25, correction_speed))
            
            if huong == 1:
                left_rpm = -correction_speed
                right_rpm = correction_speed
            elif huong == 0:
                left_rpm = -correction_speed  
                right_rpm = correction_speed
            
            await robot_chay_voi_toc_doc(left_rpm, right_rpm)
            await asleep_ms(20)  # Shorter intervals for smoother control
            start_time += 20
        
        await robot_chay_voi_toc_doc(0, 0)
        await asleep_ms(30)  # Brief pause
    
    await stop()
    print(f"chinh_thang_line completed. huong:{huong}, final_error:{chenh_lech_line:.2f}")


async def xoay_trai(huong):
    await reset_PID()
    await reset_line_PID()
    
    initial_rotation_speed = 50  # Start slower
    final_rotation_speed = 40    # End even slower
    
    # Phase 1: Clear intersection với controlled speed
    while True:
        value1 = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
        value2 = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
        if value1 == 0 and value2 == 0:
            break
        await robot_chay_voi_toc_doc(-initial_rotation_speed, initial_rotation_speed)
        await asleep_ms(15)  # Shorter intervals
    
    await robot_chay_voi_toc_doc(0, 0)
    await asleep_ms(20)
    
    # Phase 2: Find new line với slower, more controlled movement
    while True:
        if huong == 1:  # tiến
            value1 = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
            if value1 > 0:
                break
        if huong == 0:  # lùi
            value2 = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
            if value2 > 0:
                break
        
        await robot_chay_voi_toc_doc(-final_rotation_speed, final_rotation_speed)
        await asleep_ms(15)
    
    await robot_chay_voi_toc_doc(0, 0)
    await asleep_ms(50)
    
    await chinh_thang_line(huong)
    await asleep_ms(200)
    print("xoay_trai completed. huong:", huong)

 
async def xoay_phai(huong):
    await reset_PID()
    await reset_line_PID()
    
    initial_rotation_speed = 50  
    final_rotation_speed = 40    
    
    # 1: Clear intersection
    while True:
        value1 = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
        value2 = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
        if value1 == 0 and value2 == 0:
            break
        await robot_chay_voi_toc_doc(initial_rotation_speed, -initial_rotation_speed)
        await asleep_ms(15)
    
    # Brief pause
    await robot_chay_voi_toc_doc(0, 0)
    await asleep_ms(20)
    
    # 2: Find new line
    while True:
        if huong == 1:  
            value1 = _line_sensor1.read(0) + _line_sensor1.read(1) + _line_sensor1.read(2) + _line_sensor1.read(3)
            if value1 > 0:
                break
        if huong == 0:  
            value2 = _line_sensor2.read_ss2(0) + _line_sensor2.read_ss2(1) + _line_sensor2.read_ss2(2) + _line_sensor2.read_ss2(3)
            if value2 > 0:
                break
        
        await robot_chay_voi_toc_doc(final_rotation_speed, -final_rotation_speed)
        await asleep_ms(20)
    
    await robot_chay_voi_toc_doc(0, 0) #
    await asleep_ms(50)
    
    await chinh_thang_line(huong)
    await asleep_ms(200)
    print("xoay_phai completed. huong:", huong)


# Hàm di_den_n4() sau đó xoay trái/phải hoặc dừng lại
async def di_den_n4(h, k, hanh_dong, tocdo_bamline=75):
    global n4
    n4 = 0
    
    await chinh_thang_line(h)
    await asleep_ms(50)  # 
    
    while n4 < k:
        await bam_line(h, tocdo_bamline)  
        await asleep_ms(5)     
    
    # mặc dù tốc độ là 75 65 55 nhưng khối lượng cũng nặng theo nên vẫn đúng, điều chỉnh tốc độ sẽ làm khối sau, thêm vào khối n4 luôn.
    if h == 0:
        await asleep_ms(150) # canh chỉnh khoảng tg phát hiện ngã tư, để tâm xe trùng tâm ngã tư
    elif h == 1:
        await asleep_ms(210)

      
    await robot_chay_voi_toc_doc(0, 0)  # Stop
    await asleep_ms(30)
    await chinh_thang_line(h)
    await asleep_ms(50)
    
    if hanh_dong == 'D':
        await reset_PID()
        await reset_line_PID()
        await chinh_thang_line(h)
        await asleep_ms(200) #
        await stop()
        
    elif hanh_dong == 'T':
        await xoay_trai(h)
        
    elif hanh_dong == 'P':
        await xoay_phai(h)

    # print("di_den_n4 completed. h:", h, "k:", k, "hanh_dong:", hanh_dong)



