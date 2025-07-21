import math

# Global variables, khởi tạo giá trị ban đầu
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

# Biến lưu trữ giá trị PID tùy chỉnh
custom_kp = 1.5  # Giá trị mặc định
custom_ki = 0.07  # Giá trị mặc định
custom_kd = 0.5  # Giá trị mặc định

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