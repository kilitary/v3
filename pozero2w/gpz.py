import gpiozero
import rich
import time

# Create an LED object using the onboard LED
led = gpiozero.LED(25)  # The onboard LED is typically on GPIO pin 25

try:
    # Inform the user that the program is running
    rich.print("[bold green]LED blinking program started. Press CTRL+C to exit.[/bold green]")

    # Main loop to blink the LED
    while True:
        led.on()
        time.sleep(0.3)  # LED on for 0.3 seconds
        led.off()
        time.sleep(0.3)  # LED off for 0.3 seconds

except KeyboardInterrupt:
    # Clean exit on CTRL+C
    rich.print("[bold yellow]Program terminateree by user.[/bold yellow]")
    led.off()  # Ensure LED is off when exiting

