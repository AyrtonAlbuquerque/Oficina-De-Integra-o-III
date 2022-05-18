#include <Arduino.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <esp32cam.h>
#include <esp_camera.h>

/* -------------------------------------------------------------------------- */
/*                                   Defines                                  */
/* -------------------------------------------------------------------------- */
#define WIDTH       1024
#define HEIGHT      768
#define QUALITY     95
#define BAUD_RATE   115200

/* -------------------------------------------------------------------------- */
/*                                   Globals                                  */
/* -------------------------------------------------------------------------- */
const char *ssid = "AndroidAP";
const char *password = "gisi6622";
const String url = "http://192.168.1.166:8081/classifications/request";
const String host = "192.168.1.166";
const int port = 8081;
const String recyclerID = "1";
int status = WL_IDLE_STATUS;
String bound = "boundry";

/* -------------------------------------------------------------------------- */
/*                                Declarations                                */
/* -------------------------------------------------------------------------- */
void connectWiFi();

void sendImage(camera_fb_t *frame, WiFiClient client);

void writeClient(camera_fb_t *frame, WiFiClient client);

void sendResponse(String message);

/* -------------------------------------------------------------------------- */
/*                                    Setup                                   */
/* -------------------------------------------------------------------------- */
void setup() {
    // Initialize Serial
    Serial.begin(BAUD_RATE);

    // Camera configuration
    {
        using namespace esp32cam;
        Config cfg;
        cfg.setPins(pins::AiThinker);
        cfg.setResolution(esp32cam::Resolution::find(WIDTH, HEIGHT));
        cfg.setBufferCount(2);
        cfg.setJpeg(QUALITY);

        // Initialize the camera
        sendResponse(Camera.begin(cfg) ? "Camera initialized" : "Camera initialization failed");
    }
}

void loop() {
    camera_fb_t *frame = NULL;
    WiFiClient client;

    // If connected to WiFi
    if (WiFi.status() == WL_CONNECTED) {
        // If message received from Arduino
        if (Serial.available()) {
            // Clear the Serial buffer
            Serial.readString();

            // Take a picture
            frame = esp_camera_fb_get();
            esp_camera_fb_return(frame);
            frame = esp_camera_fb_get();
            esp_camera_fb_return(frame);
            frame = esp_camera_fb_get();
            if (!frame) {
                sendResponse("Failed to capture image");
            } else {
                // Integration test
                sendResponse("{\"host\":\"" + host + "\",\"type\":\"" + String(rand() % 5) + "\",\"code\":\"sdjacbdert123dswedfeecf\",\"message\":\"Test message\"}");
            }
            // Return the frame buffer to be reused again
            esp_camera_fb_return(frame);
            frame = NULL;
        }
    } else {
        connectWiFi();
    }
    delay(10);
}

/* -------------------------------------------------------------------------- */
/*                                  Functions                                 */
/* -------------------------------------------------------------------------- */
void connectWiFi() {
    // Send message to be displayed
    sendResponse("Trying to connect to WiFi...");

    // Try to connect to wifi
    WiFi.begin(ssid, password);

    // While not connected keep trying until a connection is established
    while (WiFi.status() != WL_CONNECTED) { delay(500); }
}

void sendImage(camera_fb_t *frame, WiFiClient client) {
    String form = "--" + bound + "\r\nContent-Disposition: form-data; name=\"recyclerID\"" + "\r\n\r\n" + recyclerID + "\r\n";
    String head = "--" + bound + "\r\nContent-Disposition: form-data; name=\"file\";filename=\"image.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";
    String tail = "\r\n--" + bound + "--\r\n";
    uint32_t length = form.length() + frame->len + head.length() + tail.length();
    char buffer[form.length() + 1];
    form.toCharArray(buffer, form.length() + 1);

    // Send post
    client.println("POST " + url + " HTTP/1.1");
    client.println("Host: " + host);
    client.println("Content-Length: " + String(length));
    client.println("Content-Type: multipart/form-data; boundary=" + bound);
    client.println();
    client.write(buffer);
    client.println();
    client.print(head);
    writeClient(frame, client);
    client.print(tail);
}

void writeClient(camera_fb_t *frame, WiFiClient client) {
    uint8_t *buffer = frame->buf;
    size_t length = frame->len;
    size_t remainder;

    for (size_t i = 0; i < length; i = i + 1024) {
        if (i + 1024 < length) {
            client.write(buffer, 1024);
            buffer += 1024;
        } else if (length % 1024 > 0) {
            remainder = length % 1024;
            client.write(buffer, remainder);
        }
    }
}

void sendResponse(String message) {
    DynamicJsonDocument doc(1024);
    DynamicJsonDocument response(1024);
    int begin = message.indexOf("{");
    int end = message.lastIndexOf("}");

    // Build the final response
    if (begin != -1 && end != -1) {
        DeserializationError error = deserializeJson(doc, message.substring(begin, end + 1));
        response["host"] = host;
        response["code"] = doc["redeem_code"];
        response["type"] = doc["class"];
        response["message"] = error ? message : doc["message"];
    } else {
        response["host"] = host;
        response["code"] = doc["redeem_code"];
        response["type"] = doc["class"];
        response["message"] = message;
    }

    // Send response
    serializeJson(response, Serial);
}