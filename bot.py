import discord
import datetime
from utils import *
from dotenv import load_dotenv
import os


load_dotenv()

token = os.getenv("discord_token")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Store user's current todos and start times (in-memory for now)
user_todos = {}




@client.event
async def on_ready():
    print(f"logged in as {client.user.name}#{client.user.discriminator}")
    channel=client.get_channel(1359075240142966917)
    if channel:
        await channel.send("grind guide is ready")
    print("bot is ready")


@client.event
async def on_message(message):
    # Ignores messages sent by the bot itself to prevent looping
    if message.author == client.user:
        return
    #     if message.content.startswith('!todo'):




    # we have recieved a todo command
    if message.guild and message.content.startswith("!todo"):

        # first ,we will take the user message,take the string after "!todo"
        tasks_string = message.content[
            len("!todo") :
        ].strip()  # removes trailing or leading spaces

        # now, we make list of tasks by spliting it
        tasks_list = tasks_string.split("\n")

        # Clean each task by removing leading/trailing dashes and spaces.
        tasks_list = [task.strip("- ").strip() for task in tasks_list if task.strip()]

        # to check the other condition if no todos are enter
        if not tasks_list:
            await message.channel.send(
                "Please list your todos after the !todo command."
            )
            return

        # storing user data
        user_id = message.author.id
        start_time_utc = datetime.datetime.now(datetime.timezone.utc)
        end_time_utc = start_time_utc + datetime.timedelta(hours=24)

        user_todos[user_id] = {
            "tasks": tasks_list,
            "start_time": start_time_utc,
            "end_time": end_time_utc,
            "completed": [False] * len(tasks_list),  # Initialize all as not completed
        }

        # send confirmation in the channel
        await message.channel.send(
            "Your 24-hour academic grind started! Check DMs for details."
        )

        # WORK IN DM
        # message to be dm
        dm_message = f"Your GRIND starts at {start_time_utc.strftime('%H:%M UTC on %d|%m|%Y')}. \n Your provided todos are as follows:\n"

        # providing the todo list
        for i, task in enumerate(tasks_list):
            dm_message += f"{i+1}) {task}\n"
        dm_message += f"\nDEADLINE : {end_time_utc.strftime('%H:%M UTC on %d|%m|%Y')}"

        # dm the user
        try:
            await message.author.send(dm_message)
        except discord.errors.Forbidden:
            await message.channel.send(
                f"{message.author.mention},I couldn't DM you. Please make sure your DMs are open."
            )

    #the to mark the task as done
    elif message.guild is None and message.content.startswith('!done'):
        user_id=message.author.id
        if user_id in user_todos:
            try:
                # abtracting the task number
                task_number=int(message.content[len('!done'):].strip())-1
                #checking if the number
                try:
                    if 0 <= task_number < len(user_todos[user_id]['tasks']):
                        #if the task entered is not completed, it will makr it as completed
                        if not user_todos[user_id]['completed'][task_number]:
                            user_todos[user_id]['completed'][task_number]=True
                            completed_tasks,points=calculate_daily_score(user_todos[user_id]['completed'],user_todos[user_id]['tasks'])
                            total_tasks=len(user_todos[user_id]['tasks'])
                            time_left=user_todos[user_id]['end_time']-datetime.datetime.now(datetime.timezone.utc)

                            time_left_str=f"{time_left.seconds// 3600} hours" if time_left.days==0 else f"{time_left.days} days" if time_left.days>0 else f"{time_left.seconds // 60} minutes"\
                            

                            response=f"Task '{user_todos[user_id]['tasks'][task_number].upper()}' complete succesfully\n"
                            response+=f"PROGRESS: {completed_tasks}/{total_tasks}\n"
                            response+=f"POINTS: {points}\n"
                            response+=f"TIME LEFT: {time_left_str}"

                            # here we will add leaderboard in future,for now lets skip it.
                            # await message.send("do you want to see the leaderboard?[Y/N]")




                            await message.author.send(response)
                        else:
                            await message.author.send(f"The task number {task_number+1} is already completed by you")
                    else:
                        await message.author.send(f"Invalid task number. Please use the number from your todo list.") 
                except discord.errors.Forbidden:
                    await message.channel.send(
                f"{message.author.mention},I couldn't DM you. Please make sure your DMs are open."
            )    
                    
            except:
                await message.author.send("query entered in wrong format")
        else:
              await message.author.send("You haven't started your todo list for today.please start in guild")       

client.run(token)
