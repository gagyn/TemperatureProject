namespace TemperatureProject
{
    constexpr uint8_t ANALOG_PIN = A1; // where termistor is connected

    TemperatureScanner::TemperatureScanner()
    {
        this->temperatureCalculator = new TemperatureCalculator();
    }

    inline double TemperatureScanner::printRecords(const int numberOfRecords)
    {
        for (int i = 0; i < numberOfRecords; i++)
        {
            int raw = analogRead(ANALOG_PIN);
            double record = this->temperatureCalculator->getTemp(raw);
            Serial.println(record);
        }
    }
} // namespace TemperatureProject
