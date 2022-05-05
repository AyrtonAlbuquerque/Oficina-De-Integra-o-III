#include <Arduino.h>
#include <esp_camera.h>
#include <HTTPClient.h>
#include <WiFi.h>

/* -------------------------------------------------------------------------- */
/*                     Defines for CAMERA_MODEL_AI_THINKER                    */
/* -------------------------------------------------------------------------- */
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22
#define JPEG_QUALITY 10
#define FRAME_SIZE FRAMESIZE_UXGA

/* -------------------------------------------------------------------------- */
/*                     Number of WiFi connection attempts                     */
/* -------------------------------------------------------------------------- */
#define WIFI_ATTEMPTS 10

/* -------------------------------------------------------------------------- */
/*                               System Defines                               */
/* -------------------------------------------------------------------------- */
#define BOUD_RATE 9600

/* -------------------------------------------------------------------------- */
/*                              System Constants                              */
/* -------------------------------------------------------------------------- */
const char *ssid = "*****";
const char *password = "*****";
const char *url = "http://198.167.0.1/classification/request";

/* -------------------------------------------------------------------------- */
/*                            Function Declarations                           */
/* -------------------------------------------------------------------------- */
bool connectWiFi();

/* -------------------------------------------------------------------------- */
/*                                    Setup                                   */
/* -------------------------------------------------------------------------- */
void setup() {
    // Setup the serial communication
    Serial.begin(BOUD_RATE);

    // connect to WiFi
    if (connectWiFi()) {
        // Send message back to Arduinno
        Serial.println("Connected to WiFi");
    }

    // Setup camera configuration
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;

    // Configure frame size and quality
    if (psramFound()) {
        config.frame_size = FRAME_SIZE;
        config.jpeg_quality = JPEG_QUALITY;
        config.fb_count = 2;
    } else {
        config.frame_size = FRAMESIZE_SVGA;
        config.jpeg_quality = 12;
        config.fb_count = 1;
    }

    // Initialize the camera
    esp_err_t error = esp_camera_init(&config);
    if (error != ESP_OK) {
        Serial.printf("Camera initialization failed with error 0x%x", error);
        return;
    }
}

/* -------------------------------------------------------------------------- */
/*                                    Loop                                    */
/* -------------------------------------------------------------------------- */
void loop() {
    camera_fb_t *fb = NULL;
    HTTPClient client;
    int httpCode;

    // Message received from Arduino
    if (Serial.available()) {
        // Take a picture
        fb = esp_camera_fb_get();
        if (!fb) {
            Serial.println("Failed to capture image");
        } else {
            // Begin connection with the server
            client.begin(url);

            // If connected
            if (client.connected()) {
                // Send the request with the whole image in the body
                httpCode = client.POST(fb->buf, fb->len);

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
            // Return the frame buffer to be reused again
            esp_camera_fb_return(fb);
        }
    }
    delay(10);
}

/* -------------------------------------------------------------------------- */
/*                               WiFi Connection                              */
/* -------------------------------------------------------------------------- */
bool connectWiFi() {
    int attempt = 0;

    // Try to connect to wifi
    WiFi.begin(ssid, password);

    // While not connected keep trying for the number of attempts
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        // If not connect yet already over the max number of attempts
        if (attempt > WIFI_ATTEMPTS) { return false; }
        // Increase number of attempts
        attempt++;
    }

    return true;
}
