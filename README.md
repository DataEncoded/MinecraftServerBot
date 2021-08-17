# MinecraftServerBot
A bot that was coded in python3 that starts a server on my specific linux system. You can easily change stuff around and get it to work on whatever you need it for. Will be updated in the future for full inclusiveness.

# How do I get this to work with my server? 
Well the bot essentially just starts a start.sh file, so all you have to do is change the line with 
```python
server = subprocess.Popen(['/home/minecraft_server/fabric/start.sh'], stdout=subprocess.PIPE)
```

to whereever your server is. Make sure you also change the role_id at the top to be your role. 

Future version will make it much easier to set up for your specific situation.

Future versions will also have player and chat recognition (hopefully)
