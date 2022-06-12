#define RED_PIN 5
#define GREEN_PIN 6
#define BLUE_PIN 9

// [mode][beat][color]
//int flash[100][3] = {};
//int rgb[400][3] = {};

int* config = new int[5];
int rgb[2][2] = {{3,4},
                {3,4}};

int beat = 0;

IntervalTimer timer;

void setup()
{
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);
    Serial.begin(9600);

    config[0] = 1;
}


void light()
{
    if (beat == 0)
    {
        digitalWrite(RED_PIN, true);
    }
    else
    {
        digitalWrite(RED_PIN, false);
    }
    beat = (beat + 1) % 1000;
}


void loop()
{

    

    if (Serial.available() > 0){
        noInterrupts();
        timer.begin(light, 1000);
        interrupts();
    }
}