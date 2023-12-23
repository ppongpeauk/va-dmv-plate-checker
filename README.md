# va-dmv-plate-checker
A simple wrapper library to check if a Virginia DMV license plate number is available for purchase. Built using BeautifulSoup, lxml, and requests.

Demo files are included in the repository.

## Installation
```bash
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

## Example Return Values
```json
{"plate": "VPT-740A", "available": True, "reserved" : False, "message": "Congratulations. The message you requested is available."}

{"plate": "VPT-7401", "available": False, "reserved" : False, "message": "Personalized message requested is not available. Please try another message."}

{"plate": "VPT-574", "available": False, "reserved" : True, "message": "If you have reserved this message or it is on a vehicle you own, click Purchase Plate Now; if not, try a new message."}
```