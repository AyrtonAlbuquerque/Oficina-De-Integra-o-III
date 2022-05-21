#include <Arduino.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <esp32cam.h>

/* -------------------------------------------------------------------------- */
/*                                   Defines                                  */
/* -------------------------------------------------------------------------- */
#define WIDTH       640
#define HEIGHT      480
#define QUALITY     95
#define BOUD_RATE   115200

/* -------------------------------------------------------------------------- */
/*                                   Globals                                  */
/* -------------------------------------------------------------------------- */
const char* ssid = "Ayrton_2G";
const char* password = "Ayrton297866*";
const char* url = "http://198.167.0.1/classification/request";
const char* host = "198.167.0.1";

/* -------------------------------------------------------------------------- */
/*                                Declarations                                */
/* -------------------------------------------------------------------------- */
void connectWiFi();

void sendResponse(String message);

/* -------------------------------------------------------------------------- */
/*                                    Setup                                   */
/* -------------------------------------------------------------------------- */
void setup() {
    // Initialize Serial
    Serial.begin(BOUD_RATE);

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

/* -------------------------------------------------------------------------- */
/*                                    Loop                                    */
/* -------------------------------------------------------------------------- */
void loop() {
    HTTPClient client;
    int httpCode;

    // If connected to WiFi
    if (WiFi.status() == WL_CONNECTED) {
        // If message received from Arduino
        if (Serial.available()) {
            // Clear the Serial buffer
            Serial.readString();

            // Take a picture
            auto frame = esp32cam::Camera.capture();
            if (frame == nullptr) {
                sendResponse("Failed to capture image");
            } else {
                // Begin connection with the server
                client.begin(url);

                // If connected
                if (client.connected()) {
                    // Set header content type
                    client.addHeader("Content-Type", "multipart/form-data");
                    // Send the request with the whole image in the body
                    httpCode = client.POST(frame->data(), frame->size());

                    // If code is negative an error accoured
                    if (httpCode > 0) {
                        // Image processed by the server
                        if (httpCode == HTTP_CODE_OK) {
                            // Send response to Arduino
                            sendResponse(client.getString());
                        }
                    } else {
                        // On error send it to Arduino as well
                        sendResponse("HTTP POST failed");
                    }
                    // End the client connection
                    client.end();
                } else {
                    // Could not connect to server, send message to Arduino
                    sendResponse("Could not connect to server");
                }
                // Release the frame
                frame.release();
            }
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

void sendResponse(String message) {
    DynamicJsonDocument doc(1024);
    DynamicJsonDocument response(1024);
    DeserializationError error = deserializeJson(doc, message);

    // Build the final response
    response["host"] = host;
    response["code"] = doc["redeem_code"];
    response["type"] = doc["class"];
    response["message"] = error ? message : doc["message"];

    // Send response
    serializeJson(response, Serial);
}