#include <Arduino.h>
#include <math.h>

// ESP32 demonstrator: ADC-based sensor acquisition + smoothed proportional control.
// Wiring: analog sensor -> GPIO34 (3.3V MAX); output LED/transistor input -> GPIO25.
// Never connect an unknown voltage or high-current load directly to the board.
constexpr uint8_t SENSOR_PIN = 34;
constexpr uint8_t OUTPUT_PIN = 25;
constexpr float VREF = 3.3f;
constexpr float SETPOINT_VOLTS = 1.65f;
constexpr float KP = 0.25f;
constexpr unsigned long PERIOD_MS = 100;
float filteredVoltage = 0.0f;
unsigned long lastSample = 0;

void setup() {
  Serial.begin(115200);
  pinMode(SENSOR_PIN, INPUT);
  pinMode(OUTPUT_PIN, OUTPUT);
  analogReadResolution(12);
  analogSetPinAttenuation(SENSOR_PIN, ADC_11db);
  Serial.println("timestamp_ms,voltage,filtered_voltage,control_output");
}

void loop() {
  unsigned long now = millis();
  if (now - lastSample < PERIOD_MS) return;
  lastSample = now;
  const int raw = analogRead(SENSOR_PIN);
  const float voltage = (raw / 4095.0f) * VREF; // illustrative; calibrate actual ESP32 ADC
  filteredVoltage = 0.15f * voltage + 0.85f * filteredVoltage;
  const float error = SETPOINT_VOLTS - filteredVoltage;
  const float output = constrain(0.5f + KP * error, 0.0f, 1.0f);
  // Binary digital indicator. Replace with PWM only after verifying attached hardware.
  digitalWrite(OUTPUT_PIN, output > 0.5f ? HIGH : LOW);
  Serial.print(now); Serial.print(',');
  Serial.print(voltage, 4); Serial.print(',');
  Serial.print(filteredVoltage, 4); Serial.print(',');
  Serial.println(output, 4);
}
