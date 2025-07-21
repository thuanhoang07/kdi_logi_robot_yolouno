import math

class PIDController:
    # Biến lưu trữ class (static variables)
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
    
    def set_custom_pid(cls, kp, ki, kd):
        """Hàm thiết lập giá trị PID tùy chỉnh"""
        cls.custom_kp = kp
        cls.custom_ki = ki
        cls.custom_kd = kd
        print(f"Custom PID values set to: Kp={kp}, Ki={ki}, Kd={kd}")
    
    def reset_PID(cls):
        """EXTENSION, có thể tạo khối mà không phụ thuộc vào thư viện robotics
           Reset PID"""
        cls.Kp_motor = cls.custom_kp
        cls.Ki_motor = cls.custom_ki
        cls.Kd_motor = cls.custom_kd
        cls.P_M1 = 0
        cls.P_M2 = 0
        cls.I_M1 = 0
        cls.I_M2 = 0
        cls.D_M1 = 0
        cls.D_M2 = 0
        cls.PID_M1 = cls.P_M1 + (cls.I_M1 + cls.D_M1)
        cls.PID_M2 = cls.P_M2 + (cls.I_M2 + cls.D_M2)
        cls.Error_M1 = 0
        cls.Error_M2 = 0
        cls.Last_Error_M1 = 0
        cls.Last_Error_M2 = 0