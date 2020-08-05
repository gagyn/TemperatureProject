namespace TemperatureProject
{
  constexpr int ARDUINO_MAX_VOLTAGE = 5;
  constexpr int R1 = 46000; // first resistor in circuit - check yours

  // values specified for concrete thermistor - yours probably has different values
  constexpr int B = 3950;
  constexpr int R0 = 10000;
  constexpr double T0 = 273.15 + 25;

  inline double TemperatureCalculator::calculateVoltage(const int rawValue)
  {
    double b = rawValue * ARDUINO_MAX_VOLTAGE;
    double voltage = b / 1024.0;
    return voltage;
  }

  inline double TemperatureCalculator::calculateResistance(const double voltage)
  {
    double b = (ARDUINO_MAX_VOLTAGE / voltage) - 1;
    double R2 = R1 * b;
    return R2;
  }

  inline double TemperatureCalculator::calculateTemp(const double resistance)
  {
    double logR = log(resistance / R0);
    double reversedT = 1 / T0 + 1 / B * logR;
    return 1 / reversedT - 273.15;
  }

  inline double TemperatureCalculator::getTemp(const int rawInputValue)
  {
    double voltage = this->calculateVoltage(rawInputValue);
    double resistance = this->calculateResistance(voltage);
    return this->calculateTemp(resistance);
  }
} // namespace TemperatureProject