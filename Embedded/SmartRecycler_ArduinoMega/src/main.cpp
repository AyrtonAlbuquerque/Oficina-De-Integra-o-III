#include <Arduino.h>
#include <Wire.h>
#include <Servo.h>
#include <LCDWIKI_GUI.h>
#include <SSD1283A.h>
#include <qrcode.h>
#include <ArduinoJson.h>
#include "MedianFilterLib2.h"
//#include <avr8-stub.h> // Debugging only

/* -------------------------------------------------------------------------- */
/*                                   Defines                                  */
/* -------------------------------------------------------------------------- */
#define ECHO1           2
#define ECHO2           3
#define ECHO3           4
#define ECHO4           5
#define SERVOT_PIN      8
#define SERVOL_PIN      9
#define SERVOR_PIN      10
#define LED_TAPE_PIN    12
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
#define DISPLAY_CS      53
#define DISPLAY_DC      47
#define DISPLAY_RESET   48
#define DISPLAY_LED     43
#define DISPLAY_SCK     52
#define DISPLAY_SDA     51
#define WIDTH           128
#define HEIGHT          64
#define BOUD_RATE       115200
#define PROCESS_TIMEOUT 15000
#define CONTAINER_COUNT 4
#define CONTAINER_FULL  10
#define IR_TIME         1000
#define INITIAL_DELAY   2000
#define QRCODE_VERSION  3
#define QRCODE_ECC      ECC_LOW
#define BLACK           0x0000
#define WHITE           0xFFFF

/* -------------------------------------------------------------------------- */
/*                                    Types                                   */
/* -------------------------------------------------------------------------- */
typedef struct waste_t {
    char *host;
    char *type;
    char *code;
    char *message;
} Waste;

typedef struct led_t {
    int metal;
    int plastic;
    int paper;
    int other;
} Led;


/* -------------------------------------------------------------------------- */
/*                                   Globals                                  */
/* -------------------------------------------------------------------------- */
Servo servoT;
Servo servoL;
Servo servoR;
Led containers;
bool processing;
long start;
String current_message = "";

/* -------------------------------------------------------------------------- */
/*                                Declarations                                */
/* -------------------------------------------------------------------------- */
SSD1283A_GUI display(DISPLAY_CS, DISPLAY_DC, DISPLAY_RESET, DISPLAY_LED);

Waste *parseResponse(String response);

void recycle(Waste *item);

void generateQRCode(Waste *item);

void updateLED(int container);

void moveServos(Servo servo1, int base1, int value1, Servo servo2, int base2, int value2);

bool checkSensor();

void displayMessage(String message);

String getResponse();

/* -------------------------------------------------------------------------- */
/*                                    Setup                                   */
/* -------------------------------------------------------------------------- */
void setup() {
    // For debuggig only
//    debug_init();

    // Setup system variables
    processing = false;

    // Setup the serial
    Serial3.begin(BOUD_RATE);

    // Setup pin modes
    pinMode(IR1_PIN, INPUT);
    pinMode(IR2_PIN, INPUT);
    pinMode(ECHO1, INPUT);
    pinMode(ECHO2, INPUT);
    pinMode(ECHO3, INPUT);
    pinMode(LED1_PIN, OUTPUT);
    pinMode(LED2_PIN, OUTPUT);
    pinMode(LED3_PIN, OUTPUT);
    pinMode(LED4_PIN, OUTPUT);
    pinMode(TRIGGER1, OUTPUT);
    pinMode(TRIGGER2, OUTPUT);
    pinMode(TRIGGER3, OUTPUT);
    pinMode(TRIGEGR4, OUTPUT);
    pinMode(TRIGEGR4, OUTPUT);
    pinMode(LED_TAPE_PIN, OUTPUT);

    // Setup Leds and Led tape
    digitalWrite(LED1_PIN, HIGH);
    digitalWrite(LED2_PIN, HIGH);
    digitalWrite(LED3_PIN, HIGH);
    digitalWrite(LED4_PIN, HIGH);
    digitalWrite(LED_TAPE_PIN, HIGH);

    // Setup servos
    servoT.attach(SERVOT_PIN);
    servoR.attach(SERVOR_PIN);
    servoL.attach(SERVOL_PIN);

    // Initialial Container setup
    containers.metal = LOW;
    containers.plastic = LOW;
    containers.paper = LOW;
    containers.other = LOW;

    // Setup de display
    display.init();
    display.fillScreen(BLACK);
}

/* -------------------------------------------------------------------------- */
/*                                    Loop                                    */
/* -------------------------------------------------------------------------- */
void loop() {
    Waste *item = NULL;

    // If not processing waste
    if (!processing) {
        // If the IR Sensor is active for a minimal duration than start processing
        if (checkSensor()) {
            processing = true;
            start = millis();

            // Display processing massage
            displayMessage("Processing...");
            // Waste processing begins. wait for a moment
            delay(INITIAL_DELAY);
            // Turn on the Led tape
            digitalWrite(LED_TAPE_PIN, LOW);
            // Notify ESP32 to take a picture and get classification
            Serial3.println(".");
        } else {
            // If not processing, check and display messages from ESP32
            if (Serial3.available()) {
                // Handle the serial message
                String response = getResponse();

                // If it is a valid response
                if (response != "") {
                    item = parseResponse(response);
                    displayMessage(item->message);
                    free(item);
                }
            } else {
                if (!current_message.equals("Smart Recycler"))
                    displayMessage("Smart Recycler");
            }
        }
    } else {
        // While processing timeout has not been reached
        if ((millis() - start) <= PROCESS_TIMEOUT) {
            // If there is a response from ESP32
            if (Serial3.available()) {
                // Handle the serial message
                String response = getResponse();

                // If it is a valid message
                if (response != "") {
                    // Parse the response string
                    item = parseResponse(response);

                    // If item type is NULL or empty than its just a message from ESP32
                    if (String(item->type).equals("") || !(item->type)) {
                        // Display the message in the screen
                        displayMessage(item->message);
                    }

                    // Turn off led tape and recycle item
                    digitalWrite(LED_TAPE_PIN, HIGH);
                    recycle(item);
                    free(item);
                    processing = false;
                }
            }
        } else {
            // Turn off led tape and recycle item to others
            digitalWrite(LED_TAPE_PIN, HIGH);
            recycle(item);
            free(item);
            displayMessage("Smart Recycler");
            processing = false;
        }
    }
    delay(10);
}

/* -------------------------------------------------------------------------- */
/*                                  Functions                                 */
/* -------------------------------------------------------------------------- */
Waste *parseResponse(String response) {
    Waste *item;
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, response);

    item = (Waste *) malloc(sizeof(Waste));

    // Parse the response to the item structure
    item->type = doc["type"];
    item->host = doc["host"];
    item->code = doc["code"];
    item->message = doc["message"];

    return item;
}

void recycle(Waste *item) {
    if (item->type) {
        // Generate and show QRCode
        generateQRCode(item);

        // Waste treatment based on type (0 -> Metals | 1-2 -> Paper | 3-5 -> Plastic | Other)
        if (String(item->type).equals("0") && containers.metal == LOW)
            moveServos(servoT, 0, 90, servoR, 0, 90);
        else if ((String(item->type).equals("1") || String(item->type).equals("2")) && containers.paper == LOW)
            moveServos(servoT, 0, 90, servoR, 180, 90);
        else if ((String(item->type).equals("3") || String(item->type).equals("4") || String(item->type).equals("5")) && containers.plastic == LOW)
            moveServos(servoT, 180, 90, servoL, 0, 90);
        else
            moveServos(servoT, 180, 90, servoL, 180, 90);

        // Delay to let the item fall into the bin before updating leds
        delay(1000);

        // Update the containers leves
        for (size_t i = 0; i < CONTAINER_COUNT; i++) {
            updateLED(i);
        }
    }
}

void generateQRCode(Waste *item) {
    QRCode qrcode;
    int offset_x = 7;
    int offset_y = 10;
    uint8_t data[qrcode_getBufferSize(QRCODE_VERSION)];
    String url = "http://" + String(item->host) + ":8081?r=" + String(item->code) + "&l=" + String(item->type);
    String text = (String(item->type).equals("0") ? "METAL" :
                   (String(item->type).equals("1") || String(item->type).equals("2")) ? "PAPER" :
                   (String(item->type).equals("3") || String(item->type).equals("4") || String(item->type).equals("5")) ? "PLASTIC" : "OTHER");

    // Create the QRCode
    qrcode_initText(&qrcode, data, QRCODE_VERSION, QRCODE_ECC, url.c_str());

    // Prepare the display
    display.fillScreen(BLACK);
    // Print Classification
    display.Set_Text_colour(WHITE);
    display.Set_Text_Back_colour(BLACK);
    display.Set_Text_Size(1);
    display.Print_String(text, 65 - text.length() * 3, 0);
    // Print QR Code
    for (int y = 0; y < qrcode.size; y++) {
        for (int x = 0; x < qrcode.size; x++) {
            int newX = offset_x + (4 * x);
            int newY = offset_y + (4 * y);

            if (qrcode_getModule(&qrcode, x, y)) {
                display.fillRect(newX, newY, 4, 4, WHITE);
            } else {
                display.fillRect(newX, newY, 4, 4, BLACK);
            }
        }
    }
}

void updateLED(int container) {
    int trigger = (container == 0) ? TRIGGER1 : ((container == 1) ? TRIGGER2 : ((container == 2) ? TRIGGER3
                                                                                                 : TRIGEGR4));
    int echo = (container == 0) ? ECHO1 : ((container == 1) ? ECHO2 : ((container == 2) ? ECHO3 : ECHO4));
    int led = (container == 0) ? LED1_PIN : ((container == 1) ? LED2_PIN : ((container == 2) ? LED3_PIN : LED4_PIN));
    MedianFilter2<int> medianFilter(15);
    long duration;
    int distance;

    for (int i = 0; i < 15; i++) {
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
        medianFilter.AddValue(distance);
    }
    distance = medianFilter.GetFiltered();

    // Update the leds and the containers struct
    containers.metal = (container == 0) ? ((distance < CONTAINER_FULL) ? LOW : HIGH) : containers.metal;
    containers.paper = (container == 1) ? ((distance < CONTAINER_FULL) ? LOW : HIGH) : containers.paper;
    containers.metal = (container == 2) ? ((distance < CONTAINER_FULL) ? LOW : HIGH) : containers.metal;
    containers.metal = (container == 3) ? ((distance < CONTAINER_FULL) ? LOW : HIGH) : containers.metal;
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
    delay(500);
}

bool checkSensor() {
    if (digitalRead(IR1_PIN) == LOW && digitalRead(IR2_PIN) == LOW) {
        delay(IR_TIME);
        return (digitalRead(IR1_PIN) == LOW && digitalRead(IR2_PIN) == LOW);
    }
    return false;
}

void displayMessage(String message) {
    int x = 65 - message.length() * 3;

    // If x possition on display is less than 0, than set to 0
    x = (x < 0) ? 0 : x;

    // Serial.println(message);
    display.fillScreen(BLACK);
    display.Set_Text_colour(WHITE);
    display.Set_Text_Back_colour(BLACK);
    display.Set_Text_Size(1);
    display.Print_String(message, x, 58);
    current_message = message;
}

String getResponse() {
    String response = "";
    String data = Serial3.readString();
    int begin = data.indexOf('{');
    int end = data.lastIndexOf("}");

    if (begin != -1 && end != -1) {
        // Messages received are always a JSON, so take from first "{" to last "}"
        response = data.substring(begin, end + 1);
    }

    return response;
}