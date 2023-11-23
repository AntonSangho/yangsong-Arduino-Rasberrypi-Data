#include <DHT.h>

// DHT22 센서 설정
#define DHTPIN 2     // DHT22 데이터 핀
#define DHTTYPE DHT22   
DHT dht(DHTPIN, DHTTYPE);

// RX-9 센서 핀 설정
#define EMF_pin A0  // RX-9 E, Analog, A0 of Arduino
#define THER_pin A1 // RX-9 T, Analog, A1 of Arduino

// RX-9 센서 관련 상수 및 변수 선언
const String VER = "RX-9_SAMPLE_CODE_WO_EEP_200312";
#define Base_line 432
const int32_t max_co2 = 6000;
int warm_up_time = 180; 
unsigned long current_time = 0;
unsigned long prev_time = 0;
int set_time = 1;  
#define averaging_count 10 
float m_averaging_data[averaging_count + 1][2] = {0,};
float sum_data[2] = {0,};
float EMF = 0;
float THER = 0;
int averaged_count = 0;
float EMF_data = 0;
float THER_data = 0;
float THER_ini = 0;
unsigned int mcu_resol = 1024;
float mcu_adc = 5;
#define C1 0.00230088
#define C2 0.000224
#define C3 0.00000002113323296
float Resist_0 = 15;
bool status_sensor = 0;
float cal_A = 372.1;        
float cal_B = 63.27;        
float cal_B_offset = 1.0;   
float co2_ppm = 0.0;
float co2_ppm_output = 0.0;
float DEDT = 1.0;           
int ELTI = 0;
int upper_cut = 0;
int under_cut_count = 0;
int under_cut_cnt_value = 300;
float under_cut = 0.99;               // if co2_ppm shows lower than (Base_line * undercut), sensor do re-calculation
bool cal_A_LOCK = 0;

// 추가된 함수 선언
void ppm_cal();
void sensor_reset();
float EMF_max = 0;
float THER_max = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  // RX-9 센서 초기화 코드는 여기에 추가
}

void loop() {
  // DHT22 센서에서 온습도 읽기
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // 오류 검사: NaN (not a number) 값을 반환하는 경우
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // RX-9 센서에서 CO2 농도 읽기 및 처리
  current_time = millis() / 1000;
  if (current_time - prev_time >= set_time) {
    warm_up_chk();
    ppm_cal(); 
    prev_time = current_time;
  } else {
    return;  // CO2 데이터가 준비되지 않았으면 데이터 전송을 건너뜁니다.
  }

  // 모든 센서 데이터를 하나의 문자열로 조합하여 시리얼 포트를 통해 전송
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\tTemperature: ");
  Serial.print(t);
  Serial.print(" *C\tCO2 Concentration: ");
  Serial.print(co2_ppm_output);
  Serial.println(" ppm");

  delay(2000); // 2초 간격으로 데이터 읽기
}


// RX-9 데이터 처리 관련 함수들 (기존 코드에서 필요한 부분을 추출하여 사용)
void warm_up_chk() {
  if (current_time < warm_up_time) {
    status_sensor = 0;
  }
  else if (current_time >= warm_up_time && status_sensor == 0) {
    status_sensor = 1;
    sensor_reset();
  }
}

void ppm_cal() {
  /*
   * to calculate the concentration of CO2
   * 1. collet EMF(from E pin of RX-9) and THER(from T pin of RX-9)
   * 2. moving average to minimize noise
   * 3. calculate equation with EMF and THER
   * 4. limitate co2 value maximum and minimum
   * 5. if sensor shows too low co2 value, update the variant of calculation equation
   */
  EMF = analogRead(EMF_pin);
  EMF = EMF / mcu_resol; // 10 bits, Change the number if your MCU have other resolution
  EMF = EMF * mcu_adc;    // 5V     , Change the number if your MCU have other voltage
  EMF = EMF / 6;    //OPAMP   , Don't change!
  EMF = EMF * 1000; //V to mV conversion
  delay(1);
  THER = analogRead(THER_pin);
  THER = 1 / (C1 + C2 * log((Resist_0 * THER) / (mcu_resol - THER)) + C3 * pow(log((Resist_0 * THER) / (mcu_resol - THER)), 3)) - 273.15;
  delay(1);

  // Moving Average START --->
  m_averaging_data[averaged_count][0] = EMF;
  m_averaging_data[averaged_count][1] = THER;

  if (averaged_count < averaging_count) {
    averaged_count++;
  }
  else if (averaged_count >= averaging_count) {
    for (int i = 0; i < averaging_count; i++) {
      sum_data[0] = sum_data[0] + m_averaging_data[i][0]; //EMF
      sum_data[1] = sum_data[1] + m_averaging_data[i][1]; //THER
      for (int j = 0; j < 2; j++) {
        m_averaging_data[i][j] = m_averaging_data[i + 1][j];
      }
    }
    EMF_data = sum_data[0] / averaging_count;
    THER_data = sum_data[1] / averaging_count;

    sum_data[0] = 0;
    sum_data[1] = 0;
  }
  // <---Moving Average END

  // CO2 Concentratio Calculation START --->
  co2_ppm = pow(10, ((cal_A - (EMF_data + DEDT * (THER_ini - THER_data))) / (cal_B * cal_B_offset)));
  co2_ppm = co2_ppm * 100 / 100;
  // <--- CO2 Concentration Calculation END

  // CO2 ppm min, max regulation START-->
  if (co2_ppm > max_co2) {
    co2_ppm_output = max_co2;
  }
  else if (co2_ppm <= Base_line) {
    co2_ppm_output = Base_line;
  }
  else {
    co2_ppm_output = co2_ppm;
  }
  // <--- CO2 ppm min, max regulation END

  // CO2 ppm baseline update START -->
  if (co2_ppm <= Base_line * under_cut) {
    under_cut_count++;
    if (under_cut_count > under_cut_cnt_value) {
      under_cut_count = 0;
      sensor_reset();
    }
  }
  else {
    under_cut_count = 0;
  }
}

void sensor_reset() {
  /*
   *  센서의 상태가 정상상태인 경우
   *  센서의 출력값을 초기화시킴
   *  센서의 정상상태 판단 (Warm-up이 끝났을 것, DMG_REC()에서 판정하는 기준에 해당하지 않을 것)
   *    
   *  
   */
  if (cal_A_LOCK == 0) {
    THER_ini = THER_data;
    EMF_max = EMF_data;
    THER_max = THER_data;
    ELTI = 0;
    cal_A = EMF_data + log10(Base_line) * (cal_B * cal_B_offset);
  }
}

// RX-9 센서 데이터 처리와 관련된 나머지 함수들
// (기존 코드 참조 및 필요한 부분 추출)

