namespace TemperatureProject
{
    constexpr uint8_t ANALOG_PIN = A1; // where termistor is connected

    TemperatureScanner::TemperatureScanner()
    {
        this->temperatureCalculator = new TemperatureCalculator();
    }

    double TemperatureScanner::getValidatedTemp(const int numberOfRecords)
    {
        double maxTemp = 200;
        double minTemp = -200;
        double sum = 0;
        for (int i = 0; i < numberOfRecords; i++)
        {
            int raw = analogRead(ANALOG_PIN);
            double record = this->temperatureCalculator->getTemp(raw);
            sum += record;
            if (record < minTemp)
            {
                minTemp = record;
            }
            else if (record > maxTemp)
            {
                maxTemp = record;
            }
        }
        return sum / numberOfRecords;
    }
} // namespace TemperatureProject
