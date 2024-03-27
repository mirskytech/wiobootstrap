from espat import ESPAT

print("\n\ninitializing...\n")

esp8285 = ESPAT()

esp8285.power_on()
esp8285.send_at_command()

print("\ncomplete\n")
