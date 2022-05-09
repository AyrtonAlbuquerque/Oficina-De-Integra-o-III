#include <Arduino.h>
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
const char *ssid = "Ayrton_2G";
const char *password = "Ayrton297866*";
const char *url = "http://198.167.0.1/classification/request";

/* -------------------------------------------------------------------------- */
/*                                Declarations                                */
/* -------------------------------------------------------------------------- */
void connectWiFi();

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
        Serial.println(Camera.begin(cfg) ? "Camera initialized" : "Camera initialization failed");
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
            // Take a picture
            auto frame = esp32cam::Camera.capture();
            if (frame == nullptr) {
                Serial.println("Failed to capture image");
            } else {
                // Begin connection with the server
                client.begin(url);

                // If connected
                if (client.connected()) {
                    // Set header content type to image/jpeg
                    client.addHeader("Content-Type", "image/jpg");
                    // Send the request with the whole image in the body
                    httpCode = client.POST(frame->data(), frame->size());

                    // If code is negative an error accoured
                    if (httpCode > 0) {
                        // Image processed by the server
                        if (httpCode == HTTP_CODE_OK) {
                            // Get response and send it to Arduino
                            Serial.println(client.getString());
                        }
                    } else {
                        // On error send it to Arduino as well
                        Serial.printf("HTTP POST failed with error: %s\n", client.errorToString(httpCode).c_str());
                    }
                    // End the client connection
                    client.end();
                } else {
                    // Could not connect to server, send message to Arduino
                    Serial.println("Could not connect to server");
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
    Serial.println("Trying to connect to WiFi...");

    // Try to connect to wifi
    WiFi.begin(ssid, password);

    // While not connected keep trying until a connection is established
    while (WiFi.status() != WL_CONNECTED) { delay(500); }
}
