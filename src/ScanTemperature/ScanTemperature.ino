#define ANALOG_PIN A1 // where termistor is connected
#define ARDUINO_MAX_VOLTAGE 5
#define R1 46000 // first resistor in circuit - check yours

// values specified for concrete thermistor - yours probably has different values
#define B 3950
#define R0 10000
#define T0 273.15 + 25

class TemperatureCalculator
{
private:
  double calculateVoltage(const int rawValue)
  {
    double b = rawValue * ARDUINO_MAX_VOLTAGE;
    double voltage = b / 1024.0;
    return voltage;
  }

  double calculateResistance(const double voltage)
  {
    double b = (ARDUINO_MAX_VOLTAGE / voltage) - 1;
    double R2 = R1 * b;
    return R2;
  }

  double calculateTemp(const double resistance)
  {
    double logR = log(resistance / R0);
    double reversedT = 1 / T0 + 1 / B * logR;
    return 1 / reversedT - 273.15;
  }

public:
  double getTemp()
  {
    int raw = analogRead(ANALOG_PIN);
    double voltage = calculateVoltage(raw);
    double resistance = calculateResistance(voltage);
    return calculateTemp(resistance);
  }
};

double calculateAverage(const int numberOfRecords)
{
  double minTemp = 100;
  double maxTemp = -100;
  double sumTemp = 0;
  TemperatureCalculator calculator;
  for (int i = 0; i < numberOfRecords; i++)
  {
    double record = calculator.getTemp();
    if (record < minTemp)
    {
      minTemp = record;
    }
    if (record > maxTemp)
    {
      maxTemp = record;
    }
    sumTemp += record;
  }
  sumTemp -= minTemp;
  sumTemp -= maxTemp;
  return sumTemp / (numberOfRecords - 2);
}

void setup()
{
  Serial.begin(19200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop()
{
  const int numberOfRecords = 2000;
  double temp = calculateAverage(numberOfRecords);
  Serial.println(temp);
  delay(30 * 1000);
}
