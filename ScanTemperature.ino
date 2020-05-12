int Uwe = 5;
float Uwy = 0;
float R1 = 122;
float R2 = 0;
float b = 0;
int analogPin = 0;
int ledOut = 2;

double calculateResistance(double voltage)
{
  b = voltage * Uwe;
  Uwy = (b) / 1024.0;
  b = (Uwe / Uwy) - 1;
  R2 = R1 * b;
  return R2;
}

double calculateTemp(double resistance)
{
  const int B = 3950;
  const double e = 2.71828182845;
  const int R0 = 10000;
  const double T0 = 25;
  
  double logRe = log(resistance) / log(R0*e);
  double temperature = 1 / ( logRe/B + 1/T0);
  return temperature;
}

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  double r = analogRead(analogPin);
  Serial.println(r);
  double resistance = calculateResistance(r);
  double temp = calculateTemp(resistance);
  
  if(temp > 24 && temp < 26)
  {
    digitalWrite(ledOut, HIGH);
  }
  else
  {
    digitalWrite(ledOut, LOW);
  }
  Serial.print("R: ");
  Serial.println(resistance);
  Serial.println(temp);
  delay(1000);
}
