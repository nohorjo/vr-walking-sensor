#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <Wire.h>

#define SAMPLE_SIZE 25
#define ZERO_TIME 200

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

const char *ssid =  "***REMOVED***";     // Enter your WiFi Name
const char *password =  "***REMOVED***"; // Enter your WiFi Password

int16_t Ay_upper = 2000;

int16_t Ay;

int current_index = 0;
int16_t y_vals[SAMPLE_SIZE];

int16_t Ay_last = 0;

bool current_walking = false;

unsigned long last_0_y = 0;

WebSocketsClient webSocket;

void setup() {
    pinMode(D3, OUTPUT);
    digitalWrite(D3, LOW);
    Wire.begin(D7, D6);
    MPU6050_Init();
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }

    delay(5000);

    webSocket.begin("192.168.1.15", 4513, "/");
}

void loop() {
    Get_Data();

    webSocket.loop();

    if (Ay_upper) {
        y_vals[current_index] = Ay;

        if (current_index == SAMPLE_SIZE - 1) {
            int16_t Ay_avg = 0;

            for (char i = 0; i < SAMPLE_SIZE; i++) {
                Ay_avg += y_vals[i];
            }

            Ay_avg = round(Ay_avg / SAMPLE_SIZE);

            int16_t Ay_change = Ay_avg - Ay_last;

            Ay_last = Ay_avg;

            unsigned long current_time = millis();

            if (current_walking) {
                if (Ay_change < Ay_upper) {
                    if (current_time - last_0_y > ZERO_TIME) {
                        current_walking = false;
                    }
                } else {
                    last_0_y = current_time;
                }
            } else if (Ay_change > Ay_upper) {
                current_walking = true;
                last_0_y = current_time;
            }
            if (current_walking) {
                webSocket.sendTXT("f");
            }
        }

        current_index = ++current_index % SAMPLE_SIZE;
    } else {
        calibrate();
    }

    delay(16);
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

    Wire.read(); Wire.read(); // skip az
    Wire.read(); Wire.read(); // skip temp
    Wire.read(); Wire.read(); // skip gx
    Wire.read(); Wire.read(); // skip gy

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

