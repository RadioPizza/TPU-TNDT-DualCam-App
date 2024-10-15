// Имитация контроллера нагревателя

#define BAUD_RATE 115200
#define LED_PIN 7
bool heaterState = false;

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "COMMAND1") {
      heaterState = true;
      Serial.println("ACK1");
      digitalWrite(LED_PIN, HIGH);
    } else if (command == "COMMAND2") {
      heaterState = false;
      Serial.println("ACK2");
      digitalWrite(LED_PIN, LOW);
    } else {
      Serial.println("Err");
    }
  }
}
