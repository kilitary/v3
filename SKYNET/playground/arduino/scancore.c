//#include <SPI.h>
//#define FAILURE_HANDLING
//#undef MINIMAL
#include <RF24.h>
#include <TaskScheduler.h>
//#include <iarduino_OLED_I2C.h>
//#if defined(TwoWire_h) || defined(__ARDUINO_WIRE_IMPLEMENTATION__) || defined(__AVR_ATmega328__) || defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega1284P__) || defined(__AVR_ATmega2560__) || defined(ESP8266) || defined(ESP32) || defined(ARDUINO_ARCH_RP2040) || defined(RENESAS_CORTEX_M4)  // Если подключена библиотека Wire или платы её поддерживают...
//#include <Wire.h>                                                                                                                                                                                                                                                                                   //	Разрешаем использовать библиотеку Wire в данной библиотеке.
//#endif                                                                                                                                                                                                                                                                                              //
//#if defined(iarduino_I2C_Software_h)                                                                                                                                                                                                                                                                //	Если библиотека iarduino_I2C_Software подключена в скетче...
//#include <iarduino_I2C_Software.h>                                                                                                                                                                                                                                                                  //	Разрешаем использовать библиотеку iarduino_I2C_Software в данной библиотеке.
//#endif

#define SCREEN_ADDRESS 0x3d
#define SCREEN_WIDTH 96   // OLED //info width, in pixels
#define SCREEN_HEIGHT 16  // OLED //info height, in pixels

//Adafruit_SSD1306 //info(SCREEN_WIDTH, SCREEN_HEIGHT);
//iarduino_OLED //info(SCREEN_ADDRESS);

unsigned long epochs = 0;

// Pin definitions
#define CE_PIN 7
#define PIN_EMPTY A4
#define PIN_BUZZER A1
#define CSN_PIN 10
#define END_CHECK_LED_PIN 4
#define SCAN_LED_PIN 6  // LED that blinks during scanning
#define RX_LED_PIN 8    // LED that lights when signal received

// NRF24 module configuration
RF24 radio(CE_PIN, CSN_PIN);
bool changing_channel = false;
unsigned sends = 0;
const uint8_t MIN_CHANNEL = 0;
uint8_t packetSize = 0;
const uint8_t MAX_CHANNEL = 125;  // NRF24 has channels 0-125
uint8_t currentChannel = MIN_CHANNEL;
unsigned totalRead = 0;
bool signalDetected = false;
unsigned int rand_skip = 0;
unsigned long centsEarned = 0;
unsigned prevSends = 0;
// Add RX detection timing
unsigned long lastChannelSwitch = 0;
const unsigned long RX_DETECT_WINDOW = 30;  // ms to wait for RX after channel switch
unsigned currentEarnRatio = 2250;
// Buffer for recei

uint8_t receivedData[32];  // NRF24 can receive up to 32 bytes
char randomeSpectreData[32] = "";
bool noscreen = 0;

// Add carrier detection variables
bool carrierDetected = false;
int carrierSignalCount = 0;
unsigned long lastCarrierCheck = 0;
const unsigned long CARRIER_CHECK_INTERVAL = 150;

// Task scheduler
Scheduler runner;

// Buffer to hold random frequency scan results
#define RANDOM_FREQ_SAMPLES 8
uint8_t randomFreqChannels[RANDOM_FREQ_SAMPLES];
uint8_t randomFreqStrength[RANDOM_FREQ_SAMPLES];  // 0-255 signal strength values

void sndtick(int tn = 1150);
void rnd_spect(int o = 2);

// Task declarations
void scanFrequencyCallback();
void checkReceivedSignalCallback();
void blinkScanLedCallback();
void flashRxLedCallback();
void infoCallback();
void sampleRandomFrequenciesCallback();
void writeCallback();

// Define tasks
Task scanFrequencyTask(250, TASK_FOREVER, &scanFrequencyCallback);
Task checkReceivedSignalTask(125, TASK_FOREVER, &checkReceivedSignalCallback);
Task blinkScanLedTask(500, TASK_FOREVER, &blinkScanLedCallback);
Task flashRxLedTask(400, TASK_FOREVER, &flashRxLedCallback);
Task infoTask(11150, TASK_FOREVER, &infoCallback);
Task writeTask(229, TASK_FOREVER, &writeCallback);
Task sampleRandomTask(200, TASK_FOREVER, &sampleRandomFrequenciesCallback);

void setup() {
    char txt[255] = "";

    // Initialize serial communication
    Serial.begin(115200);
    Serial.println("NRF24: Frequency Radio service starting");

    // Initialize LEDs
    pinMode(SCAN_LED_PIN, OUTPUT);
    pinMode(RX_LED_PIN, OUTPUT);
    pinMode(END_CHECK_LED_PIN, OUTPUT);
    pinMode(PIN_EMPTY, INPUT);
    // Clear RX LED at startup
    digitalWrite(RX_LED_PIN, LOW);
    digitalWrite(END_CHECK_LED_PIN, HIGH);
    rand_skip = analogRead(PIN_EMPTY);
    srandom(rand_skip);
    int o = random();
    Serial.print("NRF24: rand_skip=");
    Serial.println(rand_skip);
    Serial.print("NRF24: out=");
    Serial.println(o);
    rnd_spect();
    // Initialize NRF24 module
    Serial.println("NRF24: getting screen up");
    noscreen = true;
    //if (!//info.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    //    Serial.println(F("NRF24: SSD1306 allocation failed"));
    //    noscreen = true;
    //}
    //info.display();
    Serial.println("NRF24: getting radio up");
    if (!radio.begin()) {
        Serial.println("NRF24: Radio hardware not responding!");
        while (1) {}  // Hold in infinite loop
    }
    Serial.println("NRF24: radio up");
    //radio.toggle_features();
    //radio.errNotify();
    Serial.println("NRF24: common systems init done");
    //info.clearDisplay();
    //info.dim(0);
    //info.setTextWrap(true);
    //info.cp437(true);
    //info.setFont(&SmallFont);
    //info.setTextSize(1);                              // Normal 1:1 pixel scale
    //info.setTextColor(SSD1306_WHITE, SSD1306_BLACK);  // Draw white text
    //info.display();

    int is_nikolson = radio.isPVariant();
    //info.setCursor(0, 0);
    sprintf(txt, "%s nikolson with %s", (o % 2 == 2 ? "partial " : "full "), is_nikolson ? "nRF24L01+" : "nRF24 std");
    Serial.println(txt);

    //info.display();

    delay(1000);

    //info.invertDisplay(true);

    // Configure radio
    radio.setPALevel(RF24_PA_MAX);  // Set power level
    radio.setDataRate(RF24_1MBPS);  // Set data rate
    radio.setAutoAck(false);        // Disable auto-acknowledgment
    radio.setPayloadSize(32);       // Set payload size
    radio.disableCRC();             // Disable CRC

    delay(1555);

    // Start in receiving mode on first channel
    radio.setChannel(currentChannel);
    radio.startListening();

    //info.invertDisplay(false);
    //info.setRotation(0);
    //info.display();

    // Initialize task scheduler
    runner.init();
    runner.addTask(scanFrequencyTask);
    runner.addTask(checkReceivedSignalTask);
    runner.addTask(sampleRandomTask);
    runner.addTask(blinkScanLedTask);
    runner.addTask(flashRxLedTask);
    //runner.addTask(infoTask);
    runner.addTask(writeTask);

    Serial.println("NRF24: registered parallel functions");

    scanFrequencyTask.enable();
    checkReceivedSignalTask.enable();
    blinkScanLedTask.enable();
    //infoTask.enable();
    sampleRandomTask.enable();
    flashRxLedTask.enable();
    writeTask.enable();

    Serial.println("NRF24: tasks enabled");

    digitalWrite(END_CHECK_LED_PIN, LOW);

    // Enable tasks
    Serial.println("NRF24: Scanner initialized and running");

    int a = 3;
    while (a--) {
        sndtick();
        delay(200);
    }

    Serial.println("entering loop()");
}
void sndtick(int tn = 1150) {
    tone(PIN_BUZZER, tn, 55);
    digitalWrite(PIN_BUZZER, HIGH);
    delay(55);
    noTone(PIN_BUZZER);
    digitalWrite(PIN_BUZZER, LOW);
}

void rnd_spect(int o = 2) {
    if (o == 2) {
        o = random() % 9;
    }
    for (int i = 0; i < o; i++) {
        int a;

        a = random(10);
        if (random(a) < a / 3) {
            return;
        }
    }
}

void wait_switching(void) {
    char wt = 0;

    return;
    while (changing_channel && wt < 100) {
        delayMicroseconds(10);
        wt++;
    };
}

// Helper to get random frequency radio wave values with analog measurements
void sampleRandomFrequenciesCallback() {
    char txt[255] = "";
    int packetSize = 0;

    memset(receivedData, 0x0, sizeof(receivedData) - 1);

    for (int i = 0; i < RANDOM_FREQ_SAMPLES; i++) {
        uint8_t randChannel = MIN_CHANNEL + (rand() % (MAX_CHANNEL - MIN_CHANNEL + 1));
        randomFreqChannels[i] = randChannel;

        // Set to the random channel
        wait_switching();

        if (currentChannel != randChannel) {
            radio.stopListening();
            delayMicroseconds(150);
            radio.setChannel(randChannel);
            delayMicroseconds(150);
        }

        radio.startListening();

        // Measure signal activity by sampling multiple times
        uint8_t signalStrength = 0;
        for (int sample = 0; sample < 10; sample++) {
            //uint8_t flags = radio.clearStatusFlags();
            // Check for activity
            wait_switching();
            delayMicroseconds(150);
            if (radio.available()) {
                packetSize = radio.getDynamicPayloadSize();
                if (!packetSize) {
                    packetSize = radio.getPayloadSize();
                }

                if (packetSize > 0) {
                    // More bytes = stronger signal (generally)
                    signalStrength += packetSize;
                    radio.read(receivedData, sizeof(receivedData));
                    totalRead += packetSize;
                }
            }

            // Add environmental noise by reading analog pin
            // This adds true randomness based on RF and electrical noise
            signalStrength += (analogRead(A0) & 0x0F);  // Use lower 4 bits of analog noise

            delayMicroseconds(150);
        }

        // Store the resulting signal strength (normalized to 0-255)
        randomFreqStrength[i] = (signalStrength > 255) ? 255 : signalStrength;

        // Entropy collection - use timing differences between operations as additional source
        randomFreqStrength[i] ^= (micros() & 0xFF);
    }

    // Return to normal scanning channel

    if (radio.getChannel() != currentChannel) {
        wait_switching();
        radio.setChannel(currentChannel);
        delayMicroseconds(150);
    }

    // Print results with analog values
    if (packetSize) {
        sprintf(txt, "Random freq scan: packetSize: %d [", packetSize);
        Serial.print(txt);
        for (int i = 0; i < packetSize; i++) {
            Serial.print("Ch");
            Serial.print(randomFreqChannels[i]);
            Serial.print(":");
            Serial.print(randomFreqStrength[i]);
            Serial.print(" ");
        }
        Serial.println("]");
    }

    // Update the randomeSpectreData with these values for display
    for (int i = 0; i < RANDOM_FREQ_SAMPLES && i < 32; i++) {
        randomeSpectreData[i] = (char)randomFreqStrength[i];
    }
}
void markExec(void) {
    char txt[100] = "";
    if (epochs == 0 || epochs % 10 == 2) {
        sprintf(txt, "EXEC #%lu %lu", epochs, micros());
        Serial.println(txt);
    }
}

void loop() {
    char txt[255] = "";

    //markExec();

    runner.execute();

    // Enhanced carrier detection in main loop
    if (millis() - lastCarrierCheck >= CARRIER_CHECK_INTERVAL) {
        lastCarrierCheck = millis();

        // Check for carrier on current channel
        if (!changing_channel && radio.testCarrier()) {
            if (!carrierDetected) {
                carrierDetected = true;
                carrierSignalCount++;
                sndtick();
                Serial.print("Carrier detected on channel ");
                sprintf(txt, "%3u", currentChannel);
                Serial.print(txt);
                sprintf(txt, " %8u mhz", (unsigned)2400 + currentChannel);
                Serial.println(txt);
            }
        } else {
            carrierDetected = false;
        }
    }

    if (!changing_channel && radio.available()) {
        int bytes_avaible = 0;
        bytes_avaible = radio.getDynamicPayloadSize();
        if (!bytes_avaible) {
            bytes_avaible = radio.getPayloadSize();
        }

        if (bytes_avaible) {
            radio.read((void*)randomeSpectreData, min(bytes_avaible, sizeof(randomeSpectreData)));

            if (randomeSpectreData[0]) {
                // Call sndtick for each valid signal received
                sndtick();
                carrierSignalCount++;

                Serial.print("Signal received - calling sndtick(). Count: ");
                Serial.println(carrierSignalCount);
                Serial.print("bytes_avaible: ");
                Serial.println(bytes_avaible);
                Serial.print(", data: ");

                for (int i = 0; i < bytes_avaible; i++) {
                    Serial.print(randomeSpectreData[i], HEX);
                    Serial.print(" ");
                }
                Serial.println();
            }
        }
    }

    rnd_spect();

    checkReceivedSignalCallback();

    epochs++;
}

// Scan through available frequencies
void scanFrequencyCallback() {
    char txt[255] = "";
    changing_channel = true;
    // Move to the next channel
    currentChannel++;
    if (currentChannel > MAX_CHANNEL) {
        currentChannel = MIN_CHANNEL;
        sprintf(txt, "Completed full scan cycle (carriers detected: %d)", carrierSignalCount);
        Serial.println(txt);
        carrierSignalCount = 0;
    }
    //radio.flush_rx();
    //radio.flush_tx();
    delayMicroseconds(150);

    radio.stopListening();

    // Set the new channel
    delayMicroseconds(150);
    radio.setChannel(currentChannel);
    delayMicroseconds(150);
    // Flush RX buffer for stability
    //radio.flush_tx();
    ///radio.flush_rx();
    delayMicroseconds(150);
    radio.startListening();  // Resume listening
    delayMicroseconds(150);
    lastChannelSwitch = millis();
    //Serial.print("Scanning channel: ");
    //Serial.println(currentChannel);
    changing_channel = false;
}

void checkReceivedSignalCallback() {
    char txt[255] = "";
    // Only check for RX within a short window after switching channel
    if (millis() - lastChannelSwitch < RX_DETECT_WINDOW && !changing_channel) {
        //uint8_t flags = radio.clearStatusFlags();
        if (radio.available()) {
            // Get the data
            radio.read(&receivedData, sizeof(receivedData));
            sndtick();
            signalDetected = true;
            Serial.print("Signal detected on channel ");
            Serial.print(currentChannel);
            Serial.print(", data: ");

            for (int i = 0; i < 8; i++) {
                Serial.print(receivedData[i], HEX);
                Serial.print(" ");
            }
            Serial.println();

            // Debounce: only flash RX LED if not already flashing
            if (!flashRxLedTask.isEnabled()) {
                flashRxLedTask.restart();
                flashRxLedTask.enable();
            }
        }
    }
}

// Blink the scan LED
void blinkScanLedCallback() {
    static bool ledState = false;
    ledState = !ledState;
    digitalWrite(SCAN_LED_PIN, ledState);
}

// Flash the RX LED when signal is detected
void flashRxLedCallback() {
    static bool ledState = false;
    ledState = !ledState;
    digitalWrite(RX_LED_PIN, ledState);

    // Ensure RX LED is off after flashing
    if (flashRxLedTask.isLastIteration()) {
        digitalWrite(RX_LED_PIN, LOW);
        signalDetected = false;
    }
}
void writeCallback() {
    char txt[255] = "";

    if (rand() % 4 == 1 && !changing_channel) {
        digitalWrite(END_CHECK_LED_PIN, HIGH);
        int bytes = 1 + rand() % 32;
        char buf[bytes];
        for (int i = 0; i < bytes; i++) {
            buf[i] = (char)rand() % 255;
        }
        radio.stopListening();
        delayMicroseconds(150);
        radio.write(buf, bytes);
        delayMicroseconds(50);
        radio.startListening();
        delayMicroseconds(150);

        sends += bytes;

        sprintf(txt, "write %d bytes (%u total) to channel %u (freq: %-4dMHZ, cur: %u)", bytes, sends, radio.getChannel(), 2400 + currentChannel, currentChannel);
        Serial.println(txt);

        if (sends - prevSends >= currentEarnRatio) {
            prevSends = sends;
            centsEarned += 10;

            sndtick(899);

            sprintf(txt, "cash earned: %d, total: %lu", 10, (unsigned long)centsEarned * 100.0);
            Serial.println(txt);
        }
        digitalWrite(END_CHECK_LED_PIN, LOW);
        wait_switching();
        delayMicroseconds(150);
    }
}

void infoCallback() {
    char txt[255] = "";
    if (noscreen) {
        return;
    }

    //info.clearDisplay();

    //info.setTextSize(1);               // Normal 1:1 pixel scale
    //info.setTextColor(SSD1306_WHITE);  // Draw white text

    //info.setCursor(0, 5);
    sprintf(txt, "eph: %-9lu", epochs);
    //info.print(txt);

    //info.setCursor(0, 14);
    sprintf(txt, "chn: %-6u", currentChannel);
    //info.print(txt);
    //
    //info.setCursor(0, 21);
    sprintf(txt, "rcv: %-8d", totalRead);
    //info.print(txt);
    //
    //info.setCursor(0, 30);
    sprintf(txt, "snd: %-6u", sends);
    //info.print(txt);
    //
    //info.setCursor(60, 5);
    sprintf(txt, "csh: $%-6lu", ((unsigned long)centsEarned / 100));
    //info.print(txt);
    //
    // Add carrier signal count display
    //info.setCursor(60, 14);
    sprintf(txt, "car: %-6d", carrierSignalCount);
    //info.print(txt);
    //
    // Show carrier status indicator
    //info.setCursor(60, 21);
    //info.print(carrierDetected ? "CARR" : "-");

    //if (radio.failureDetected) {
    //    radio.begin();              // Attempt to re-configure the radio with defaults
    //    radio.failureDetected = 0;  // Reset the detection value
    //}

    //info.setCursor(60, 31);
    //info.print(carrierDetected ? "FIL" : "-");

    int frq = 2400 + currentChannel;
    //info.setCursor(60, 41);
    sprintf(txt, "frq: %-6dMHZ", frq);
    //info.print(txt);

    //info.setCursor(60, 51);
    sprintf(txt, "ARC: %-2d", radio.getARC());
    //info.print(txt);

    //
    //    //info.setCursor(0, 60);
    //    sprintf(txt, "snd: %-4u", current_sound_read);
    //    //info.print(txt);
    //
    //    //info.setCursor(65, 10);
    //    sprintf(txt, "sns: %-3u", sens);
    //    //info.print(txt);
    //
    //    //info.setCursor(65, 20);
    //    sprintf(txt, "ram: %-3u", freeRam());
    //    //info.print(txt);
    //
    //    //info.setCursor(65, 30);
    //    sprintf(txt, "mic: %-3u", current_mic_read);
    //    //info.print(txt);

    //info.display();
}
