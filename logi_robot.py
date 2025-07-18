from mdv2 import *
from drivebase import *
from mpu6050 import MPU6050
from angle_sensor import AngleSensor
from line_sensor import *
from line_sensor_stm import *
from motor import *
from ultrasonic import *
import math

class LogiRobot:
    def __init__(self, line_sensor1=None, line_sensor2=None, motor1=None, motor2=None, 
                 md_v2=None, ultrasonic=None, robot=None, imu=None, angle_sensor=None):
        # Sử dụng các thành phần được truyền vào hoặc tạo mới
        self.line_sensor1 = line_sensor1 if line_sensor1 else LineSensorI2C()
        self.line_sensor2 = line_sensor2 if line_sensor2 else LineSensorI2C2(scl_pin2=D7_PIN, sda_pin2=D8_PIN)
        
        self.md_v2 = md_v2 if md_v2 else MotorDriverV2()
        self.robot = robot if robot else DriveBase(MODE_2WD, m1=None, m2=None, m3=None, m4=None)
        
        self.imu = imu if imu else MPU6050()
        self.angle_sensor = angle_sensor if angle_sensor else AngleSensor(self.imu)
        
        self.motor1 = motor1 if motor1 else DCMotor(self.md_v2, E1, reversed=True)
        self.motor2 = motor2 if motor2 else DCMotor(self.md_v2, E2, reversed=True)
        
        self.ultrasonic_D3_D4 = ultrasonic if ultrasonic else Ultrasonic(D3_PIN, D4_PIN)
        
        # Global variables
        self.Kp_motor = 0
        self.n4 = 0
        self.Error_M1 = 0
        self.Ki_motor = 0
        self.huong = 1
        self.Error_M2 = 0
        self.Kd_motor = 0
        self.P_M1 = 0
        self.chenh_lech_line = 0
        self.P_M2 = 0
        self.I_M1 = 0
        self.I_M2 = 0
        self.D_M1 = 0
        self.D_M2 = 0
        self.Last_Error_M1 = 0
        self.PID_M1 = 0
        self.Last_Error_M2 = 0
        self.PID_M2 = 0

    # Reset PID
    async def reset_PID(self):
        self.Kp_motor = 1.5
        self.Ki_motor = 0.07
        self.Kd_motor = 0.5
        self.P_M1 = 0
        self.P_M2 = 0
        self.I_M1 = 0
        self.I_M2 = 0
        self.D_M1 = 0
        self.D_M2 = 0
        self.PID_M1 = self.P_M1 + (self.I_M1 + self.D_M1)
        self.PID_M2 = self.P_M2 + (self.I_M2 + self.D_M2)
        self.Error_M1 = 0
        self.Error_M2 = 0
        self.Last_Error_M1 = 0
        self.Last_Error_M2 = 0

    # Stop the robot
    async def stop(self):
        self.motor1.run(0)
        self.motor2.run(0)

    # Di thang quang duong
    async def di_thang(self, quang_duong):
        await self.robot_chay_voi_toc_doc(20, 20)
        await asleep_ms(int((quang_duong / 20)*1000))
        await self.stop()

    # h : huong, 1= di toi, 0 = di lui
    # k : nga 4 so k
    # hanh dong = D : dung, T : xoay trai, P : xoay phai
    async def di_den_n4(self, h, k, hanh_dong):
        self.n4 = 0
        self.huong = h
        await self.chinh_thang_line()
        while self.n4 < k:
            await self.bam_line()
        await self.stop()
        await self.chinh_thang_line()

        if hanh_dong == 'D':
            await self.stop()
        elif hanh_dong == 'T':
            await self.xoay_trai()
        elif hanh_dong == 'P':
            await self.xoay_phai()

        await self.chinh_thang_line()

    # Mô tả hàm này...
    async def chinh_thang_line(self):
        await self.doc_line()
        while math.fabs(self.chenh_lech_line) >= 3:
            await self.doc_line()
            if self.huong == 1:
                await self.robot_chay_voi_toc_doc(0 - 15 * self.chenh_lech_line, 0 + 15 * self.chenh_lech_line)
            elif self.huong == 0:
                await self.robot_chay_voi_toc_doc(0 - 15 * self.chenh_lech_line, 0 + 15 * self.chenh_lech_line)
        await self.stop()
        await asleep_ms(100)
        while math.fabs(self.chenh_lech_line) >= 2:
            await self.doc_line()
            if self.huong == 1:
                await self.robot_chay_voi_toc_doc(0 - 15 * self.chenh_lech_line, 0 + 15 * self.chenh_lech_line)
            elif self.huong == 0:
                await self.robot_chay_voi_toc_doc(0 - 15 * self.chenh_lech_line, 0 + 15 * self.chenh_lech_line)
        await self.stop()
        await asleep_ms(100)
        while math.fabs(self.chenh_lech_line) >= 2:
            await self.doc_line()
            if self.huong == 1:
                await self.robot_chay_voi_toc_doc(0 - 15 * self.chenh_lech_line, 0 + 15 * self.chenh_lech_line)
            elif self.huong == 0:
                await self.robot_chay_voi_toc_doc(0 - 15 * self.chenh_lech_line, 0 + 15 * self.chenh_lech_line)
        await self.stop()

    # Mô tả hàm này...
    async def bam_line(self, toc_do=70, he_so_chenh_lech=30):
        await self.doc_line()
        if self.huong == 1:
            await self.robot_chay_voi_toc_doc(toc_do - he_so_chenh_lech * self.chenh_lech_line, toc_do + he_so_chenh_lech * self.chenh_lech_line)
        elif self.huong == 0:
            await self.robot_chay_voi_toc_doc(- toc_do - he_so_chenh_lech * self.chenh_lech_line, - toc_do + he_so_chenh_lech * self.chenh_lech_line)

    # Mô tả hàm này...
    async def doc_line(self):
        line_sensor1_read = self.line_sensor1.read()
        line_sensor2_read = self.line_sensor2.read()
        
        line1 = 0
        line2 = 0
        
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
            if self.huong == 1:
                self.n4 += 1
                await wait_for_async(lambda: (not (self.line_sensor1.read() == (1, 1, 1, 1))))
        
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
            if self.huong == 0:
                self.n4 += 1
                await wait_for_async(lambda: (not (self.line_sensor2.read() == (1, 1, 1, 1))))
        
        if self.huong == 1:
            # lech ben trai < 0
            # lech ben phai > 0
            self.chenh_lech_line = (line1 - line2) + 0.2 * (line1 + line2)
        elif self.huong == 0:
            # lech ben trai < 0
            # lech ben phai > 0
            self.chenh_lech_line = (line1 - line2) - 0.2 * (line1 + line2)

    # Mô tả hàm này...
    async def xoay_trai(self):
        while (self.line_sensor1.read(1)) + ((self.line_sensor1.read(1)) + ((self.line_sensor1.read(2)) + (self.line_sensor1.read(3)))) > 0 or (self.line_sensor2.read(1)) + ((self.line_sensor2.read(1)) + ((self.line_sensor2.read(2)) + (self.line_sensor2.read(3)))) > 0:
            await self.robot_chay_voi_toc_doc(-45, 45)
        while (self.line_sensor1.read(1)) + ((self.line_sensor1.read(1)) + ((self.line_sensor1.read(2)) + (self.line_sensor1.read(3)))) == 0 or (self.line_sensor2.read(1)) + ((self.line_sensor2.read(1)) + ((self.line_sensor2.read(2)) + (self.line_sensor2.read(3)))) == 0:
            await self.robot_chay_voi_toc_doc(-45, 45)
        
        await self.chinh_thang_line()

    # Mô tả hàm này...
    async def xoay_phai(self):
        while (self.line_sensor1.read(1)) + ((self.line_sensor1.read(1)) + ((self.line_sensor1.read(2)) + (self.line_sensor1.read(3)))) > 0 or (self.line_sensor2.read(1)) + ((self.line_sensor2.read(1)) + ((self.line_sensor2.read(2)) + (self.line_sensor2.read(3)))) > 0:
            await self.robot_chay_voi_toc_doc(45, -45)
        while (self.line_sensor1.read(1)) + ((self.line_sensor1.read(1)) + ((self.line_sensor1.read(2)) + (self.line_sensor1.read(3)))) == 0 or (self.line_sensor2.read(1)) + ((self.line_sensor2.read(1)) + ((self.line_sensor2.read(2)) + (self.line_sensor2.read(3)))) == 0:
            await self.robot_chay_voi_toc_doc(45, -45)
        await self.chinh_thang_line()

    # Mô tả hàm này...
    async def robot_chay_voi_toc_doc(self, rpm_trai, rpm_phai):
        await self.set_toc_do_2_motor(-1 * rpm_trai, rpm_phai)

    # Mô tả hàm này...
    async def set_toc_do_2_motor(self, toc_do_mong_muon_motor_1, toc_do_mong_muon_motor_2):
        # Trả về tốc độ quay hiện tại của động cơ trong 100ms gần nhất, đơn vị là rpm (revolutions per minute). Chỉ áp dụng với động cơ có cảm biến tốc độ encoder.
        self.Error_M1 = toc_do_mong_muon_motor_1 - (self.motor1.speed())
        self.Error_M2 = toc_do_mong_muon_motor_2 - (self.motor2.speed())
        self.P_M1 = self.Error_M1
        self.P_M2 = self.Error_M2
        self.I_M1 = self.I_M1 + self.Error_M1
        self.I_M2 = self.I_M2 + self.Error_M2
        self.D_M1 = self.Error_M1 - self.Last_Error_M1
        self.D_M2 = self.Error_M2 - self.Last_Error_M2
        self.PID_M1 = self.Kp_motor * self.P_M1 + (self.Ki_motor * self.I_M1 + self.Kd_motor * self.D_M1)
        self.PID_M2 = self.Kp_motor * self.P_M2 + (self.Ki_motor * self.I_M2 + self.Kd_motor * self.D_M2)
        
        if self.PID_M1 >= 50:
            toc_do_thuc_te_M1 = 50
        elif self.PID_M1 <= -50:
            toc_do_thuc_te_M1 = -50
        else:
            toc_do_thuc_te_M1 = self.PID_M1
        
        if self.PID_M2 >= 50:
            toc_do_thuc_te_M2 = 50
        elif self.PID_M2 <= -50:
            toc_do_thuc_te_M2 = -50
        else:
            toc_do_thuc_te_M2 = self.PID_M2
        
        self.Last_Error_M1 = self.Error_M1
        self.Last_Error_M2 = self.Error_M2
        self.motor1.run(toc_do_thuc_te_M1)
        self.motor2.run(toc_do_thuc_te_M2)

    def deinit(self):
        self.robot.stop()

    # Khởi tạo cần thiết
    async def init_sensors(self):
        self.angle_sensor.calibrate(250)
        create_task(self.angle_sensor.run())
        self.robot.angle_sensor(self.angle_sensor)
        self.robot.line_sensor(self.line_sensor1)
        self.motor1.set_encoder(rpm=350, ppr=13, gears=48)
        self.motor2.set_encoder(rpm=350, ppr=13, gears=48)
        await self.reset_PID()
        self.huong = 1

# Các hàm tiện ích độc lập (không phụ thuộc vào instance)
async def wait_for_obstacle(robot_instance, distance=10):
    """Chờ cho đến khi phát hiện vật cản"""
    await wait_for_async(lambda: robot_instance.ultrasonic_D3_D4.distance_cm() < distance)