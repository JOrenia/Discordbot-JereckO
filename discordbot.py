#To create a discord bot, importing the discord library is neccesary to create the bot.
#The os library is used to interact with the linux operating system and the environment variables in the ec2 instance.
#The import random is used to generate a random choice or number such as choosing a randoom response later seen in the code.
#To retrieve the metadata from the the Amazon instance, we need to import from ecs_metadata.
#To import the the variables from a separate file named '.env', we load and import using loud_dotenv.
import discord 
import os 
import random 
from ec2_metadata import ec2_metadata 
from dotenv import load_dotenv 


#I created a list containing three sentences and defined it as 'jokes'.
jokes = [
    "Why does python live on land? Bacause its above c level",
    "Look at a mirror",
    "Dana white podcasts",
]

#To load the .env file containing the discord bot token, I use the load_dotenv() function.
#To create the discod bot client, I use dicord.bot() function.
load_dotenv()
client = discord.Bot()
token = str(os.getenv('TOKEN')) #This retrieves the token from the .env file and converts it into a string.

'''
I created a client event that is initiated once the discord bot connects to the discord server.
once the bot connnects, it prints the messages of the bot logging in, the region, instance id, and public ip address.
'''
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))
    print(f'EC2 Region: {ec2_metadata.region}')
    print(f'EC2 Instance ID: {ec2_metadata.instance_id}')
    print(f'Public IP Address: {ec2_metadata.public_ipv4}')


#I created another client even that is initiated once a message is sent into the channel where the bot has access to.
#this also retrieves informations such as username, channel name, and what the message is for in the instance terminal.
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    
    print(f'Message {user_message} by {username} on {channel}')
    #This if statement is used to prevent the bot from responding to itself.
    if message.author == client.user:
        return
    
    '''In this if statement, the bot can only respond to the channels random, bot-rando, and general. 
    The specific channel from the server must be specified for the bot to respond'''
    if channel == "random" or "bot-rando" or "general":
        #The try and else blocks are used as an error handler to give an error message if the bot cannot connect or loses connection from the server.
        try:
            #In the try block there are if, elif, and else statements houseing the prompts and responses.
            if user_message.lower() == "hello" or user_message.lower() == "hi":
                await message.channel.send(f'What up my G {username}')
                return

            elif user_message.lower() == "hello world" or user_message.lower() == "Hello world":
                await message.channel.send(f'Hello {username}')

            elif user_message.lower() == "bye":
                await message.channel.send(f'PEACE OUT {username}')

            elif user_message.lower() == "tell me a joke":
                random_joke = random.choice(jokes)#The response for this prompt appends a randomized joke from the jokes list.
                await message.channel.send(random_joke)

            elif user_message.lower() == "tell me about my server":#If the bot receives this message, it pulls information from the ec2 metadata and responds accordingly.
                await message.channel.send(f'EC2 Region: {ec2_metadata.region}\nEC2 Instance ID: {ec2_metadata.instance_id}\nIP Address: {ec2_metadata.public_ipv4}')
                #To make the response from the bot look more organized, I added a '\n' to start a new line for each section of this response.

            else:
            #This handles any other inputs that do not match the conditions above.
                await message.channel.send(f"Sorry, I dont understand")
        #If the try function fails and cannot connect to the server, the except block becomes true and posts this response.
        except Exception as e:
            await message.channel.send(f"An error has occurred: {e}")
            

client.run(token)#This allows the bot to run and connect to discord using the discord token.