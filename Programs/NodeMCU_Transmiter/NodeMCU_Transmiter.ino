

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#ifndef STASSID
#define STASSID "Alvaro-wifi-lp"
#define STAPSK  "12345678"
#endif


// the IP address for the shield:
IPAddress ip(192, 168, 137, 4);
IPAddress subnet(255, 255, 255, 0);
IPAddress gateway(192, 168, 137, 1); 
IPAddress dns(192, 168, 137, 1); 

unsigned int localPort = 8888;      // local port to listen on

// buffers for receiving and sending data
char packetBuffer[UDP_TX_PACKET_MAX_SIZE + 1]; //buffer to hold incoming packet,
float temp = 0;


const int analog_ip = A0; //Naming analog input pin


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

    // Reading light
    int lightLevelRaw = analogRead (analog_ip); // Analog Values 0 to 1023
    float l = lightLevelRaw/1024. * 100;

    // Define 
    String str = String(l);

    Serial.println("Send to IOT hub : ");
    Serial.println(str);
    // Length (with one extra character for the null terminator)
    int str_len = str.length() + 1; 

    // Prepare the character array (the buffer) 
    char char_array[str_len];

    // Copy it over 
    str.toCharArray(char_array, str_len);
    // send a reply, to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(char_array);
    Udp.endPacket();
  }

}
