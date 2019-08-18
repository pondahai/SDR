/*
  LiquidCrystal Library - Hello World

 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.

 This sketch prints "Hello World!" to the LCD
 and shows the time.

  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe
 modified 7 Nov 2016
 by Arturo Guadalupi

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/LiquidCrystalHelloWorld

*/

// include the library code:
#include <LiquidCrystal.h>
#include <Wire.h>
#include <Adafruit_SI5351.h>
#include <DTMF.h>

int sensorPin = A1;
float n=128.0;
float sampling_rate=8926.0;
DTMF dtmf = DTMF(n,sampling_rate);


Adafruit_SI5351 clockgen = Adafruit_SI5351();

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 6, d5 = 7, d6 = 8, d7 = 9;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
//
const byte interruptPin = 2;
const byte rotateEncoderPin = 3;

//volatile uint32_t vfo = 40000000L;
//volatile uint32_t vfo = 39356000L;
//volatile uint32_t vfo = 30000000L;
//volatile uint32_t vfo = 27000000L;
//volatile uint32_t vfo = 25556000L;
//volatile uint32_t vfo = 19816000L;
//volatile uint32_t vfo = 27000000L;
//volatile uint32_t vfo = 17460000L;
//volatile uint32_t vfo = 15000000L;
//volatile uint32_t vfo = 14940000L;
//volatile uint32_t vfo = 11430000L;
//volatile uint32_t vfo = 13605000L;
//volatile uint32_t vfo = 9839000L;
//volatile uint32_t vfo = 9505000L;
//volatile uint32_t vfo = 9276000L;
//volatile uint32_t vfo = 8100000L;
//volatile uint32_t vfo = 7925000L;
//volatile uint32_t vfo = 7404000L;
//volatile uint32_t vfo = 7342000L;
//volatile uint32_t vfo = 6389000L;
//volatile uint32_t vfo = 5923000L;
//volatile uint32_t vfo = 5442000L;
//volatile uint32_t vfo = 4954000L;
//volatile uint32_t vfo = 4625000L;
//volatile uint32_t vfo = 1500000L;
//volatile uint32_t vfo = 1000000L;
volatile uint32_t vfo = 830000L;
//volatile uint32_t vfo = 500000L;

const uint32_t radix = 1000L; //start step size 1kHz
boolean changed_f = 1;
uint32_t si5351denomi = 1000000L; //Multicounter denominator one million
uint32_t si5351nomi; // Multicounter nominator
uint32_t si5351multi_int;  // Multicounter integer
uint32_t si5351multiCount; // Multicounter 
uint32_t pllFreq; // si5351 internal vco frequency
uint32_t si5351divider; // VCO output divider integer part
//


//
void count_frequency()
{
  uint32_t f, g;
// lcd.clear();
  lcd.setCursor(3,0);
  f = (vfo*4) / 1000000L;   //variable is now vfo instead of 'frequency' vfo esim 145787500
  si5351divider = 900000000L/(vfo*4); // vfo divider integer
  pllFreq = si5351divider * (vfo*4); // counts pllFrequency
  si5351multiCount = pllFreq / 25L; // feedback divider
  si5351multi_int = pllFreq / 25000000L; // feedback divider integer
  si5351nomi = si5351multiCount % 1000000L;  // feedback divider integer
  si5351denomi = 1000000L; // feedback divider fraktion
  Serial.print(" (vfo*4) ");
  Serial.println( (vfo*4));  
//  Serial.print(" pllFreq ");
//  Serial.println( pllFreq);
//  Serial.print("si5351divider ");
//  Serial.println(si5351divider);
//  Serial.print(" si5351multiCount ");
//  Serial.println(si5351multiCount);
//  Serial.print(" si5351multi_int ");
//  Serial.println(si5351multi_int);
//  Serial.print(" si5351nomi ");
//  Serial.println(si5351nomi);
//  Serial.print(" si5351denomi ");
//  Serial.println(si5351denomi);
 // Serial.println(f = vfo / 1000000); // printtaa f 145.XXX.XXX
  if (f < 10)
   lcd.print("");
  lcd.print(f);
  lcd.print(",");
  f = ((vfo*4) % 1000000L) / 1000L; // printtaa taajuuden 3 viim numeroa XXX.550.XXX
 // Serial.println (f = (vfo % 1000000) / 1000);
  if (f < 100)
    lcd.print("0");
  if (f < 10)
    lcd.print("0");
  lcd.print(f);
  lcd.print(".");
 // f = vfo % 1000;
   f = ((vfo*4) % 1000L) / 100L; // removing 2 last digit from frequency reading 
 // Serial.println( f = vfo % 1000); // printtaa XXX.XXX.000
 // if (f < 100)
   // lcd.print("0");
 // if (f < 10)
  //  lcd.print("0");
  lcd.print(f); //
  lcd.print("kHz ");
 // lcd.setCursor(0, 0);
 // lcd.print(tbfo);
//  Serial.println(vfo + bfo);
//  Serial.println(tbfo);
//////
  f = (vfo) / 1000000L;   //variable is now vfo instead of 'frequency' vfo esim 145787500
  lcd.setCursor(3,1);
    if (f < 10)
  lcd.print("");
  lcd.print(f);
  lcd.print(",");
  f = ((vfo) % 1000000L) / 1000L; // printtaa taajuuden 3 viim numeroa XXX.550.XXX
  if (f < 100)
    lcd.print("0");
  if (f < 10)
    lcd.print("0");
  lcd.print(f);
  lcd.print(".");
  f = ((vfo) % 1000L) / 100L; // removing 2 last digit from frequency reading 
  lcd.print(f); //
  lcd.print("kHz ");
  
}
//


void setup() {
  Serial.begin(115200);
  delay(300);
  Serial.println("Si5351 Clockgen Test"); Serial.println("");
  /* Initialise the sensor */
  if (clockgen.begin() != ERROR_NONE)
  {
    /* There was a problem detecting the IC ... check your connections */
    Serial.print("Ooops, no Si5351 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  Serial.println("OK!");

  clockgen.enableOutputs(true);
  count_frequency();  // Count f and update the display

//  clockgen.setupPLL(SI5351_PLL_B, 24, 2, 3);
//  Serial.println("Set Output #1 to 13.553115MHz");  
//  clockgen.setupMultisynth(1, SI5351_PLL_B, 45, 1, 2);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("hello, world!");

  pinMode(interruptPin, INPUT);
  pinMode(rotateEncoderPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), rotate_encoder_ISR, FALLING);

  lcd.clear();
//
   pinMode(13, OUTPUT);                    //initalize blink led to show if any tone is detected




}
//
float d_mags[8];
String inString = "";    // string to hold input

void loop() {

  
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  //lcd.setCursor(0, 1);
  // print the number of seconds since reset:
  //lcd.print("                ");
  



  if (changed_f)
  {
    count_frequency();
  clockgen.setupPLL(SI5351_PLL_B, (si5351multi_int),(si5351nomi),(si5351denomi)); // write si5351ctl divider word  
 // clockgen.setupMultisynthInt(0, SI5351_PLL_A, SI5351_MULTISYNTH_DIV_6);
  clockgen.setupMultisynth(1, SI5351_PLL_B,(si5351divider),0,1 );
      changed_f = 0;

      delay(20);
  }

// DTMF decoder
  char thischar;
      /* while(1) */dtmf.sample(sensorPin);
      dtmf.detect(d_mags,512);
      for(int i = 0;i < 8;i++) {
        d_mags[i] /= 100;
      }
      thischar = dtmf.button(d_mags,30.);
      if(thischar) {
        //Serial.print(thischar);
        if(thischar == '#'){
          lcd.setCursor(3,1);
          lcd.print("               ");
          lcd.setCursor(3,1);
          lcd.print(inString);
          Serial.println();
          vfo = inString.toInt();
          Serial.println(vfo);
          inString = "";
          changed_f = 1;
        }
        else if(thischar == '*'){
          Serial.println(inString);
          if(inString == "2") vfo += 10000L;
          if(inString == "4") vfo -= 1000L;
          if(inString == "6") vfo += 1000L;
          if(inString == "8") vfo -= 10000L;
          
          Serial.println(vfo);
          inString = "";
          changed_f = 1;
        }    
        else{
          inString += thischar;
        }
      } // if thischar
}

 unsigned long old_timer = millis();
 int back_count = 1;
 int old_pin_state = 0;
void rotate_encoder_ISR() {
//  noInterrupts();
//  for(int i;i<200;i++) volatile int temp = digitalRead(interruptPin);
//  if(digitalRead(interruptPin) == LOW) {
//  if(millis() - old_timer > 50) {
//    old_timer = millis();
//    int pin_state = digitalRead(rotateEncoderPin);
//    if(pin_state) {
//      if(old_pin_state != pin_state) {
//        old_pin_state = pin_state;
//      }
//      else {
//        vfo+=radix;
//        changed_f = 1;
//      }
//    }else{
//      if(old_pin_state != pin_state) {
//        old_pin_state = pin_state;
//      }
//      else { 
//        vfo-=radix;
//        changed_f = 1;
//      }
//    }
//  while(digitalRead(rotateEncoderPin) & digitalRead(interruptPin));
//  }
//  }
//  interrupts();

 noInterrupts();
    int pin_state = digitalRead(rotateEncoderPin);
    if(pin_state) {
        vfo+=radix;
        changed_f = 1;
    }else{
        vfo-=radix;
        changed_f = 1;
    }
//  while(digitalRead(rotateEncoderPin) & digitalRead(interruptPin));
 for(int i;i<12000;i++) volatile int temp = digitalRead(interruptPin);
 interrupts();


}
