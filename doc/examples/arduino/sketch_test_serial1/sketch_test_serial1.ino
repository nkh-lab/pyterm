void setup() {
  // Initialize Serial1 at 9600 baud rate (or your preferred rate)
  Serial1.begin(9600);
}

void loop() {
  // Check if data is available on Serial1
  if (Serial1.available() > 0) {
    // Read the incoming string
    String message = Serial1.readStringUntil('\n');
    // Check if the message is "Hello from Terminal!"
    if (message == "Hello from Terminal!") {
      // Send the reply
      Serial1.println("Hello from Arduino!");
    }
  }
}