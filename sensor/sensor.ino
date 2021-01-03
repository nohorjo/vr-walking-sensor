#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>

#include "constants.h"

#define MPU6050SlaveAddress 0x68

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

int current_index = 0;
int16_t y_vals[SAMPLE_SIZE];
int16_t z_vals[SAMPLE_SIZE];
WebSocketsClient webSocket;

void setup() {
    Wire.begin(D7, D6);

    MPU6050_Init();

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    delay(1000);

    webSocket.begin(ip, PORT, path);
}

void loop() {
    Get_Data();

    webSocket.loop();

    if (current_index == SAMPLE_SIZE - 1) {
        unsigned long Ay = 0;
        unsigned long Az = 0;

        for (char i = 0; i < SAMPLE_SIZE; i++) {
            int16_t y = y_vals[i];
            Ay += (y < 0 ? -y : y);

            Az += z_vals[i];
        }

        Ay = Ay / SAMPLE_SIZE;
        Az = Az / SAMPLE_SIZE;

        int16_t A = sqrt(sq(Ay) + sq(Az));

        if (A > AY_UPPER) {
            webSocket.sendTXT("f");
        }
    }

    current_index = ++current_index % SAMPLE_SIZE;
    delay(10);
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

    Wire.read(); Wire.read(); // skip ax
    y_vals[current_index] = ((int16_t)Wire.read()<<8) | Wire.read();
    z_vals[current_index] = ((int16_t)Wire.read()<<8) | Wire.read();

    Wire.read(); Wire.read(); // skip temp
    Wire.read(); Wire.read(); // skip gx
    Wire.read(); Wire.read(); // skip gy
    Wire.read(); Wire.read(); // skip gz
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

