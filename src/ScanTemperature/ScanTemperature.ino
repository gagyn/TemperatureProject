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
    double getValidatedTemp(const int numberOfRecords);
  };
} // namespace TemperatureProject

void setup()
{
  Serial.begin(19200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop()
{
  const int numberOfRecords = 2000;
  TemperatureProject::TemperatureScanner scanner;
  double temp = scanner.getValidatedTemp(numberOfRecords);
  Serial.println(temp);
  delay(30 * 1000);
}
