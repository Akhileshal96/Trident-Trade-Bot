from kite_api import get_kite_instance
import json

kite = get_kite_instance()

instruments = kite.instruments()
with open("instruments.json", "w") as f:
    json.dump(instruments, f)

print("✅ Instruments list saved to instruments.json")
