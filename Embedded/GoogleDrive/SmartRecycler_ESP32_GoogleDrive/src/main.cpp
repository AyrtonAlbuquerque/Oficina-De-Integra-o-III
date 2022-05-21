#include <WebServer.h>
#include <WiFi.h>
#include <esp32cam.h>

/* -------------------------------------------------------------------------- */
/*                              System Constants                              */
/* -------------------------------------------------------------------------- */
const char *ssid = "Ayrton_2G";
const char *password = "Ayrton297866*";
const char *url = "/images";
WebServer server(80);

/* -------------------------------------------------------------------------- */
/*                     Defines for CAMERA_MODEL_AI_THINKER                    */
/* -------------------------------------------------------------------------- */
#define BOUD_RATE 115200

/* -------------------------------------------------------------------------- */
/*                                Declarations                                */
/* -------------------------------------------------------------------------- */
void connectWiFi();

void sendImage();

/* -------------------------------------------------------------------------- */
/*                                    Setup                                   */
/* -------------------------------------------------------------------------- */
void setup() {
    // Initialize Serial
    Serial.begin(BOUD_RATE);
    Serial.println();

    // Camera configuration
    {
        using namespace esp32cam;
        Config cfg;
        cfg.setPins(pins::AiThinker);
        cfg.setResolution(esp32cam::Resolution::find(640, 480));
        cfg.setBufferCount(2);
        cfg.setJpeg(95);

        // Initialize the camera
        Serial.println(Camera.begin(cfg) ? "Camera initialized" : "Camera initialization failed");
    }

    // Setup server
    server.on(url, sendImage);
}

/* -------------------------------------------------------------------------- */
/*                                    Loop                                    */
/* -------------------------------------------------------------------------- */
void loop() {
    // If connected to WiFi
    if (WiFi.status() == WL_CONNECTED) {
        server.handleClient();
    } else {
        connectWiFi();
        server.begin();
    }
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

void sendImage() {
    WiFiClient client = server.client();
    auto frame = esp32cam::capture();

    // If failed to take picture
    if (frame == nullptr) {
        Serial.println("Failed to capture image");
        server.send(503, "", "");
    } else {
        Serial.printf("Image captured: Resolution: %dx%d, Size: %d bytes\n", frame->getWidth(), frame->getHeight(), static_cast<int>(frame->size()));
        server.setContentLength(frame->size());
        server.send(200, "image/jpeg");
        frame->writeTo(client);
    }
}