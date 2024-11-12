// Имитация реального контроллера 

#define BAUD_RATE 115200
#define LED_PIN 9

bool ledState = false;  // Состояние светодиода (включен/выключен)
int brightness = 100;   // Яркость в процентах (от 0 до 100)
int responseDelay = 50;  // Задержка перед ответом, мс

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(LED_PIN, OUTPUT);
  analogWrite(LED_PIN, 0);
}

void loop() {
  if (ledState == true) {
    // Преобразуем яркость из процентов в значение PWM (от 0 до 255)
    int pwmValue = map(brightness, 0, 100, 0, 255);
    analogWrite(LED_PIN, pwmValue);
  } else {
    // Выключаем светодиод
    analogWrite(LED_PIN, 0);
  }

  // Проверяем, есть ли доступные данные в буфере последовательного порта
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Читаем данные до символа новой строки
    command.trim(); // Удаляем лишние пробелы и символы новой строки

    if (command == "i") {
      // Команда запроса информации
      delay(responseDelay);
      Serial.println("i");
    }
    else if (command == "S") {
      // Команда включения светодиода
      delay(responseDelay);
      Serial.println("S");
      ledState = true;
    }
    else if (command == "s") {
      // Команда выключения светодиода
      delay(responseDelay);
      Serial.println("s");
      ledState = false;
    }
    else if (command.startsWith("p")) {
      // Команда установки яркости в формате "p100", где 100 - яркость от 0 до 100
      // Извлекаем числовое значение яркости из команды
      delay(responseDelay);
      Serial.println(command);
      String valueStr = command.substring(1); // Получаем подстроку после первого символа
      int value = valueStr.toInt(); // Конвертируем строку в число
      if (value >= 0 && value <= 100) {
        brightness = value; // Устанавливаем яркость
      } else {
        // Обработка некорректного значения яркости
        Serial.println("E1");  // Отправляем сообщение об ошибке
      }
    }
    else {
      // Обработка неизвестных команд
      delay(responseDelay);
      Serial.println("E2");
    }
  }
}
