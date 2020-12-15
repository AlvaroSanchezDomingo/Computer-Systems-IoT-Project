/*
  UDPSendReceive.pde:
  This sketch receives UDP message strings, prints them to the serial port
  and sends an "acknowledge" string back to the sender

  A Processing sketch is included at the end of file that can be used to send
  and received messages for testing with a computer.

  created 21 Aug 2010
  by Michael Margolis

  This code is in the public domain.

  adapted from Ethernet library examples
*/


#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "DHT.h"

#ifndef STASSID
#define STASSID "Alvaro-wifi-lp"
#define STAPSK  "12345678"
#endif

// Pin
#define DHTPIN 5

// Use DHT11
#define DHTTYPE DHT11

// the IP address for the shield:
IPAddress ip(192, 168, 137, 3);
IPAddress subnet(255, 255, 255, 0);
IPAddress gateway(192, 168, 137, 1); 
IPAddress dns(192, 168, 137, 1); 

// Create instance
DHT dht(DHTPIN, DHTTYPE, 15);

unsigned int localPort = 8888;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE + 1]; //buffer to hold incoming packet,
float temp = 0;

WiFiUDP Udp;

void setup() {
  Serial.begin(115200);
  WiFi.config(ip, gateway, subnet, dns);
  //WiFi.mode(WIFI_STA);
  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());
  Serial.printf("UDP server on port %d\n", localPort);
  Udp.begin(localPort);

  // Init DHT
  dht.begin();
}

void loop() {
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.printf("Received packet of size %d from %s:%d\n    (to %s:%d, free heap = %d B)\n",
                  packetSize,
                  Udp.remoteIP().toString().c_str(), Udp.remotePort(),
                  Udp.destinationIP().toString().c_str(), Udp.localPort(),
                  ESP.getFreeHeap());

    // read the packet into packetBufffer
    int n = Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    packetBuffer[n] = 0;
    Serial.println("Request from IOT hub:");
    Serial.println(packetBuffer);

    // Reading temperature & humidity
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    int lightLevelRaw = analogRead(A0);
    float l = lightLevelRaw/1024. * 100;

    String aStringObject;
    aStringObject = packetBuffer;

    // Define 
    String str = ""; 
    if (aStringObject == "temperature"){
      str = String(t); 
      
    }else if(aStringObject == "humidity"){
      str = String(h);
    }
    Serial.println("Send to IOT hub : ");
    Serial.println(str);
    // Length (with one extra character for the null terminator)
    int str_len = str.length() + 1; 

    // Prepare the character array (the buffer) 
    char char_array[str_len];

    // Copy it over 
    str.toCharArray(char_array, str_len);
    // send a reply, to the IP address and port that sent us the packet we received
    //char  ReplyBuffer[] = ;       // a string to send back
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(char_array);
    Udp.endPacket();
  }

}

/*
  test (shell/netcat):
  --------------------
	  nc -u 192.168.esp.address 8888
*/
