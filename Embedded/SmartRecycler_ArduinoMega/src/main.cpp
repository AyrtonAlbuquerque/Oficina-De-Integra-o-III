#include <Arduino.h>
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

/* -------------------------------------------------------------------------- */
/*                                   Defines                                  */
/* -------------------------------------------------------------------------- */
#define ECHO1           2
#define ECHO2           3
#define ECHO3           4
#define ECHO4           5
#define LED1_PIN        23
#define LED2_PIN        25
#define LED3_PIN        27
#define LED4_PIN        29
#define TRIGGER1        22
#define TRIGGER2        24
#define TRIGGER3        26
#define TRIGEGR4        28
#define IR1_PIN         30
#define IR2_PIN         31
#define WIDTH           128
#define HEIGHT          64
#define BOUD_RATE       115200
#define PROCESS_TIMEOUT 15000
#define CONTAINER_COUNT 4
#define CONTAINER_FULL  10
#define RECYCLER_ID     0

/* -------------------------------------------------------------------------- */
/*                                    Types                                   */
/* -------------------------------------------------------------------------- */
typedef struct waste_t {
    int type;
    String code;
    String message;
} waste;

/* -------------------------------------------------------------------------- */
/*                                   Globals                                  */
/* -------------------------------------------------------------------------- */
Servo servoT;
Servo servoL;
Servo servoR;
bool processing;

/* -------------------------------------------------------------------------- */
/*                                Declarations                                */
/* -------------------------------------------------------------------------- */
Adafruit_SSD1306 display(WIDTH, HEIGHT, &Wire, -1);

waste parseResponse(String response);

void recycle(waste item);

String generateQRCode(waste item);

void updateLED(int container);

void moveServos(Servo servo1, int base1, int value1, Servo servo2, int base2, int value2);

/* -------------------------------------------------------------------------- */
/*                                    Setup                                   */
/* -------------------------------------------------------------------------- */
void setup() {
    // Setup system variables
    processing = false;

    // Setup pin modes
    pinMode(IR1_PIN, INPUT);
    pinMode(IR2_PIN, INPUT);
    pinMode(ECHO1, INPUT);
    pinMode(ECHO2, INPUT);
    pinMode(ECHO3, INPUT);

    // Setup the serial ports
    Serial3.begin(BOUD_RATE);
}

/* -------------------------------------------------------------------------- */
/*                                    Loop                                    */
/* -------------------------------------------------------------------------- */
void loop() {
    long start;
    waste item;

    // If not processing waste
    if (!processing) {
        // If the IR Sensor is active than start processing
        if (digitalRead(IR1_PIN) == HIGH && digitalRead(IR2_PIN) == HIGH) {
            processing = true;
            start = millis();

            // Waste processing begins. wait for a moment
            delay(3000);
            // Notify ESP32 to take a picture and get classification
            Serial3.println(".");
        }
    } else {
        // While processing timeout has not been reached
        if ((start + PROCESS_TIMEOUT) <= millis()) {
            // If there is a response from ESP32
            if (Serial3.available()) {
                // Get and parse the response string
                item = parseResponse(Serial3.readString());

                // If item message is not empty than its just a message from ESP32
                if (item.message != "") {
                    // Display the message in the display
                    display.println(item.message);
                    display.display();
                    processing = false;
                } else {
                    recycle(item);
                }
            }
        } else {
            // Timeout reached, end processing
            display.println("Smart Recycler");
            display.display();
            processing = false;
        }
    }
    delay(10);
}

/* -------------------------------------------------------------------------- */
/*                                  Functions                                 */
/* -------------------------------------------------------------------------- */
waste parseResponse(String response) {
    waste item;

    // Initial setup
    item.type = -1;
    item.code = "";
    item.message = "";

    if (response != "") {
        // Classification logic based on response
    }

    return item;
}

void recycle(waste item) {
    // Waste treatment based on type
    if (item.type == 0)                                             // Soda cans
        moveServos(servoT, 0, 90, servoR, 0, 90);
    else if (item.type == 1 || item.type == 2)                      // Juice boxes | Crumpled paper
        moveServos(servoT, 0, 90, servoR, 180, 90);
    else if (item.type == 3 || item.type == 4 || item.type == 5)   // Plastic bottles | Plastic cups | Chip bags
        moveServos(servoT, 180, 90, servoL, 0, 90);
    else                                                            // Others
        moveServos(servoT, 180, 90, servoL, 180, 90);

    // Generate and Show QRCode
    display.println(generateQRCode(item));
    display.display();

    // Check containers levels
    for (size_t i = 0; i < CONTAINER_COUNT; i++) {
        updateLED(i);
    }
}

String generateQRCode(waste item) {
    // QRCode logic


    return "";
}

void updateLED(int container) {
    int trigger = (container == 0) ? TRIGGER1 : ((container == 1) ? TRIGGER2 : ((container == 2) ? TRIGGER3 : TRIGEGR4));
    int echo = (container == 0) ? ECHO1 : ((container == 1) ? ECHO2 : ((container == 2) ? ECHO3 : ECHO4));
    int led = (container == 0) ? LED1_PIN : ((container == 1) ? LED2_PIN : ((container == 2) ? LED3_PIN : LED4_PIN));
    long duration;
    int distance;

    // Clears the trigger pin condition and sets the trigger pin to HIGH (active) for 10 microseconds
    digitalWrite(trigger, LOW);
    delayMicroseconds(2);
    digitalWrite(trigger, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigger, LOW);

    // Reads the echo pin and returns the sound wave travel time in microseconds
    duration = pulseIn(echo, HIGH);

    // Calculating the distance. Speed of sound wave divided by 2 (go and back)
    distance = duration * 0.034 / 2;

    // Update the led
    digitalWrite(led, ((distance < CONTAINER_FULL) ? LOW : HIGH));
}

void moveServos(Servo servo1, int base1, int value1, Servo servo2, int base2, int value2) {
    servo1.write(value1);
    delay(1000);
    servo1.write(base1);
    delay(500);
    servo2.write(value2);
    delay(1000);
    servo2.write(base2);
}