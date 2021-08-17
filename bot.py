import discord
import subprocess
import re

role_id = 838848407296409600

token_file = open('token.txt', 'r')
token = token_file.read()
token_file.close()


def server_check():
    # Checks if the server is already up
    ps = subprocess.run(['ps', '-a'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    if 'java' in ps:
        return True
    else:
        return False

def get_java_pid():
    ps = subprocess.run(['ps', '-a'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    for line in ps.splitlines():
        if 'java' in line:
            return line.strip().split(' ')[0]



server_up = server_check()
server = None

async def read_output(channel):
    #await channel.send('Server starting!')
    while True:
        if not server:
            break
        
        for line in iter(server.stdout.readline, b''):
            matched = re.search('Done \(d{1,}.\d{1,3}s\)! For help, type "help"', line.decode('utf-8'))
            print(line.decode('utf-8'))
            if matched:
                channel.send('Server started.')
                
            if not server:
                break
        


class discordClient(discord.Client):
    async def send_message(self, channel, message):
        await channel.send(message)

    async def update_activity(self):
        discord_state = 'Unknown'
        
        if server_up:
            discord_state = 'up'
        else:
            discord_state = 'down'
        await self.change_presence(activity=discord.Activity(name='Server is {}!'.format(discord_state), type=0))

    async def on_ready(self):
        print('Ready')
        await self.update_activity()

    async def on_message(self, msg):
        if msg.content.startswith('mc!'):
            if role_id in [role.id for role in msg.author.roles]:
                global server_up
                global server
                command = msg.content[3:].lower()
                if command == 'start':
                    if server_up == True:
                        await msg.channel.send('Could not start server, server is already started/is starting!')
                    else:
                        if server_check():
                            await msg.channel.send('Server is currently attempting to start or shut down, please try again later.')
                        else:
                            server = subprocess.Popen(['/home/minecraft_server/fabric/start.sh'], stdout=subprocess.PIPE)
                            global thread
                            #loop = asyncio.get_event_loop()
                            #thread = await loop.run_in_executor(ThreadPoolExecutor(), read_output(msg.channel))
                            server_up = True
                            await self.update_activity()
                            await msg.channel.send('Sent message to server to start.')
                elif command == 'stop':
                    if server_up == False:
                        await msg.channel.send('Could not stop server, server is offline.')
                    else:
                        if not server_check():
                            await msg.channel.send('Server stopped instantly!')
                            server_up = False
                            await self.update_activity()
                        else:
                            await msg.channel.send('Sending message to server to stop.')
                            subprocess.run(['kill', get_java_pid()])
                            server_up = False
                            await self.update_activity()
                            if server:
                                server.kill()
                                server.wait()
                                server.returncode
                                server = None
                                #Ensure command closes
                
                elif command[0:2] == 'say':
                    server.communicate('<Discord> [{}] {}\n'.format(msg.author.name,command[4:]))

                elif command == 'status':
                    status = None
                    if server_up == True:
                        status = 'up'
                    else:
                        status = 'down'
                         
                    await msg.channel.send('The server is {}!'.format(status))
            else:
                await msg.channel.send('You do not have adequate permissions to use fabric commands.')
                        
client = discordClient()

client.run(token)
