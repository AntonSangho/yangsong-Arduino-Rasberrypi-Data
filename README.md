# 양송이프로젝트

## 프로젝트 소개 
co2센서와 온습도 데이터 값을 웹 상으로 보여준다. 

## 인수인계
- [아두이노코드](/arduino/) 
- [라즈베리파이 파이썬 코드](/python/) 

## 개발일정 (11월24일 마감) 
1. 프로젝트 인수인계 (11/16)
2. 기존 코드 동작확인 

## 부품
1. 아두이노 우노
2. 라즈베리파이 4 
3. 온습도 센서(DHT22)
4. CO2 센서 (RX-9)

## 설치방법
### 아두이노 우노 
1. 하드웨어 연결하기  
2. 하드웨어 동작확인하기
- [온습도센서](/DHT/DHT.ino) 
- [CO2 센서](/RX-9/RX-9.ino)
3. 라즈베리파이에 USB로 연결하기 
### 라즈베리파이 4
1. 이미지를 준비
2. Raspi-config 설정  
- SSH enable
- GPIO enable 
- Keyboard layout UK -> US
2. 업데이트 하기   
```sudo apt-get update -y && sudo apt-get upgrade```  
3. 프로젝트 다운로드받기 **(microschool 레포지토리로 변경)**  
```git clone https://github.com/AntonSangho/yangsong-Arduino-Rasberrypi-Data.git```
4. Fastapi 설치하기 


## 참고링크

- [아두이노 나노(Arduino Nano)로 EXSEN CO2 Sensor(RX-9) 테스트](https://remnant24c.tistory.com/205)
