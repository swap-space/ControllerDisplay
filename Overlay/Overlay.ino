#define dataLatchPin 2
#define dataClockPin 3
#define dataPin 4
#define dataMask (1<<dataPin)

static union
{
  uint8_t controllerBytes[2];
  uint16_t controllerState = 0x00;
};

static volatile bool sendState = false;
static volatile uint8_t currentClock = 0;

//void dataLatch()
ISR(INT0_vect)
{
  currentClock = 0;
  controllerState = 0x00;
  EIFR &= ~0x01;
//  reti();
}

#define DATA_STATE (((~PIND) & dataMask)>>4)

//void dataClock()
ISR(INT1_vect)
{
  controllerState |= (DATA_STATE << currentClock++);
  if(currentClock >= 12)
    sendState = true;
  EIFR &= ~0x02;
//  reti();
}

void setup() {
  Serial.begin(250000);
  
  pinMode(dataLatchPin, INPUT);
  pinMode(dataClockPin, INPUT);
  pinMode(dataPin, INPUT);

  cli();

  // Enable the latch and clock interrupts
  EICRA &= 0xF0;
  EICRA |= ((0x02<<2) | 0x03);
  EIMSK |= 0x03;
  EIFR = 0;

  // Disable all other interrupts (except UART)
  PCICR = 0;
  EECR = 0;
  WDTCSR = 0;
  TIMSK0 = 0;
  TIMSK1 = 0;
  TIMSK2 = 0;
  SPCR = 0;
  TWCR = 0;
  ACSR = 0xF0;
  ACSR = 0x00;
  ADCSRA = 0;

  sei();
  
//  attachInterrupt(digitalPinToInterrupt(dataLatchPin), dataLatch, RISING);
//  attachInterrupt(digitalPinToInterrupt(dataClockPin), dataClock, FALLING);
}

void loop() {
  while(!sendState);
  sendState = false;
  controllerState &= 0x0FFF;
  Serial.write("FF");
  Serial.write(controllerBytes[0]);
  Serial.write(controllerBytes[1]);
}
