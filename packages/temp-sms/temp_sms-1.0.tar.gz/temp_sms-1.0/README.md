# Python Temp SMS
## Requires playwright
```
python -m playwright install
```

### Example:
```python
from temp_sms import PhoneNumber

with PhoneNumber() as number:
    print(number)  # Number: +1 (920) 572-2111, Carrier: Verizon
    print("+" + number.number_country_code + number.number_plain)  # +19205722111
    print(number.messages())  # [("Now", "*****9", "Your Roblox account verification code: 69420"), ('11 min ago', '****0', 'G-405383 is your Google verification code.')]
```
