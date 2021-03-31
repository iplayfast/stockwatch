# stockwatch
watches stocks in the background and alerts you when there are 10 buys or sells in a row, or the stock has reached new highs or lows for the day.
The idea is that you can do other things on your computer while this runs in the background and will say, using text to speech (thanks google), an alert about the situtation.

requires 
yahoo_fin
gtts
python-dateutil
playsound

install requirements with
pip yahoo_fin gtts python-dateutil playsound


Will alert you by saying 
"Alert Tesla is heading up" or "Alert Tesla is heading down" if it detects 10 buys or sells in a row. Usually this is accurate enough to indicate.
or if the stock has reached a new recorded high or low "Alert Tesla has a new maximum price" etc.

Only a few stocks have their names, associted with the symbol, and if there is no name association, the symbol is spelled out. 

To use
python watch.py symbols

for example
python watch.py tsla pltr pypl

