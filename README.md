# Multiplayer Tank Game

These are the basics that you need for a ultiplayer tank game.

## To play with friends across networks
- pip install -r requirements.txt
- deploy the server.py file to your favorite server such as Linode or AWS
- run the server.py
- run the first client on one machine and then another across networks or on the same network
- select remote
- type in the server ip

## To test locally
- pip install -r requirements.txt
- open 3 terminals
- run server.py in the first terminal
- run client.py in the second terminal
- run client.py in the third terminal

Type as prompted by each message selecting player1 in the first terminal then player2 in the second. Type local for local testing. There is little to no input validation so be careful typing!
