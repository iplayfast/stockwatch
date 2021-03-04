# stockwatch
watches stocks in the background and alerts you when there are 10 buys or sells in a row.

requires 
yahoo_fin
gtts
python-dateutil
playsound

install requirements with
pip yahoo_fin gtts python-dateutil playdound


Will alert you by saying 
"Alert TSLA is heading up" or "Alert TSLA is heading down"
or if the stock has reached a new recorded high or low.

To use
python watch.py symbols

for example
python watch.py tsla pypl

