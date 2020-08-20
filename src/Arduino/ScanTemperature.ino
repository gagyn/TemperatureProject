namespace TemperatureProject
{
  class TemperatureCalculator
  {
  private:
    double calculateVoltage(const int rawValue);
    double calculateResistance(const double voltage);
    double calculateTemp(const double resistance);

  public:
    double getTemp(const int rawInputValue);
  };

  class TemperatureScanner
  {
  private:
    TemperatureCalculator *temperatureCalculator;

  public:
    TemperatureScanner();
    double printRecords(const int numberOfRecords);
  };
} // namespace TemperatureProject

void setup()
{
  Serial.begin(19200);
  Serial.setTimeout(100);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop()
{
  if (!Serial.available())
  {
    delay(100);
    return;
  }
  int numberOfRecords = Serial.readString().toInt();
  TemperatureProject::TemperatureScanner scanner;
  scanner.printRecords(numberOfRecords);
}
