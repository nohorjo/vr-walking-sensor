#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>

const char* ssid = "VRWALINGSENSORf8b7244402318";
const char* password = "4d34c0958460d";

const uint8_t MPU6050SlaveAddress = 0x68;

// MPU6050 few configuration register addresses
#define MPU6050_REGISTER_SMPLRT_DIV        0x19
#define MPU6050_REGISTER_USER_CTRL         0x6A
#define MPU6050_REGISTER_PWR_MGMT_1        0x6B
#define MPU6050_REGISTER_PWR_MGMT_2        0x6C
#define MPU6050_REGISTER_CONFIG            0x1A
#define MPU6050_REGISTER_GYRO_CONFIG       0x1B
#define MPU6050_REGISTER_ACCEL_CONFIG      0x1C
#define MPU6050_REGISTER_FIFO_EN           0x23
#define MPU6050_REGISTER_INT_ENABLE        0x38
#define MPU6050_REGISTER_ACCEL_XOUT_H      0x3B
#define MPU6050_REGISTER_SIGNAL_PATH_RESET 0x68

int16_t Ax, Ay, Az, Gx, Gy, Gz;

WebSocketsClient webSocket;

void setup() {
    Wire.begin(D7, D6);
    MPU6050_Init();
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    delay(5000);

    webSocket.begin("192.168.4.22", 80);
}

void loop() {
    Get_Data();

    webSocket.loop();
    char data[45];
    sprintf(data, "h%d,%d,%d,%d,%d,%d", Ax, Ay, Az, Gx, Gy, Gz);
    webSocket.sendTXT(data);

    delay(11);
}

void I2C_Write(uint8_t regAddress, uint8_t data){
    Wire.beginTransmission(MPU6050SlaveAddress);
    Wire.write(regAddress);
    Wire.write(data);
    Wire.endTransmission();
}

// read all 14 register
void Get_Data(){
    Wire.beginTransmission(MPU6050SlaveAddress);
    Wire.write(MPU6050_REGISTER_ACCEL_XOUT_H);
    Wire.endTransmission();
    Wire.requestFrom(MPU6050SlaveAddress, (uint8_t)14, true);

    Ax = (((int16_t)Wire.read()<<8) | Wire.read());
    Ay = (((int16_t)Wire.read()<<8) | Wire.read());
    Az = (((int16_t)Wire.read()<<8) | Wire.read());

    Wire.read(); Wire.read(); // skip temp

    Gx = (((int16_t)Wire.read()<<8) | Wire.read());
    Gy = (((int16_t)Wire.read()<<8) | Wire.read());
    Gz = (((int16_t)Wire.read()<<8) | Wire.read());
}

//configure MPU6050
void MPU6050_Init(){
    delay(150);
    I2C_Write(MPU6050_REGISTER_SMPLRT_DIV, 0x07);
    I2C_Write(MPU6050_REGISTER_PWR_MGMT_1, 0x01);
    I2C_Write(MPU6050_REGISTER_PWR_MGMT_2, 0x00);
    I2C_Write(MPU6050_REGISTER_CONFIG, 0x00);
    I2C_Write(MPU6050_REGISTER_GYRO_CONFIG, 0x00);//set +/-250 degree/second full scale
    I2C_Write(MPU6050_REGISTER_ACCEL_CONFIG, 0x00);// set +/- 2g full scale
    I2C_Write(MPU6050_REGISTER_FIFO_EN, 0x00);
    I2C_Write(MPU6050_REGISTER_INT_ENABLE, 0x01);
    I2C_Write(MPU6050_REGISTER_SIGNAL_PATH_RESET, 0x00);
    I2C_Write(MPU6050_REGISTER_USER_CTRL, 0x00);
}

