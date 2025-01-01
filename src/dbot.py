import time
from datetime import datetime, timedelta

# timedelta: https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-28.php
# https://docs.python.org/3/library/datetime.html

import asyncio
from asyncio import sleep
# import threading

import os # Execute a command from python script
import sys 

# connect to wifi by using requests to connect to host / error exception
# https://www.codespeedy.com/how-to-check-the-internet-connection-in-python/
import requests
wifiWaitCount = 0

# connectWifi(host) - returns boolean for wifi connection
# reason: sometimes, import discord errors due to wifi connection not established yet
def connectWifi(host='http://google.com'):
    try:
        print(f'Request from Discord.com: {requests.get(host)}')
        webGot = requests.get(host)
        return True
    except:
        return False

while connectWifi() == False:
    wifiWaitCount+=1
    print(f'Waiting for Wifi... wifiCount: {wifiWaitCount}')
    time.sleep(1)


import discord
from discord.utils import get

import random
import json

from pathlib import Path #https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

#import sys, json, numpy as np
# communication from node.js to python | https://www.sohamkamani.com/blog/2015/08/21/python-nodejs-comm/
#import axios # https://www.youtube.com/watch?v=fQqkaQSc8dI


# from bs4 import BeautifulSoup # https://www.youtube.com/watch?v=4UcqECQe5Kc

import re
from discord.ext import commands, tasks

# multi threading video
# https://www.youtube.com/watch?v=IEEhzQoKtQU

import threading
#import concurrent.futures
# with concurrent.futures.ThreadPoolExecutor() as executor:
#   executor.submit( func_name, args=[] )



# prefixes.json acts as a dictionary, including every server / prefix
path_dbot = "/home/pi/discordbot"
prefixes_file = path_dbot + "/json_storage/prefixes.json"
guild_settings_file = path_dbot + "/json_storage/guild_settings.json"
work_reminder_file = path_dbot + "/json_storage/work_reminder.json"
work_stats_file = path_dbot + "/json_storage/work_stats.json"
egg_dict_file = path_dbot + "/json_storage/egg_dict.json"
frame_info_file = path_dbot + "/json_storage/frame_info.json"
bits_file = path_dbot + "/json_storage/bits.json"

# koibito json files
_question_storage_file = path_dbot + "/char_questions/base_files/_question_storage.json"
_similar_questions_file = path_dbot + "/char_questions/base_files/_similar_questions.json"
koibito_aliases_file = path_dbot + "/char_questions/base_files/koibito_aliases.json"

_template_char_file = path_dbot + "/char_questions/_template_char.json"


max_dice_roll = 20


# https://stackoverflow.com/questions/1724693/find-a-file-in-python
def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
        else:
            return None

def get_prefix(client, message):
    # opening json file, read mode
    with open(prefixes_file, 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def get_guild_prefix(ctx):
    with open(prefixes_file, 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(ctx.guild.id)]

client = commands.Bot(command_prefix=get_prefix)

# ==============================================================================
all_commands = {
    '# general' : {
        'simp': '',
        'ping': '',
        '8ball': '<question>',
        'e': '<emote>',
        'emotes': '',
        'link (l)': '<acronym>',
        'linkadd (la)': '<acronym> <link>',
        'linkremove (lr)': '<acronym',
        'links (ls)': '',
    },
    '# admin' : {
        'parse': '<hexcode>',
        'clear': '<number>',
        'bind': '<command>',
        'unbind': '<command>',
        'status': '<string>',
        'kick': '@user <reason>',
        'ban': '@user <reason>',
        'unban': '<user>',
        'custom': '',
    },
    '# commander_in_chief' : {
        'changeprefix': '<prefix>',
        'shutdown': '<countdown = None>',
        'reboot': '',
    }
}


authority_whitelist = [
    '<rank: authority>',
    731644582164430870, #mai sakurajima bot
    263853089419821056, #puf
    235088799074484224  #rhythm bot
    ]

admin_whitelist = [
    '<rank: admin>',
    731644582164430870, # bot
    263853089419821056, # puf
    476844367613526036, # boof
    239858810439729162, # ritsuno6
    424042277577424897, # beehive
    253390316260818944, # xiushak
    516411039575965697, # tim
    291408560661725186, #mausu
]

commander_in_chief = [
    '<rank: commander_in_chief>',
    263853089419821056 # puf
]

async def isWhitelisted(ctx, array, perm='do thing', can_send_fail=True):
    if ctx.author.id in array:
        return True
    if can_send_fail == True:
        await ctx.send(f':no_entry: Only a `{array[0]}` can {perm}.', delete_after = 3)
        await asyncio.sleep(3)
        await ctx.message.delete()
    return False

# shutdown bot from discord
# shutdownActive = False
maxShutdown = 300;
bot_shutdown_message = ":white_check_mark: Goodnight~ :heart: \n`[ Shutting Down Raspberry Pi ]`"

@client.command(aliases=['sd'])
async def shutdown(ctx, countdown=None):
    if await isWhitelisted(ctx, commander_in_chief, "Shutdown the Raspberry Pi 4"):
        #if shutdownActive == False:
        #    shutdownActive = True
            if countdown == None or countdown < 5:
                shutdown_msg = await ctx.send(bot_shutdown_message)
                time.sleep(1)
                # await shutdown_msg.delete()
                os.system('sudo shutdown -h now')
            elif countdown <= maxShutdown:
                countdown_msg = await ctx.send(f':white_check_mark: Shutting down in {countdown} seconds...')
                while countdown > 1:
                    countdown -= 1
                    time.sleep(1)
                    await countdown_msg.edit(content=f':white_check_mark: Shutting down in {countdown} seconds...')
                await countdown_msg.delete()
                shutdown_msg = await ctx.send(bot_shutdown_message)
                time.sleep(3)
                await shutdown_msg.delete()
                os.system('sudo shutdown -h now')
            else:
                await ctx.send(f':no_entry: Shutdowns can only be {maxShutdown} seconds or less.')
        #else:
        #    await ctx.send(':no_entry: A Shutdown is already active.', delete_after = 1)
            await ctx.message.delete()
        

# reboot bot from discord
@client.command(aliases=['restart'])
async def reboot(ctx):
    if await isWhitelisted(ctx, commander_in_chief, "Reboot the Raspberry Pi 4"):
        reboot_msg = await ctx.send(":white_check_mark: I'll be back :wink: \n`[ Rebooting Raspberry Pi ]`")
        await asyncio.sleep(1)
        os.system('sudo reboot -h now')


# support functions
def canKickOrBan(user):
    for unbannable_user_id in authority_whitelist:
        if unbannable_user_id == user.id:
            return False
    return True

# check if using command in correct channel
# json file: checking if element exists  |  command in the_guild or
async def isCorrectChannel(ctx, command):
    with open(guild_settings_file, 'r') as f:
        guild_settings = json.load(f)
    the_guild = guild_settings[str(ctx.guild.id)]
    if command in the_guild and not the_guild[command] == ctx.channel.name:
        await ctx.send(f':no_entry: Incorrect channel for command `<{command}>`.', delete_after = 3)
        # how to delete a message using asyncio
        await asyncio.sleep(3)
        await ctx.message.delete()
        return False
    else:
        return True

def createGuildSetting(guild):
    with open(guild_settings_file, 'r') as f:
        guild_settings = json.load(f)

    guild_settings[str(guild.id)] = {}

    with open(guild_settings_file, 'w') as f:
        json.dump(guild_settings, f, indent=4)

def removeGuildSetting(guild):
    with open(guild_settings_file, 'r') as f:
        guild_settings = json.load(f)

    guild_settings.pop(str(guild.id), None)

    with open(guild_settings_file, 'w') as f:
        json.dump(guild_settings, f, indent=4)
# ==============================================================================

@client.command()
async def pfp(ctx, *, member=None):
    if member != None:
        # get a user from a mention
        target_user_id = int(member[3:len(member)-1])
        await ctx.send(client.get_user(target_user_id).avatar_url)
    else:
        await ctx.send(ctx.author.avatar_url)


# ==============================================================================

#@client.event
#async def on_disconnect(ctx):
#    await ctx.voice_client.disconnect()

@client.command()
async def status(ctx, *, member):
    if await isWhitelisted(ctx, admin_whitelist, perm = 'can set the status'):
        ctx.message.delete(delete_after = 1)
        await client.change_presence(activity=discord.Game(member))
        await ctx.send(f':white_check_mark: Status has been changed.')

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


# ==============================================================================

@client.event
async def on_guild_join(guild):
    with open(prefixes_file, 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.' # default

    with open(prefixes_file, 'w') as f:
        json.dump(prefixes, f, indent=4)

    createGuildSetting(guild)

@client.event
async def on_guild_remove(guild):
    # prefixes variable is a local copy of the .json file.
    # .json file edited, then dumped back
    with open(prefixes_file, 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open(prefixes_file, 'w') as f:
        json.dump(prefixes, f, indent=4)

    removeGuildSetting(guild)

@client.command()
async def changeprefix(ctx, prefix):
    if await isWhitelisted(ctx, commander_in_chief, perm = 'change the prefix'):
        with open(prefixes_file, 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix # default

        with open(prefixes_file, 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f':white_check_mark: Prefix changed to {prefix}')

 # ==============================================================================

@client.event
async def on_member_join(member):
    print(f'Welcome {member} to the Bunny Boi Senpai discord.')

@client.event
async def on_member_remove(member):
    print(f'Farewell {member}.')

# ==============================================================================

@client.command(aliases=['commands', 'cmds'])
async def send_commands(ctx):
    the_string = "```ini\n[ Bunny Boi Senpai Bot Commands ]\n"
    for rank in all_commands:
        the_string = the_string + f"{rank}\n"

        for cmd in all_commands[rank]:
            the_string = the_string + f"{get_guild_prefix(ctx)}{cmd} {all_commands[rank][cmd]}\n"
        the_string = the_string + "\n"
    the_string = the_string + "```"
    await ctx.send(the_string)

# simp()
# One of the very first commands I made, using it to test if bot is online 
@client.command()
async def simp(ctx):
    if await isCorrectChannel(ctx, 'simp'):
        await ctx.send(f'You a simp lmao :flushed:')

# ping() : returns None
# Shows the ping of the 
@client.command()
async def ping(ctx):
    if await isCorrectChannel(ctx, 'ping'):
        await ctx.send(f'`Bot\'s Ping`: {round(client.latency * 1000)} ms')

@client.command(aliases=['8ball', '8b'])
async def _8ball(ctx, *, question):
    responses = ['Yes.',
                'Guaranteed.',
                'Quite possibly.',
                'But of course.',
                'Fifty fifty.',
                'Possibly.',
                'Nope.',
                'Not a chance.',
                'Highly unlikely.',
                'Don\'t count on it.'
                ]
    await ctx.send(f':8ball:`{question}`\n{random.choice(responses)}')

emote_array = {
        'fbi': '<:fbi:712525009804853448>',
        'sadge': '<:sadge:732844175518859305>',
        'pepega': '<:pepega:733428444184182785>',
        'monkaS': '<:monkaS:733885688575164477>',
        'monkaW': '<:monkaW:733886218454171768>',
        'wc': '<:WeirdChamp:733397069800407051>',
        'omegalul': '<:omegalul:739562133725118563>',
        'shut': '<:shut:712522824073478196>',
        'mooseball': '<:mooseball:733836035250716763>',
        'bwide': '<:brandonWideHead:715049362732089364>',
        'lappdumb': '<:lappdumb:733484533223260231>',
        'skadi': '<:skadi:734140756033273938>'
}

# When .emotes is called, send emote_array_string
emote_array_string = '`<Emote List>`\n'
for emote in emote_array:
    emote_array_string = emote_array_string + f'{emote_array[emote]} {emote}\n'


@client.command()
async def e(ctx, member, *, message = ''):
    await ctx.message.delete()
    await ctx.send(f'{emote_array[member]} {message}')


@client.command()
async def emotes(ctx):
    if await isCorrectChannel(ctx, 'emotes'):
        await ctx.send(emote_array_string, delete_after = 20)


links_array = {
    'all' : {
        'ratwash': 'https://cdn.discordapp.com/attachments/582429031396278288/596516599205330949/ratwash.mp4',
        'ratslap': 'https://cdn.discordapp.com/attachments/716544471860510761/732542209420820580/video0.mov',
    },
    '731949622058025060' : {
        'byss' : 'https://www.roblox.com/games/33901142/Build-Your-Spaceship-and-Explore-the-Universe',
        'jojo' : 'https://www.roblox.com/games/2686500207/A-Bizarre-Day?refPageId=4becfdb7-c8f2-4be6-bb82-9c0c4b8a16a5',
        'dm' : 'https://www.roblox.com/games/4714814530/Deathmatch-Game?refPageId=d2b615f2-1aac-4d72-8331-ee1a69305b3b',
        'jura' : 'https://www.roblox.com/users/213658150/profile',
    },
    '711276355488055337' : {
        
    },
    '810628552529018930' : {
        
    }
}

# Fill links string
links_string = '```ini\n[ Links ]\n#general\n'
for _link in links_array['all']:
    links_string = links_string + _link + ' | '


@client.command(aliases=['l'])
async def link(ctx, member):
    await ctx.message.delete()
    if member in links_array['all']:
        await ctx.send(links_array['all'][member])
    elif member in links_array[str(ctx.guild.id)]:
        await ctx.send(links_array[str(ctx.guild.id)][member])
    else:
        await ctx.send(':no_entry: No link found.', delete_after=5)

@client.command(aliases=['la'])
async def linkadd(ctx, param, your_link):
    if not f'{param}' in links_array[str(ctx.guild.id)]:
        links_array[str(ctx.guild.id)].update({f'{param}': f'{your_link}'})
        await ctx.send(f':white_check_mark: Link acronym `{param}` has been added.')
    else:
        await ctx.send(f':no_entry: Link acronym `{param}` already exists!', delete_after=5)

@client.command(aliases=['le'])
async def linkedit(ctx, param, your_link):
    if f'{param}' in links_array[str(ctx.guild.id)]:
        links_array[str(ctx.guild.id)].update({f'{param}': f'{your_link}'})
        await ctx.send(f':white_check_mark: Link acronym `{param}` has been edited.')
    else:
        await ctx.send(f':no_entry: Link acronym `{param}` does not exist!', delete_after=5)
        
@client.command(aliases=['lr'])
async def linkremove(ctx, param):
    if f'{param}' in links_array[str(ctx.guild.id)]:
        links_array[str(ctx.guild.id)].pop(f'{param}')
        await ctx.send(f':white_check_mark: Link acronym `{param}` has been removed.')
    else:
        await ctx.send(f':no_entry: Link acronym `{param}` does not exist.', delete_after=5)

@client.command(aliases=['ls'])
async def links(ctx):
    print('> LINKS COMMAND CALLED')
    guild_id = str(ctx.guild.id)
    if guild_id in links_array:
        links_string_local = links_string + f'\n\n#guild\n'
        for link in links_array[guild_id]:
            links_string_local += f'{link} | '

        links_string_local += '```'
        await ctx.send(links_string_local)

# sending a file | image
#@client.command()
#async def pfp(ctx):
    #await ctx.channel.send('Worship our God, Sakurajima Mai', {files: ["./images/mai_pfp.png"]});
#    await ctx.channel.send(file=File("./images/mai_pfp.png"))
#    print('pfp: stage 2')

# ==============================================================================

@client.command(aliases=['c'])
async def clear(ctx, arg1=1):
    if await isWhitelisted(ctx, admin_whitelist, perm = 'clear messages'):
        await ctx.message.delete()
        await ctx.channel.purge(limit=arg1)


custom_whitelist = [
    #476844367613526036, # boof
    263853089419821056, # puf
    424042277577424897 # beehive
]

@client.command()
async def custom(ctx):
    if await isWhitelisted(ctx, custom_whitelist, can_send_fail = False):
        message = f'''`Custom command for people who\'s names start with K.`\nWelcome aboard, {ctx.author.name}.'''
        await ctx.send(message)
    else:
        await ctx.send(f':raised_hand: :pensive: Your name does not start with K, ' + ctx.author.name)



#@client.command()
#async def initiate(ctx):
#    with open(guild_settings_file, 'r') as f:
#        guild_settings = json.load(f)

#    guild_settings[str(ctx.guild.id)] = {}

#    with open(guild_settings_file, 'w') as f:
#        json.dump(guild_settings, f, indent=4)

def set_command_to_channel(ctx, command):
    with open(guild_settings_file, 'r') as f:
        guild_settings = json.load(f)
    guild_settings[str(ctx.guild.id)][command] = ctx.channel.name

    with open(guild_settings_file, 'w') as f:
        json.dump(guild_settings, f, indent=4)


unbindable_commands = [
    'link',
    'links',
    'bind',
    'unbind',
]

async def canBind(ctx, command):
    if command in unbindable_commands:
        await ctx.send(f':no_entry: Cannot bind command `<{command}>`.', delete_after = 3)
        await asyncio.sleep(3)
        await ctx.message.delete()
        return False
    return True

@client.command()
async def bind(ctx, command):
    if await isWhitelisted(ctx, admin_whitelist, perm = 'set a command\'s specified channel'):
        if await canBind(ctx, command) == True:
            for rank in all_commands:
              if command in all_commands[rank]:
                    set_command_to_channel(ctx, command)
                    await ctx.send(f':white_check_mark: Set command `<{command}>` to channel {ctx.channel.mention}')
                    return


def unbind_command(ctx, command):
    with open(guild_settings_file, 'r') as f:
        guild_settings = json.load(f)

    if guild_settings[str(ctx.guild.id)][command] != None:
        previous_channel = guild_settings[str(ctx.guild.id)][command]
        guild_settings[str(ctx.guild.id)].pop(command, None)

        with open(guild_settings_file, 'w') as f:
            json.dump(guild_settings, f, indent=4)

        return previous_channel


@client.command()
async def unbind(ctx, *, command):
    if await isWhitelisted(ctx, admin_whitelist, perm = 'unbind a command from a specified channel'):
        previous_channel = unbind_command(ctx, command)
        await ctx.send(f':white_check_mark: Unbinded command `<{command}>` from channel `<{previous_channel}>`.')

# ==============================================================================

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    if await isWhitelisted(ctx, admin_whitelist, perm = 'kick others'):
        if canKickOrBan(member) == True:
            await ctx.send(f':white_check_mark: Kicked {member.mention}.')
            await member.kick(reason=reason)
        else:
            await ctx.send(f':no_entry: Cannot kick a person of `{authority_whitelist[0]}`.')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    if await isWhitelisted(ctx, admin_whitelist, perm = 'ban others'):
        if canKickOrBan(member) == True:
    #    if True:
            await ctx.send(f':white_check_mark: Banned {member.mention}.')
            await member.ban(reason=reason)
        else:
            await ctx.send(f':no_entry: Cannot ban a person of `{authority_whitelist[0]}`.')

# member is no longer in the server, cannot mention
# use *
# allows for all following instances to be taken into the single parameter 'member'

@client.command()
async def unban(ctx, *, member):
    if await isWhitelisted(ctx, admin_whitelist, perm = 'unban others'):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f':white_check_mark: Unbanned {user.mention}.')
                return None


# ==============================================================================
# Allocated section for sauce commands <REDACTED>


# ==============================================================================
# Karuta Work Reminder section


# Embed for help command
work_help = {
    'color' : 10181046,
    'author':{
        'name': 'Work Reminder',
        'icon_url': 'https://cdn.discordapp.com/avatars/731644582164430870/3fd13088a206c2b3451d699f61cf2fab.webp?size=1024'
        },
    'footer': {
        'text': ''
        },
    'fields': [
    
    # normal commands
    {
        'name': '`show`',
        'value': 'Shows your current reminders are.'
        },
    {
        'name': '`add <card> <number_of_days>`',
        'value': 'Adds a reminder for your card.'
        },
    {
        'name': '`remove <card>`',
        'value': 'Removes the desired card from your dictionary.'
        },
    
    # admin commands
    {
        'name': ':lock:`setchannel`',
        'value': 'Sets the current channel to send work reminders.'
        },
    {
        'name': ':lock:`remove profile <user_id>`',
        'value': 'Removes a user from the guild\'s dictionary.'
        },
    {
        'name': ':lock:`inititate`',
        'value': 'Initiates the guild for Karuta Work Reminders.'
        }
    ]
}



# Embed for work profiles, sent when .work show
async def create_profile_embed(ctx, profile):
    check_arr = {
        'color': 12370112,
        'author': {
            'name': f'{ctx.author.name}\'s Work Dictionary',
            'icon_url': f'{ctx.author.avatar_url}'
            },
        'footer': {
            'text': ''
            },
        'fields':[
            ]
        }
    
    for i in range(0, len(profile)):
        card = profile[i]['card']
        days = profile[i]['days']
        recovery_date = profile[i]['recovery_date']
        rd_hour = int(recovery_date[3])
        rd_min = int(recovery_date[4])
        ampm = "am"
        # convert 24 hour to 12:12 hour, am/pm
        if rd_hour/12 >= 1:
            ampm = "pm"
            if rd_hour > 12:
                rd_hour -= 12;
        elif rd_hour == 0:
            rd_hour = 12
            
        # convert 12:12 hour to 01-09, 11-12 hour
        if rd_hour < 10:
            rd_hour = f'0{rd_hour}'
        # convert single-digit minutes to 01-09
        if rd_min < 10:
            rd_min = f'0{rd_min}'
            
        card_arr = {'name': f'`{card}` : {days} Days, {rd_hour}:{rd_min} {ampm}', 'value': '_ _'}            
        check_arr['fields'].insert(i, card_arr)
    
    return check_arr


# uses {work_reminder_file}
# check a guild to see if it has been initialized
def check_work_init(wr, gid):
    return gid in wr

def open_json(target_json):
    with open(target_json, 'r') as f:
        content = json.load(f)
    f.close()
    return content
    
def write_json(content, target_json):
    with open(target_json, 'w') as f:
        json.dump(content, f, indent=4)
    f.close()

# append = add to array

async def check_work_profile(ctx, wr, uid, gid):
    if not uid in wr[gid]:
        wr[gid][uid] = []
        write_json(wr, work_reminder_file)
        ws_dict = open_json(work_stats_file)
        ws_dict[gid][uid] = {
            "no_injury_streak": 0
            }
        write_json(ws_dict, work_stats_file)
        await ctx.channel.send(f':white_check_mark: {ctx.author.mention} Your profile has been added to this guild\'s Work Reminder dictionary.')
        

def collect_work_arg(arg):
    name = ""
    days = None
    if len(arg) > 2:
        for i in range(1, len(arg)):
            if not arg[i].isdigit():
                name += arg[i] + " "
            elif arg[i].isdigit():
                days = arg[i]
                break
        name = name.strip(" ")
        return name, days
    else:
        return None, days

# Argument parser for .work remove <card>
# Turns array of arguments into one string 
def collect_work_remove_arg(arg):
    target_card = ""
    for i in range(1, len(arg)):
        target_card += arg[i] + " "
    target_card = target_card.strip(" ")
    return target_card

# work update command, used for when i implemented hour/minute accuracy

# @client.command()
# async def wu(ctx):
#     wr = open_json(work_reminder_file)
#     gid = str(ctx.guild.id)
#     print(wr[gid])
#     for uid, profile in wr[gid].items():
#         if uid != "last_updated" and uid != "setchannel":
#             for i in range(len(profile)):
#                 crd = profile[i]['recovery_date']
#                 profile[i]['recovery_date'] = [crd[0], crd[1], crd[2], 20, 0]
#                 print(profile[i]['card'], " | recovery: ", profile[i]['recovery_date'])
#                 
#     await ctx.send(f":white_check_mark: {ctx.author.mention} Sent the details to console, UPDATING NOW:.")
#     write_json(wr, work_reminder_file)
#     write_json[wr, work_reminder_file]

@client.command(aliases=['w'])
async def work(ctx, *, arg=""):
    arg = arg.split(" ")
    #global work_reminder_file
    init_bool = None
    gid = str(ctx.guild.id)
    wr = open_json(work_reminder_file)
    init_bool = check_work_init(wr, gid)
    
    uid = str(ctx.author.id)
    # init_bool, check if guild has been initialized already
    if init_bool == True:
        # if profile doesn't exist, add user profile into the work dictionary
        await check_work_profile(ctx, wr, uid, gid)
        
        if arg[0] == 'show' or arg[0] == 's':
            # check if len(arg) >= 2 because arg = {'show', multiple_parameters, *}
            # CHECKING FOR UID's DICTIONARY
            if len(arg) >= 2 and arg[1].isdigit():
                
                if str(arg[1]) in wr[gid]:
                    profile = wr[gid][str(arg[1])]
                    ws_dict = open_json(work_stats_file)
                    
                    #await ctx.send(f':no_entry: {ctx.author.mention} You have no cards in your dictionary.')
                    await ctx.send(f":white_check_mark: {ctx.author.mention} Profile for uid `{arg[1]}`: \n```{profile}```\nProfile in work stats: `{arg[1] in ws_dict[gid]}`")
                else:
                    #await ctx.send(f':no_entry: {ctx.author.mention} You have no cards in your dictionary.')
                    await ctx.send(f':no_entry: {ctx.author.mention} User id `{arg[1]}` not found in Work Reminder dictionary.')
            # CHECKING OWN DICTIONARY
            else:
                profile = wr[gid][uid]
                if len(profile) > 0:
                    check_embed = discord.Embed.from_dict(await create_profile_embed(ctx, profile))
                    await ctx.send(embed=check_embed)
                else:
                    await ctx.send(f':no_entry: {ctx.author.mention} You have no cards in your dictionary.')
        elif arg[0] == 'add' or arg[0] == 'a':
            # check if remind args are valid
            arg2, arg3 = collect_work_arg(arg)
            if arg2 != None and arg3 != None and arg3.isdigit():
                new_card_days = int(arg3)
                #datetime.now() SWITCH
                rd = datetime.now() + timedelta(new_card_days)
                new_card_array = {
                    'card': f'{arg2}',
                    'days': new_card_days,
                    'recovery_date': [rd.year, rd.month, rd.day, rd.hour, rd.minute]
                    }
                if new_card_days >= 1 and new_card_days <= 30:
                    profile = wr[gid][uid]
                    if len(profile) > 0:
                        for i in range(0, len(profile)):
                            if profile[i]['days'] >= new_card_days:
                                profile.insert(i, new_card_array)
                                break
                            elif i == len(profile)-1:
                                profile.insert(len(profile), new_card_array)
                                break
                    else:
                        profile.append(new_card_array)
                    write_json(wr, work_reminder_file)
                    await ctx.send(f':white_check_mark: {ctx.author.mention} Added card `{arg2}` to Work Dictionary. \nThis card will recover after `{arg3}` days on `{rd}`.')
                else:
                    await ctx.send(f':no_entry: {ctx.author.mention} Invalid integer for `<number_of_days>`.', delete_after=5)
            # check failed, invalid arguments
            else:
                await ctx.send(f':no_entry: {ctx.author.mention} Your `<card>` or `<number_of_days>` cannot be invalid.', delete_after=5)
                time.sleep(5)
                await ctx.message.delete()
        
        elif arg[0] == 'help' or arg[0] == 'h':
            work_embed = discord.Embed.from_dict(work_help)
            await ctx.send(embed=work_embed)
        elif arg[0] == "" or arg[0] == None:
            await ctx.send(f':tools: {ctx.author.mention} Welcome to the **Work Reminder** command. Please type `.work help` for more information.')  
        
        
        elif arg[0] == 'setchannel' or arg[0] == 'sc':
            if await isWhitelisted(ctx, commander_in_chief, "set the channel for Karuta Work Reminders."):
                wr[gid]['setchannel'] = ctx.channel.id
                write_json(wr, work_reminder_file)
                await ctx.send(f':white_check_mark: {ctx.author.mention} Set the channel to {ctx.channel.mention}')
        
        
        elif arg[0] == 'remove' or arg[0] == 'r' and len(arg) > 1:
            if arg[1] == 'profile' or arg[1] == 'p' and await isWhitelisted(ctx, commander_in_chief, "clear a profile from the Work Dictionary."):
                
                # remove all profiles
                if arg[2] == 'all':
                    # on reaction here
                    msg = await ctx.send(f":arrow_forward: {ctx.author.mention} Removing all profiles from `Work Dictionary`...")
                    to_pop = []
                    for uid, profile in wr[gid].items():
                        # last_updated / setchannel are both elements inside work dictionary
                        if uid != 'last_updated' and uid != 'setchannel':
                            to_pop.append(uid)
                    for uid in to_pop:
                        wr[gid].pop(uid)
                        
                    write_json(wr, work_reminder_file)
                    time.sleep(1)
                    if len(to_pop) > 0:
                        await msg.edit(content=f":white_check_mark: {ctx.author.mention} All profiles have been removed from `Work Dictionary`.")
                    else:
                        await msg.edit(content=f":no_entry: {ctx.author.mention} No profiles in `Work Dictionary` to remove.")
                # remove a specific profile
                else:
                    if arg[2] in wr[gid]:
                        wr[gid].pop(arg[2], None)
                        write_json(wr, work_reminder_file)
                        
                        await ctx.send(f':white_check_mark: {ctx.author.mention} Successfully removed user profile `{arg[2]}` from Work Dictionary.')
                    else:
                        await ctx.send(f':no_entry: {ctx.author.mention} Failed to find user profile `{arg[2]}`', delete_after=5)
                        time.sleep(5)
                        await ctx.message.delete()
            
            # clearing a card from dictionary
            elif arg[1] != None:
                target_card = collect_work_remove_arg(arg)
                target_card = target_card.lower()
                profile = wr[gid][uid]
                
                for i in range(0, len(profile)):
                    the_card = profile[i]['card'].lower()
                    if the_card == target_card or the_card.find(target_card) != -1:
                        the_card = profile[i]['card']
                        profile.pop(i)
                        write_json(wr, work_reminder_file)
                        await ctx.send(f":white_check_mark: {ctx.author.mention} Successfully cleared `{the_card}` from Work Dictionary.")
                        return
                await ctx.message.delete()
                await ctx.send(f':no_entry: {ctx.author.mention} Did not find card `{target_card}` in your Work Dictionary.', delete_after=5)
            else:
                await ctx.message.delete()
                await ctx.send(f':no_entry: {ctx.author.mention} Invalid usage of command `<clear>`.', delete_after=5)
    elif arg[0] == 'initiate' or arg[0] == 'i':
        if await isWhitelisted(ctx, commander_in_chief, "initiate a guild for Karuta Work Reminder.") and not gid in wr:
            wr[gid] = {}
            wr[gid]['setchannel'] = str(ctx.channel.id)
            write_json(wr, work_reminder_file)
            
            ws_file = open_json(work_stats_file)
            ws_file[gid] = {}
            write_json(ws_file, work_stats_file)
            
            await ctx.send(':white_check_mark: Initiated this guild for `Karuta Work Reminder`.')
            await ctx.send(f':white_check_mark: Set the channel to {ctx.channel.mention}')
        else:
            await ctx.send(f':no_entry: {ctx.author.mention} This guild is already initialized!')
    else:
        await ctx.message.delete()
        await ctx.send(f':no_entry: {ctx.author.id} You must initiate this guild for work first.', delete_after=5)
        time.sleep(3)
        await ctx.message.delete()

frame_help = {
    'color' : 7419530,
    'author':{
        'name': 'Frame Command Help',
        'icon_url': 'https://media.discordapp.net/attachments/812909278507302964/837824721416355890/31e97cadbf129a612acc8498fd9b4e8e.png'
        },
    'footer': {
        'text': ''
        },
    'fields': [
    # normal commands
    {
        'name': '`.frame <bit>`',
        'value': 'Shows what frames use a bit.'
        },
    {
        'name': '`.frame print`',
        'value': 'Prints all the frames'
        },
    {
        'name': ':lock:`.frameadd <frame> <bit1> <bit2> <index>`',
        'value': 'Adds a frame to the frame info list.'
        },
    {
        'name': ':lock:`.frameremove <frame>`',
        'value': 'Removes a frame from the frame info list.'
        },
    {
        'name': ':lock:`.nodeadd <bit1>',
        'value': 'Add a bit to the list of bits used in bit-frames.'}
    ]
}


@client.command(aliases=['f'])
async def frame(ctx, *, args=""):
    args = args.split(" ")
    for i in range(0, len(args)):
        args[i] = args[i].lower()
    
    bfile = open_json(bits_file)
    # if the argument is a valid bit, checkingBit = target bit, instead of boolean
    checkingBit = False
    if len(args[0]) > 0:
        for bit in bfile['bits']:
            if bit.find(args[0]) != -1:
                checkingBit = bit
    
    if checkingBit != False:
        frame_info = open_json(frame_info_file)
        target_frames = {}
        frame_array = frame_info['frames']
        
        # gather all frames with the bit
        for i in range(0, len(frame_array)):
            if checkingBit in frame_array[i]['bits']:
                target_frames[frame_array[i]['frame']] = frame_array[i]['bits']
        
        all_frames_string = ""
        for fname in target_frames:
            tframe_bits = target_frames[fname]
            bit_string = ""
            if tframe_bits[0] == checkingBit:
                bit_string += f'{checkingBit:7} {tframe_bits[1]:7}'.format()
            else:
                bit_string += f'{checkingBit:7} {tframe_bits[0]:7}'.format()
                
            all_frames_string += f"> `{fname:16}`\t{bit_string}\n".format()
        
        await ctx.send(f":white_check_mark: {ctx.author.mention} Frames that use the `{checkingBit}` bit:\n{all_frames_string}")
        
    elif args[0] == "" or args[0] == "help" or args[0] == None:
        help_embed = discord.Embed.from_dict(frame_help)
        await ctx.send(embed=help_embed)
    elif args[0] == "print":
        frame_info = open_json(frame_info_file)
        frame_print = "```ini\n"
        for i in range(0, len(frame_info['frames'])):
            the_frame = frame_info['frames'][i]
            frame_print += f"{i+2:2} [{the_frame['frame']:16}] : {the_frame['bits'][0]:7} {the_frame['bits'][1]:7}\n".format()
        frame_print += "```"
        await ctx.send(f"{ctx.author.mention}\n{frame_print}")
    else:
        await ctx.send(f":no_entry: {ctx.author.mention} Invalid use of `.frame` command. See `.frame help` for more information.")

def collect_args_frameadd(args):
    fname = ""
    bits = [None, None]
    index = None
    if len(args) >= 3:
        for i in range(0, len(args)):
            if args[i].isdigit():
                if i > 2:
                    index = args[i]
                    bits[0] = args[i - 2]
                    bits[1] = args[i - 1]
                    for j in range(0, i-2):
                        fname += args[j] + " "
                    break
                else:
                    return None, None, None
            elif i == len(args)-1:
                for j in range(0, i-1):
                    fname += args[j] + " "
                bits[0] = args[i-1]
                bits[1] = args[i]
    fname = fname.strip(" ")
    
    return fname, bits, index


@client.command(aliases=['fa'])
async def frameadd(ctx, *, args=""):
    if await isWhitelisted(ctx, commander_in_chief, "add a frame to the `frame_info.json` file."):
        args = args.split(" ")
        all_bits = open_json(bits_file)
        for i in range(0, len(all_bits['bits'])):
            all_bits['bits'][i] = all_bits['bits'][i].lower()
            
        fname, bits, index = collect_args_frameadd(args)
        
        if index != None:
            index = int(index)
        #print(fname, bits, all_bits['bits'])
        #print("> bit check: ", bits[0] in all_bits['bits'], bits[1] in all_bits['bits'])
        if len(fname) > 0 and bits[0] in all_bits['bits'] and bits[1] in all_bits['bits']:
            frame_info = open_json(frame_info_file)
            new_frame = {
                "frame": fname,
                "bits": bits
                }
            if index != None:
                # minus 2 to index, match with frame shop which has 2 gem frames at the start
                frame_info['frames'].insert(index-2, new_frame)
            else:
                frame_info['frames'].insert(len(frame_info['frames']), new_frame)
            write_json(frame_info, frame_info_file)
            await ctx.send(f":white_check_mark: {ctx.author.mention} Successfully sent the frame `{fname}` with the bits `{bits}` to `frame_info.json`.")
        else:
            await ctx.send(f":no_entry: {ctx.author.mention} Invalid usage of `.frameadd` command. `(Invalid Parameters or Bits)`")


@client.command(aliases=['na'])
async def nodeadd(ctx, *, args=""):
    if await isWhitelisted(ctx, commander_in_chief, "add a node to the `bits.json` file."):
        args = args.split(" ")
        all_bits = open_json(bits_file)
        if not args[0] in all_bits['bits']:
            all_bits['bits'].append(args[0])
            write_json(all_bits, bits_file)
            await ctx.send(f":white_check_mark: {ctx.author.mention} Successfully added bit node `{args[0]}` to `bits.json` file.")
        else:
            await ctx.send(f":no_entry: {ctx.author.mention} The bit node `{args[0]}` is already in the `bits.json` file!")

# ==============================================================================


@client.command(aliases=['d'])
async def dice(ctx, arg1=None, arg2=None):
    global max_dice_roll
    if arg1 == 'set':
        if await isWhitelisted(ctx, commander_in_chief, "set the maximum dice roll."):
            if arg2.isdigit():
                max_dice_roll = int(arg2)
                await ctx.send(f':white_check_mark: Set the max dice roll to `{max_dice_roll}`.')
            else:
                await ctx.send(f':no_entry: Invalid integer.')
    elif arg1 == None:
        await ctx.send(f':game_die: Your roll was: `{random.randint(1, max_dice_roll)}`! {ctx.author.mention}')
    else:
        await ctx.send(f':no_entry: Incorrect command syntax. `[set]`')

# ==============================================================================

# Character question remember

async def send_embed_info(channel, emb):
    emb_str = f"```{emb['title']} \n{emb['description']}"
    if "footer" in emb:
        emb_str += f"\n{emb['footer']['text']}"
    emb_str += f"```"
    await channel.send(emb_str)

@client.command(aliases=['ec'])
async def embedcheck(ctx, message_id: int):
    # fetch a message from the same channel
    msg = await ctx.fetch_message(message_id)
    emb = msg.embeds[0].to_dict()
    await send_embed_info(msg.channel, emb)

# ==============================================================================

#@client.event
#async def on_command_error(ctx, error):
#    print(error)
#    pass

work_messages = []
karuta_server_id = 810628552529018930
work_success_emotes = [':candy:', ':bubble_tea:', ':tada:', ':confetti_ball:', ':partying_face:']

async def karuta_injury_check(message):
    # checked for karuta bot, karuta server
    # checked to see if message is embed (blank)
    # fetched message content for embed
    gid = str(message.guild.id)
    wr = open_json(work_reminder_file)
    
    embed = message.embeds[0]
    embed = embed.to_dict()
    desc = embed['description']
    inj_str = 'injured:**```css\n'
    
    # parse through injury embed description, find all cards
    if embed['title'] == 'Work':
        ws_dict = open_json(work_stats_file)
        uid = str(desc[desc.index('<@') + 2:desc.index('>')])
        user = await client.fetch_user(uid)
        
        if desc.find(inj_str) != -1:
            # initialize uid
            # add profile if not existing
            # initialize profile
            
            
            await check_work_profile(message, wr, uid, gid)
            profile = wr[gid][uid]
            
            # set desc string to end of injured string
            desc = desc[desc.index(inj_str)+len(inj_str):]
            desc = desc[:desc.index('```')]
            # keep looping until all injured cards are parsed
            
            while len(desc) > 1:
                card = desc[:desc.index(' [')]
                days = int(desc[desc.index('[') + 1: desc.index(' days')])
                desc = desc[desc.index(']\n')+2:]
                rd = datetime.now() + timedelta(days=int(days))
                new_card = {
                    'card': f'{card}',
                    'days': days,
                    'recovery_date': [rd.year, rd.month, rd.day, rd.hour, rd.minute]
                    }
                
                # sort card into profile array
                if len(profile) >= 1:
                    # for every card in profile array
                    for i in range(0, len(profile)):
                        if profile[i]['days'] >= days:
                            profile.insert(i, new_card)
                            break
                        elif i == len(profile)-1:
                            profile.insert(len(profile), new_card)
                            break
                else:
                    profile.insert(len(profile), new_card)
            
                await message.channel.send(f':white_check_mark: {user.mention} `{card}` has been added to reminder dictionary. It will recover in `{days}` days.')
            
            if ws_dict[gid][uid]["no_injury_streak"] > 0:
                await message.channel.send(f':octagonal_sign: {user.mention} You have broken your streak of working `{ws_dict[gid][uid]["no_injury_streak"]}` time*(s)* without an injury!')
                ws_dict[gid][uid]["no_injury_streak"] = 0
                write_json(ws_dict, work_stats_file)
            write_json(wr, work_reminder_file)
            
        elif desc.find('Your workers have finished their tasks') != -1:
            #print(desc, "\n" + str(desc.find('Your workers have finished their tasks.')) )
            celebrate_index = random.randint(0, len(work_success_emotes)-1) # includes both ends
            ws_dict[gid][uid]["no_injury_streak"] += 1
            write_json(ws_dict, work_stats_file)
            await message.channel.send(f':white_check_mark: {user.mention} You have successfully worked without injury. \n{work_success_emotes[celebrate_index]} Your injury free streak is: `{ws_dict[gid][uid]["no_injury_streak"]}`!')
        else:
            await message.channel.send(f':ballot_box_with_check: {user.mention} You decided to cancel your work.')

async def karuta_injury_setup(msg):
    # karuta bot, and kawuta server
    wr_file = open_json(work_reminder_file)
    if msg.author.id == 646937666251915264 and str(msg.guild.id) in wr_file:
#         if message.content == "":
#             msg = await message.channel.fetch_message(message.id)
        if len(msg.embeds) > 0:
            embed = msg.embeds[0]
            embed = embed.to_dict()
            if embed['title'] == 'Work':
                # add work message to array, wait for when edited and work has been done
                work_messages.append(msg.id)

# ==============================================================================

tcount = 1
tcount_max = 12
timeloop_seconds = 60*60
ksid = str(karuta_server_id)

@client.command(aliases=['tloop'])
async def timeloop(ctx, arg1=None):
    global timeloop_seconds
    if await isWhitelisted(ctx, commander_in_chief, "set the time loop seconds."):
        if arg1 == None:
            await ctx.send(f":clock1: {ctx.author.mention} The time loop is running every `{timeloop_seconds}` seconds.")
        elif arg1.isdigit() and int(arg1) > 1:
            timeloop_seconds = int(arg1)
            time_loop.change_interval(seconds=timeloop_seconds)
            time_loop.restart()
            await ctx.send(f":white_check_mark: {ctx.author.mention} Changed the time loop interval to `{timeloop_seconds}` seconds.")
        else:
            await ctx.send(f":no_entry: {ctx.author.mention} Invalid integer for seconds.")


# https://discordpy.readthedocs.io/en/latest/ext/tasks/

async def send_remind_check(setchannel_id, last_updated, today):
    await client.wait_until_ready()
    channel = client.get_channel(setchannel_id)
    await channel.send(f":cityscape: **Work Reminder** Another day has passed...\n`Last Updated`: {last_updated}\n`Today`: {today}")

async def send_now_time(setchannel_id, datetime_now):
    await client.wait_until_ready()
    channel = client.get_channel(setchannel_id)
    await channel.send(f'Hourly Update Time: `{datetime_now}`')

async def send_reminder(setchannel_id, uid, card):
#     print(f'\n\t=== SET REMINDER: === uid: {uid}')
    await client.wait_until_ready()
    channel = client.get_channel(setchannel_id)
    uid = int(uid)
    user = await client.fetch_user(uid)
#     print(f'\t\tUSER CLIENT: {user}\n\t\tSET CHANNEL: {channel}')
    now = datetime.now()
    await channel.send(f':alarm_clock: {user.mention} Your card `{card}` has recovered! ')


async def update_all_cards(wr):
    bool_sent_now = False
    today = datetime.now()
    for server_id in wr:
        for uid, profile in wr[server_id].items():
            # prevent update operation on these two string storages
            if uid != "last_updated" and uid != "setchannel":
    #             print(f'\t\tlen of profile: {len(profile)}, profile: {profile}')
                if len(profile) > 0:
                    i = 0
                    last_updated = wr[server_id]['last_updated']
    #                 print(f"===> DATE UPDATED: {last_updated}")
                    last_updated = datetime(last_updated[0], last_updated[1], last_updated[2])
                    days_diff = (today - last_updated).days
                    
                    while i < len(profile):
                        profile[i]['days'] = profile[i]['days'] - days_diff
                        # if found a card that requires a remind
    #                     print(f"DAYS IF STATEMENT CHECK: {profile[i]['days']}, {profile[i].get('card')}")
                        rd = profile[i]['recovery_date']
                        rd_dt = datetime(rd[0], rd[1], rd[2], rd[3], rd[4])
                        timedelta_secs = (today - rd_dt).total_seconds()
                        
                        if profile[i]['days'] <= 0 and timedelta_secs > 0:
                            
                            # bool_sent_now, used for sending time check first time
                            if bool_sent_now == False:
                                bool_sent_now = True
                                await send_now_time(wr[server_id]['setchannel'], today)
                                
                                
                            await send_reminder( wr[server_id]['setchannel'], uid, profile[i].get('card'))
                            profile.pop(i)
                        else:
                            i = i + 1

async def update_last_updated(wr, server_id):
    today = datetime.now()
    wr[server_id]['last_updated'] = [today.year, today.month, today.day, today.hour, today.minute]
    write_json(wr, work_reminder_file)

# client.get_user(uid) returning none: https://stackoverflow.com/questions/61112322/get-userid-cant-find-user-returns-none-self-bot-discord-py
@tasks.loop(seconds=timeloop_seconds)
async def time_loop():
    global tcount
    
    wr = open_json(work_reminder_file)
    
    for server_id in wr:
        last_updated = wr[server_id]['last_updated']
        past_date = datetime(last_updated[0], last_updated[1], last_updated[2], last_updated[3], last_updated[4])
        present_date = datetime.now()
        
        print(f'...time loop... tcount: \t{tcount} \n\tpast_date: {past_date}\tpresent date: {present_date}\n')
        
        # (present - past) is a timedelta object
        timedelta_compare = (present_date - past_date)
        if timedelta_compare.days >= 0 or timedelta_compare.seconds >= timeloop_seconds-1:
            print(f'... > Checking cards now!')
            last_updated = wr[server_id]['last_updated']
            last_updated_str = f'{last_updated[0]}-{last_updated[1]}-{last_updated[2]}'
            today = datetime.now()
            today = f'{today.year}-{today.month}-{today.day}'
            if timedelta_compare.days >= 1:
                await send_remind_check(wr[server_id]['setchannel'], last_updated_str, today)
            await update_all_cards(wr)
            await update_last_updated(wr, server_id)
            
        tcount = tcount + 1
        if tcount > tcount_max:
            tcount = 1

def init_time_loop():
    time_loop.change_interval(seconds=timeloop_seconds)
    time_loop.start()
    print('init_time_loop(): started!')


# ==============================================================================


@client.command(aliases=['stop'])
async def exit(ctx):
    if await isWhitelisted(ctx, commander_in_chief, "exit the bot program") == True:
        await ctx.send(f':white_check_mark: Goodbye~ :heart:\n`[ Raspberry Pi 4 is Closing the Python Instance ]`')
        time_loop.stop()
        sys.exit()


egg_help_embed = {
    'color': 16776960,
    'author': {
        'name': f'Egg Command Help',
        'icon_url': f'https://discord.com/assets/5ca0c0b0ad60ee4b580e7ed918426cdb.svg'
        },
    'footer': {
        'text': ''
        },
    'fields':[
        {
            'name': '`.eggs`',
            'value': 'Shows the eggs that you are currently looking for.'
            },
        {
            'name': '`.egg set <Egg Numbers>`',
            'value': 'Sets the eggs that you would like to watch for. Maximum of 5 eggs.'
            },
        {
            'name': '`.egg clear`',
            'value': 'Clears your egg reminder dictionary.'
            },
        {
            'name': '`.egg help`',
            'value': 'Shows this help command.'
            }
        ]
    }


@client.command()
async def egg(ctx, *, param=""):
    param = param.lower()
    # check if user is inside egg_dict
    uid = str(ctx.author.id)
    egg_dict = open_json(egg_dict_file)
    
    if not uid in egg_dict:
        egg_dict[uid] = []
        await ctx.send(f":white_check_mark: {ctx.author.mention} Your profile was added to the egg dictionary.")
        
    if param == "" or param == "help":
        await ctx.send(embed=discord.Embed.from_dict(egg_help_embed))
    # not a help command / empty
    else:
        param = param.split(" ")
        if param[0] == "set":
            if len(param) <= 6:
                if len(param) > 1:
                    egg_dict[uid] = []
                    for i in range(1, len(param)):
                        if param[i].isdigit() and not param[i] in egg_dict[uid]:
                            if int(param[i]) < 1 or int(param[i]) > 20:
                                 await ctx.send(f":no_entry: {ctx.author.mention} One of your eggs was not a valid number between `(1-20)`!")                                
                            else:
                                egg_dict[uid].append(param[i])
                        else:
                            await ctx.send(f":no_entry: {ctx.author.mention} One of your eggs was not a number. Try again.")
                            return
                    write_json(egg_dict, egg_dict_file)
                    await ctx.send(f':white_check_mark: {ctx.author.mention} You have set your eggs to: `{egg_dict[uid]}`.')
                else:
                    await ctx.send(f":no_entry: {ctx.author.mention} You used the `set` command without adding any eggs!")
                print(f"{ctx.author.name}'s EGG DICT: \n{egg_dict[uid]}")
            else:
                await ctx.send(f":no_entry: {ctx.author.mention} You added too many eggs! `[Maximum of 5]`.")
        elif param[0] == 'clear' or param[0] == 'c':
            egg_dict[uid] = []
            write_json(egg_dict, egg_dict_file)
            await ctx.send(f':white_check_mark: {ctx.author.mention} Egg dictionary has been cleared.')
        elif param[0] == 'print' or param[0] == 'p' and await isWhitelisted(ctx, commander_in_chief, "print the egg dictionary"):
            await ctx.send(f"```\n{egg_dict}\n```")
        else:
            await ctx.send(f':no_entry: {ctx.author.mention} Invalid usage of command `egg`.')


@client.command()
async def eggs(ctx):
    uid = str(ctx.author.id)
    egg_dict = open_json(egg_dict_file)
    if uid in egg_dict:
        if len(egg_dict[uid]) > 0:
            await ctx.send(f":egg: {ctx.author.mention} You are currently looking for eggs `{egg_dict[uid]}`.")
        else:
            await ctx.send(f":no_entry: {ctx.author.mention} You do not have any eggs in your egg dictionary! Add some using the `set` command.")
    else:
        await ctx.send(f":no_entry: {ctx.author.mention} Your profile has not been made for egg dictionary. Please use the command `egg`.")

async def egg_claimed(message):
    if message.author.id == 646937666251915264:
        if "you placed **Springtide Egg" in message.content:
            print(f'CLAIMED EGG: ')
            uid = str(message.mentions[0].id)
            hash_index = message.content.index('#')
            egg = message.content[hash_index+1:]
            #egg = egg.strip("#* ")
            print(f'CLAIMED egg edit 1: {egg}')
            egg = egg[:egg.find('*')]
            print(f'CLAIMED egg edit 2: {egg}')
            egg = int(egg)
            
            egg_dict = open_json(egg_dict_file)
            print("\t> IS EGG {egg} INSIDE {message.mentions[0]}'s dict?: {egg in egg_dict[uid]}")
            if uid in egg_dict:
                #if egg in egg_dict[str(uid)]:
                for i in range(0, len(egg_dict[uid])):
                    print(f"checking {message.mentions[0]}: '{egg_dict[uid][i]}', is equal to '{egg}'?: {int(egg_dict[uid][i]) == int(egg)}")
                    if int(egg_dict[uid][i]) == egg:
                        egg_dict[uid].pop(i)
                        write_json(egg_dict, egg_dict_file)
                        await message.channel.send(f":white_check_mark: {message.mentions[0].mention} `Egg #{egg}` has been removed from your egg dictionary.\n Remaining: `{egg_dict[uid]}`.")
                        return
                # after you check through person's egg dict, and don't find claimed egg
                #await message.channel.send(f":no_entry: `Egg #{egg}` was not found in your egg dictionary.", delete_after=10)
            else:
                if not uid in egg_dict:
                    await message.channel.send(f":no_entry: User `{message.mentions[0]}` does not have an egg dictionary.", delete_after=10)

                elif not egg in egg_dict[uid]:
                    await message.channel.send(f":no_entry: User `{message.mentions[0]}` does not have `Egg #{egg}` in their egg dictionary.", delete_after=10)


async def check_egg_emote(reaction, user):
    if user.id == 646937666251915264: # if it is karuta bot
        if str(reaction).find(":stEgg") != -1:
            print("REACT message content: ", reaction.message.content)
            react = str(reaction).strip("<:stEgg>")
            print('react1:', react)
            react = react[:react.find(":")]
            print('react2:', react)
            react = react.strip("a ")
            print('react3:', react)
            new_egg = int(react)
            
            egg_dict = open_json(egg_dict_file)
            # check each egg dictionary
            for uid in egg_dict:
                print(f"> egg check for UID {uid}")
                if len(egg_dict[uid]) > 0:
                    for wanted_egg in egg_dict[uid]:
                        print(f"> check {uid}: wanted: {wanted_egg}, checking: {new_egg}, same? = {int(wanted_egg == new_egg)}")
                        if int(wanted_egg) == new_egg:
                            person = await client.fetch_user(int(uid))
                            print(f"\t> FOUND EGG THAT IS WANTED")
                            if len(egg_dict[uid]) == 1:
                                await reaction.message.channel.send(f":egg: <:pogu:819461856875773972> :warning: The Last Egg :warning: that you're missing `Egg #{new_egg}` has spawned! {person.mention}")
                                break
                            else:
                                await reaction.message.channel.send(f":egg: An egg that you're missing `Egg #{new_egg}` has spawned! {person.mention}")
                                break
            

# @client.command()
# async def setuptemplate(ctx):
#     qstor = open_json(_question_storage_file)
#     tchar = open_json(_template_char_file)
#     num_questions = qstor['number_of_questions']
#     for i in range(0, num_questions):
#         tchar['answers'].append(None)
#         tchar['correct?'].append(None)
#         
#     write_json(tchar, _template_char_file)
#     
#     await ctx.send(f"{ctx.author.mention} Set up the `_template_char.json` file.")




# KOIBITO: for when talking, but not answered yet
def koibito_parse_talk(embed):
    desc = embed['description']
    # shorten for question parse
    desc = desc[desc.find("Energy"):len(desc)]
    question = desc[ desc.find('*“') + 2:desc.find('”*') ]
    
    # shorten for answer parse
    desc = desc[desc.find("”*") + 2:len(desc)]
    answers = desc.split("\n")
    # remove any blank answers that may be in the beginning of answers array
    while "" in answers:
        answers.remove("")
    
    return question, answers


    # emote unicode source
    # https://gist.github.com/scragly/b8d20aece2d058c8c601b44a689a47a0
    # https://apps.timwhitlock.info/emoji/tables/unicode#block-6b-additional-transport-and-map-symbols
    # LIST: https://unicode.org/emoji/charts/emoji-list.html

# used for TEMPORARY manual questions by bot
manual_questions_array = []
# example manual question:
# {
# "message": Message object,
# "question_message_id": int,
# "user_id": int
# "character": "",
# "question": "",
# "question_index": int,
# "answer": int,
# "answers": list (string)
# "datetime": datetime object
# }

# TEMPORARY command
# Print manual question array, part of Karuta question bot
@client.command()
async def printmqa(ctx):
    print('> printmqa Called!')
    for entry in manual_questions_array:
        print( entry['question_message_id'])
        print( entry['user_id'])
        print( entry['character'])
        print( entry['question'])
        print( entry['question_index'])
        print( entry['answer'])
        print( entry['answers'])
        print( "--------------------\n")

def remove_entry_from_manual_questions_array(message_id):
    for i in range(len(manual_questions_array)):
        if manual_questions_array[i]['message'].id == message_id:
            manual_questions_array.pop(i)

# Returns bool: correct reaction, 
def find_message_id_in_manual_questions_array(message_id):
    for i in range(len(manual_questions_array)):
        # When checking manual questions array, if any questions have been active for more than 40 seconds
        if (datetime.now() - manual_questions_array[i]['datetime']).seconds >= 40:
            manual_questions_array.pop(i)
            i = i - 1
            print("> find_message_id_in_manual_questions_array(): \n\t>- Found entry which was expired by 20 seconds. Removing!")
            pass
        elif manual_questions_array[i]['message'].id == message_id:
            return True, manual_questions_array[i]
    return False, None

def find_question_message_id_in_manual_questions_array(question_message_id):
    for i in range(len(manual_questions_array)):
        if manual_questions_array[i]['question_message_id'] == question_message_id:
            selected_entry = manual_questions_array[i]
            # After finding the right MQ entry, delete from array
            manual_questions_array.pop(i)
            # Return the MQ entry, used in after-answered koibito_check()
            return selected_entry
    return False

# After 20 seconds, remove manual question (Stage: Question is unknown for specific character)
def remove_expired_manual_question(manual_question_id):
    check_entry_bool, entry = find_message_id_in_manual_questions_array(manual_question_id)
    if check_entry_bool != False:
        remove_entry_from_manual_questions_array(manual_question_id)
        print(f"> Removed manual question of id: ({manual_question_id}) from array.")
    else:
        print(f" Attempted to remove manual question of id: ({manual_question_id}) from array. Unsuccessful, deleted already.")

def get_correct_answer_index(qstor, actual_answer_str, question_index):
    for i in range( len(qstor['answers'][question_index]) ):
        stored_answer = qstor['answers'][question_index][i]
        # Answer positions on karuta bot may not line up with stored question's answers
        # Comparison to get the correct index
        if stored_answer[1:len(stored_answer)] == actual_answer_str:
            # answer = i
            # break
            return i
        elif i == len(qstor['answers'][question_index]) - 1:
#             error_str = f'> :no_entry: {client.get_user(uid).mention} Something has gone **terribly wrong** with the `Karuta` and `_question_storage.json` answer comparison tests. '
#             error_str += f'\n> Please contact bot developer. {client.get_user(admin_whitelist[2]).mention}'
#             error_str += f'\n`{question}` \n#{question_index} \n{answers} \n{character}'
#             await message.channel.send(error_str)
            return None

# Specifically for checking Nezuko-chan (as of currently)
def check_char_aliases(char):
    aliases_file = open_json(koibito_aliases_file)
    characters_with_aliases = aliases_file["characters"]
    char_aliases = aliases_file["aliases"]
    
    for i in range(len(char_aliases)):
        if char in char_aliases[i]:
            return characters_with_aliases[i]
    return char

def create_new_char_file(char_file, new_char_path):
    with open(new_char_path, 'w') as char_file:
        new_template = open_json(_template_char_file)
        write_json(new_template, new_char_path)

all_number_emotes = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']

@client.event
async def on_reaction_add(reaction, user):
    # for egg remind
    # await check_egg_emote(reaction, user)
    # reaction.message.author
    
    # KOIBITO temporary manual questions
    # Check if message is from Mai Sakurajima bot
    if reaction.message.author.id == 731644582164430870 and user.id != 731644582164430870:
        correct_reaction_bool, reactioned_manual_question = find_message_id_in_manual_questions_array(reaction.message.id)
#         if reactioned_manual_question != None and reactioned_manual_question['answer'] == None:
#             print("> on_reaction_add: ", correct_reaction_bool, reactioned_manual_question['message'].id, reactioned_manual_question['character'], reactioned_manual_question['question'], reactioned_manual_question['question_index'])
        
        if correct_reaction_bool != False and reactioned_manual_question['user_id'] == user.id:
            for i in range(len(all_number_emotes)):
                if str(reaction) == all_number_emotes[i]:
                    # Change the entry in the manual_questions_array
                    reactioned_manual_question['answer'] = i
                    
                    # Edit the message as soon as the reaction is added
                    rmq_message = reactioned_manual_question['message']
                    await rmq_message.edit(content=f"{rmq_message.content}\n:white_check_mark: You chose option {reaction}.")


# Used in command .simq, and when a question is added into the 
def check_answer_group_in_simq(simq, answers, agi):
    # For every question in Same Answer Group
    # sagi = Same Answer Group Index
    for sagi in range(len(simq['answer_group'][agi])):
        simq_answer = simq['answer_group'][agi][sagi]
        # Boolean for the specific simq answer
        bool_found_answer = False
        for answers_index in range(len(answers)):
            qstor_answer = answers[answers_index]
            if qstor_answer[1:len(qstor_answer)] == simq_answer[1:len(simq_answer)]:
                bool_found_answer = True
        if bool_found_answer == False:
            break
        elif sagi == len(simq['answer_group'][agi]) - 1:
            return True
    return False

# Used for: Similar questions (simq)
# Returns the boolean / target index required for sorting into simq
# Return: found_target_ag, target_ag_index 
def return_answer_group_and_index(simq, question, answers):
    print("> DURING return_answer_group_and_index(): ", question, answers)
    found_target_ag = False
    target_ag_index = 0
    
    # For every group of answers in simq
    for agi in range(len(simq['answer_group'])):
        # For every answer in the qstor answer array
        bool_is_ag_matching = False
        bool_is_ag_matching = check_answer_group_in_simq(simq, answers, agi)
                
        if bool_is_ag_matching == True:
            found_target_ag = True
            target_ag_index = agi
            print(f"> return_answer_group_and_index(): \nFound Question/answer pair: \n\t> Question: {question} \n\tAnswers: {answers}")
            return found_target_ag, target_ag_index

def return_sorted_simq(simq, question, question_index, answers):
    target_ag_index = 0
    found_target_ag = False
    # Sort the question / answer into simq (_similar_questions.json)
    found_target_ag, target_ag_index = return_answer_group_and_index(simq, question, answers)
    
    if found_target_ag == False:
        simq['answer_group'].append(answers)
        simq['similar_question_indexes'].append([])
        simq['similar_questions'].append([])
        target_ag_index = len(simq['similar_question_indexes']) - 1
        simq['similar_question_indexes'][target_ag_index].append(question_index)
        simq['similar_questions'][target_ag_index].append(question)
    elif found_target_ag == True:
        simq['similar_question_indexes'][target_ag_index].append(question_index)
        simq['similar_questions'][target_ag_index].append(question)
    return simq

def highlight_koibito_keywords(simq_question):
    simq_question = simq_question.replace("least", "**LEAST**")
    simq_question = simq_question.replace("most", "**MOST**")
    return simq_question

# @client.command()
# async def simq(ctx):
#     if await isWhitelisted(ctx, admin_whitelist, perm = 'can setup the similar question json file.'):
#         qstor = open_json(_question_storage_file)
#         simq = open_json(_similar_questions_file)
#         # For every single question / answer in qstor
#         for i in range(len(qstor['questions'])):
#             question = qstor['questions'][i]
#             answers = qstor['answers'][i]
#             # For adding question to an answer group
#             
#             simq = return_sorted_simq(simq, question, i, answers)
#         
#         write_json(simq, _similar_questions_file)


@client.command()
async def editfiles(ctx):
    if await isWhitelisted(ctx, admin_whitelist, perm = 'can edit character files'):
        _pathdir = "/home/pi/discordbot/char_questions"
        for filename in os.listdir(_pathdir):
            print(filename)
            # Check for file that isn't character files
            if not filename == "_question_storage.json" and filename.endswith(".json"): 
                char_file_path = _pathdir + "/" + filename
                char_file = open_json(char_file_path)
                
#                 char_file["number_of_answered_questions"] = 0
#                 for i in range(len(char_file['answers'])):
#                     if char_file['answers'][i] != None:
#                         char_file["number_of_answered_questions"] += 1
#                 
#                 write_json(char_file, char_file_path)
#                 
#                 info_str = f"> Updated: {filename}, Has length of: {len(char_file['answers'])} "
#                 info_str += f"\n\tCorrect questions: {char_file['number_of_correct_questions']} "
#                 info_str += f"\n\tAnswered Questions: {char_file['number_of_answered_questions']}"
#                 print(info_str)

                
                # Refresh number of correct questions
#                 char_file['number_of_correct_questions'] = 0                
#                 for i in range(len(char_file['correct?'])):
#                     if char_file['correct?'][i] == True:
#                         char_file['number_of_correct_questions'] += 1

                # Add
                num = 100
                for i in range(0, num):
                    char_file['answers'].append(None)
                    char_file['correct?'].append(None)
                write_json(char_file, char_file_path)
                await ctx.send(f"{ctx.author.mention} Added `{num}` question slots to all `character.json` files.")


question_bot_help = {
    'color': 15277667,
    'author': {
        'name': f'Question Koibito Bot',
        'icon_url': f'https://media.discordapp.net/attachments/874760928304988240/877690245204824135/70e2e710d9ea845df9bba730bcdb0e02.png'
        },
    'footer': {
        'text': ''
        },
    'fields':[
        {'name': '`info` `<character name>`',
         'value': 'Sends the character\'s amount of correct/answered questions, similar question groups'},
        {'name': '`<question index>` `<character name>`',
         'value': 'Sends the specific question information for the character.'},
        {'name': '`simq`',
         'value': 'Send the number of similar question groups.'},
        {'name': '`simq` `<similar group index>`',
         'value': 'Sends the information of the specified similar question group. *0-max*'},
        {'name': '`date`',
         'value': 'Send the date guide image.'},
        
        {'name': ':mag_left: `showaliases`',
         'value': 'Shows all aliases for characters in question bot.'},
        {'name': ':lock: `addalias` `<character name>` `"<alias>"`',
         'value': 'Add an alias for a character. *(Include quotation)*'}
        ]
    }

def parse_char(start_index, args):
    char = ""
    for i in range(start_index, len(args)):
        args[i] = args[i].capitalize()
        char += args[i] + " "
    char = char.strip(" ")
    char = char.replace(" ", "_")
    return char

# Question bot command
@client.command(aliases=['q'])
async def question(ctx, *, args=None):
    
    if args == None or args == "help":
        question_help_embed = discord.Embed.from_dict(question_bot_help)
        await ctx.send(embed=question_help_embed)
    else:
        args = args.split(" ")
        # .question <question_index>  <character_name> 
        if args[0].isdigit() and len(args) >= 2:
            qstor = open_json(_question_storage_file)
            # .question 250 nezuko kamado
            # args = [250, nezuko, kamado]
            # Parse args for character name
            len_questions = len(qstor['questions'])
            args[0] = int(args[0])
            if 0 <= args[0] and args[0] < len_questions:
                char = parse_char(1, args)
                
                char_file = find_file(f"{char}.json", "/home/pi/discordbot/char_questions")
                # if the character file exists
                if char_file != None:
                    # comment 3 : make similar question index for individual assignment
                    char_file_path = f'/home/pi/discordbot/char_questions/{char}.json'
                    char_file = open_json(char_file_path)
                    
                    question = qstor['questions'][args[0]]
                    char_correct_status = char_file['correct?'][args[0]]
                    if char_correct_status == True:
                        char_correct_status = f":white_check_mark: **{char_correct_status}**"
                    else:
                        char_correct_status = f":no_entry: **{char_correct_status}**"
                    
                    char_answers = char_file['answers'][args[0]]
                    if char_answers != None:
                        if char_file['correct?'][args[0]] == True:
                            answer_index = char_file['answers'][args[0]]
                            char_answers = f"{qstor['answers'][args[0]][answer_index]}"
                        elif char_file['correct?'][args[0]] == False:
                            char_answers = ""
                            
                            for i in range(len(char_file['answers'][args[0]])):
                                answer_index = char_file['answers'][args[0]][i]
                                char_answers += f"{qstor['answers'][args[0]][answer_index]}"
                    mstr = f"{ctx.author.mention} \n> :grey_question: Question **#{args[0]}** `{question}`"
                    mstr += f"\n> Correct? : " + char_correct_status
                    mstr += f"\n> Answer : {char_answers}"
                    await ctx.send(mstr)
                else:
                    await ctx.message.delete()
                    await ctx.send(f":no_entry: {ctx.author.mention} Character file with the name `{char}` has not been found.", delete_after=5)
            else:
                await ctx.send(f":no_entry: {ctx.author.mention} Question #{args[0]} does not exist!")
        # Character info
        elif args[0] == "info":
            await ctx.send(f"{ctx.author.mention} Character info command not implemented yet.")
        # Similar questions info
        elif args[0] == "aa" or args[0] == "addalias":
            # Add aliases of characters for koibito questions
            # koibito_aliases_file
            aliases_file = open_json(koibito_aliases_file)
            chars_array = aliases_file["characters"]
            aliases_array = aliases_file["aliases"]
            
            args_index = 1
            adding_to_alias = False
            char = ""
            alias = ""
            # While loop to parse through character / alias from arguments
            while args_index < len(args):
                # If we are still registering the character name
                if args[args_index].startswith('"'):
                    adding_to_alias = True
                    
                if not adding_to_alias:
                    char += args[args_index] + " "
                else:
                    alias += args[args_index] + " "
                args_index += 1
                
                # If by the end, there is no correct alias in arguments
                if args_index == len(args) and adding_to_alias == False:
                    await ctx.send(f":no_entry: {ctx.author.mention} Incorrect Alias formatting. ***(Include quotations)***")
                    return None
            
            char = char.strip(" ")
            alias = alias.strip('" ')
            
            target_index = -1
            if char in chars_array:
                for i in range(0, len(chars_array)):
                    if chars_array[i] == char:
                        target_index = i
                        break
                aliases_array[target_index].append(alias)
            else:
                # No need for target index if adding a new character
                chars_array.append(char)
                aliases_array.append([alias])
                write_json(aliases_file, koibito_aliases_file)
                
            await ctx.send(f":white_check_mark: {ctx.author.mention} Character `{char}` has been added to `koibito_aliases.json` with Alias: `{alias}`")
            
        elif args[0] == "sa" or args[0] == "showaliases":
            # Show all aliases for characters
            aliases_file = open_json(koibito_aliases_file)
            chars_array = aliases_file["characters"]
            aliases_array = aliases_file["aliases"]
            
            mstr = f"{ctx.author.mention}\n"
            for i in range(0, len(chars_array)):
                mstr += f'**{chars_array[i]}**\n> '
                mstr += f'`{aliases_array[i]}`\n'
                
            await ctx.send(mstr)
        elif args[0] == "simq":
            qstor = open_json(_question_storage_file)
            simq = open_json(_similar_questions_file)
            # .question simq <group_index>
            if len(args) > 1 and args[1].isdigit():
                group_index = int(args[1])
                if 0 <= group_index and group_index < len(simq['similar_question_indexes']):
                    # comment 3 : write info for char
                    mstr = f"> :white_check_mark: {ctx.author.mention} Similar Group #**{group_index}**"
                    mstr += f"\n> Questions: **"
                    max_question_index = len(simq['similar_question_indexes'][group_index])
                    for i in range(max_question_index):
                        mstr += f"{simq['similar_question_indexes'][group_index][i]}"
                        if not i == max_question_index - 1:
                            mstr += ", "
                    mstr += "**"
                    
                    # Random showcase question, designed to be 
                    random_similar_question_index = random.randint(0, len(simq['similar_question_indexes'][group_index])-1)
                    random_showcase_index = simq['similar_question_indexes'][group_index][random_similar_question_index]
                    showcase_question = qstor['questions'][random_showcase_index]
                    mstr += f"\n#**{random_showcase_index}** *`" + showcase_question + "`*"
                    
                    mstr += f"\nAnswers: \n"
                    for i in range(len(simq['answer_group'][group_index])):
                        mstr += f"{simq['answer_group'][group_index][i]}\n"
                    await ctx.send(mstr)
                else:
                    await ctx.send(f":no_entry: {ctx.author.mention} Similar group of index {group_index} is invalid!")
            else:
                simq = open_json(_similar_questions_file)
                await ctx.send(f"{ctx.author.mention} \n> There are a total of `{len(simq['answer_group'])}` groups of similar questions.")
        # Send date guide image
        elif args[0] == "date":
            await ctx.message.delete()
            await ctx.send("https://media.discordapp.net/attachments/809242709607841864/868903659629600848/date-guide.png", delete_after=120)


text_unanswered = "Choose the response most likely to impress "
async def koibito_check(message, before=None):
    # check for embeds
    if len(message.embeds) > 0:
        emb = message.embeds[0].to_dict()
        
        # ===[  KOIBITO DATE QUESTION REMEMBER-ER  ]===
        if emb['title'] == "Visit Character":
            if 'footer' in emb:
                # ===[ Question page, unanswered ]===
                if emb['footer']['text'].find("Choose the response most likely to impress ") != -1:
                    footer = emb['footer']['text']
                    # text_unanswered = "Choose the response most likely to impress "
                    char = footer[footer.find(text_unanswered) + len(text_unanswered): len(footer)]
                    
                    # Check for name aliases, Specifically Nezuko-chan
                    char = check_char_aliases(char)
                    
                    question, answers = koibito_parse_talk(emb)
                    desc = emb['description']
                    uid = desc[desc.find("<@") + 2: desc.find(">")]
                    uid = int(uid)
                    question_index = None # index of question inside _question_storage.json
                    
                    qstor = open_json(_question_storage_file)
                    
                    # Check _question_storage.json, if the question is not there, add it
                    if not question in qstor['questions']:
                        qstor['questions'].append(question)
                        qstor['answers'].append(answers)
                        qstor['number_of_questions'] = len(qstor['questions'])
                        write_json(qstor, _question_storage_file)
                        
                        # Set the question index variable
                        question_index = qstor['questions'].index(question)
                        
                        simq = open_json(_similar_questions_file)
                        simq = return_sorted_simq(simq, question, question_index, answers)
                        write_json(simq, _similar_questions_file)
                        
                        await message.channel.send(f":white_check_mark: {client.get_user(uid).mention} \n> Added Question **#{len(qstor['questions']) - 1}**: *`{question}`*.")
                    else:
                        question_index = qstor['questions'].index(question)
                    
                    # find_file(name, path) - https://stackoverflow.com/questions/1724693/find-a-file-in-python
                    char = char.replace(" ", "_")
                    char_file = find_file(f"{char}.json", "/home/pi/discordbot/char_questions")
                    # if the character file exists
                    if char_file == None:
                        # create a clone of template, for the character
                        new_char_path = f'/home/pi/discordbot/char_questions/{char}.json'
                        create_new_char_file(char_file, new_char_path)
                        await message.channel.send(f"{client.get_user(uid).mention} Created new file `{char}.json`.")
                    
                    char_file_path = f'/home/pi/discordbot/char_questions/{char}.json'
                    char_file = open_json(char_file_path)
                    
                    # If question hasn't been answered correctly, then
                    if char_file['correct?'][question_index] != True:
                        # Add answers to the message in a string variable
                        answer_str = ""
                        for i in range(len(answers)):
                            answer_str += answers[i] + "\n"
                            
#                             Code: Checking unmatched answer positions on substring
#                             print(f"> Answer check: {answers[i]}")
#                             for ans in qstor['answers'][question_index]:
#                                 condensed_1 = answers[i][1:len(answers[i])]
#                                 condensed_2 = ans[1:len(ans)]
#                                 print(f"Checking: {condensed_1} == {condensed_2}: {condensed_1 == condensed_2}") 
#                             print("\n")
                            
                        # Send manual question message to user
                        manual_question_text = f':grey_question: {client.get_user(uid).mention}'
                        simq = open_json(_similar_questions_file)
                        
                        # Setup for Similar Question Algorithm
                        found_target_ag, target_ag_index = return_answer_group_and_index(simq, question, answers)
                        
                        # For every similar question to this question:
                        past_correct_answers = []
                        similar_questions_answered = False
                        for i in range(len(simq['similar_question_indexes'][target_ag_index])):
                            simq_index = simq['similar_question_indexes'][target_ag_index][i]
                            simq_question = qstor['questions'][simq_index]
                            print(f"\t> SIMQ question: #{simq_index} : {simq_question}")
                            
                            print(f"\t> answers: {char_file['answers'][simq_index]}")
                            if char_file['answers'][simq_index] != None:
                                print(f"\t\t> SIMQ answer: {qstor['answers'][simq_index]}\n")
                                if similar_questions_answered == False:
                                    manual_question_text += f"\n> :arrow_right: Previous Answers:"
                                    similar_questions_answered = True
                                
                                # Comment 3 : fix this method, wont highlight key words
                                simq_question = highlight_koibito_keywords(simq_question)
                                
                                # manual_question_text += f"\n> :pencil: #**{simq_index}** `{simq_question}`"
                                if char_file['correct?'][simq_index] == True:
                                    correct_answer_index = char_file['answers'][simq_index]
                                    simq_answer = qstor['answers'][simq_index][correct_answer_index]
                                    
                                    # If out of the already displayed correct answers, the duplicate isn't there
                                    if not simq_answer[1:len(simq_answer)] in past_correct_answers:
                                        # Add correct question text
                                        manual_question_text += f"\n> :pencil: #**{simq_index}** `{simq_question}`"
                                        past_correct_answers.append(simq_answer[1:len(simq_answer)])
                                        manual_question_text += f"\n> :white_check_mark: {simq_answer}"
                                        
                                elif char_file['correct?'][simq_index] == False:
                                    # Add question text
                                    manual_question_text += f"\n> :pencil: #**{simq_index}** `{simq_question}`"
                                    simq_all_answers = char_file['answers'][simq_index]
                                    for j in range(len(simq_all_answers)):
                                        simq_answer_index = simq_all_answers[j]
                                        simq_answer = qstor['answers'][simq_index][simq_answer_index]
                                        manual_question_text += f"\n> :no_entry: {simq_answer}"
                        
                        if similar_questions_answered == False:
                            manual_question_text += f'\n> Question #**{question_index}** has not been answered for `{char.replace("_", " ")}` yet.'
                        
                        # Previous Directly-incorrect question send
#                         if char_file['correct?'][question_index] == False:
#                             answers_str = ""
#                             for ans in char_file['answers'][question_index]:
#                                 answers_str += qstor['answers'][question_index][ans] + "\n"
#                             await message.channel.send(f':no_entry::grey_question: {client.get_user(uid).mention} \n> Previous answers to the question *`{question}`* are: \n{answers_str}')
                        
                        manual_question_text += f'\n#**{question_index}** \n{answer_str}'
                        manual_question = await message.channel.send(manual_question_text)
                        
                        # example manual question:
                        # {
                        # "message": Message object,
                        # "question_message_id": int,
                        # "user_id": int,
                        # "character": "",
                        # "question": "",
                        # "question_index": int
                        # "answer": int
                        # "answers": list (string)
                        # }
                        
                        # Add manual question to the manual_questions_array
                        manual_question_entry = {
                            "message": manual_question,
                            "question_message_id": message.id,
                            "user_id": uid,
                            "character": char,
                            "question": question,
                            "question_index": question_index,
                            "answer": None,
                            "answers": answers,
                            "datetime": datetime.now()
                            }
                        # Manual question will get deleted from array in function: find_message_id_in_manual_questions_array()
                        manual_questions_array.append(manual_question_entry)
                        print(f"> Added manual question of id: ({manual_question.id}) into manual_questions_array.")
                        
                        # Add reactions
                        for i in range(len(answers)):
                            await manual_question.add_reaction(all_number_emotes[i])
                            
                    elif char_file['correct?'][question_index] == True:
                        correct_answer_index = char_file['answers'][question_index]
                        correct_answer = qstor['answers'][question_index][correct_answer_index]
                        correct_answer = correct_answer[1:len(correct_answer)]
                        
                        for msg_answer in answers:
                            # comment 3
                            
                            if correct_answer == msg_answer[1:len(msg_answer)]:
                                correct_answer = msg_answer
                                
                        await message.channel.send(f":white_check_mark::grey_question: {client.get_user(uid).mention} \nPrevious correct answer: {correct_answer}")
                        
            # After a question is answered, no footer found
            elif not 'footer' in emb and emb['description'].find("Your Affection Rating has ") != -1:
                print('> AFTER-QUESTION  Response message!   Rating has...')
                # Check before question, see if it matches with any entries in manual_questions_array
                # If found, entry is deleted from array
                # Returns manual question entry dict
                
                bemb = before.embeds[0].to_dict()
                bdesc = bemb['description']
                uid = bdesc[bdesc.find("<@") + 2: bdesc.find(">")]
                uid = int(uid)
                answered_question_entry = find_question_message_id_in_manual_questions_array(before.id)
                
                if answered_question_entry != False:
                    # Find the information from the (before) answered question message
                    bemb = before.embeds[0].to_dict()
                    char = answered_question_entry['character']
                    question = answered_question_entry['question']
                    answer = answered_question_entry['answer']
                    answers = answered_question_entry['answers']
                    uid = answered_question_entry['user_id']
                    question_index = answered_question_entry['question_index'] # index of question inside _question_storage.json
                    
                    qstor = open_json(_question_storage_file)
                    char_file_path = f'/home/pi/discordbot/char_questions/{char}.json'
                    char_file = open_json(char_file_path)
                    char = char.replace("_", " ")
                    
                    # Find the status of the after-message
                    
                    # Add to "number_of_answered_questions"
                    if answer != None and char_file['answers'][question_index] == None:
                        char_file['number_of_answered_questions'] += 1
                    
                    # If answered correctly
                    if emb['description'].find("increased by") != -1:
                        # If the answer hasn't been answered correctly yet, and the person did answer
                        if char_file['correct?'][question_index] != True and answer != None:
                            # Find the right answer in _question_storage.json, set it to the correct index
                            # Substring to remove number and accurately compare stored question
                            actual_answer_str = answers[answer]
                            actual_answer_str = actual_answer_str[1:len(actual_answer_str)]
                            
                            answer = get_correct_answer_index(qstor, actual_answer_str, question_index)
                            
                            # If the function: get_correct_answer_index() returns None, due to no matching answer found 
                            if answer == None:
                                error_str = f'> :no_entry: {client.get_user(uid).mention} Something has gone **terribly wrong** with the `Karuta` and `_question_storage.json` answer comparison tests. '
                                error_str += f'\n> Please contact bot developer. {client.get_user(admin_whitelist[2]).mention}'
                                error_str += f'\n`{question}` \n#{question_index} \n{answers} \n{character}'
                                await message.channel.send(error_str)
                                return None
                            
                            # Update the {char}.json files with the correct answers / question status
                            char_file['answers'][question_index] = answer
                            char_file['correct?'][question_index] = True
                            char_file['number_of_correct_questions'] += 1
                            write_json(char_file, char_file_path)
                            
                            num_correct = char_file['number_of_correct_questions']
                            num_answered = char_file['number_of_answered_questions']
                            num_questions = qstor['number_of_questions']
                            
                            celebrate_index = random.randint(0, len(work_success_emotes)-1)
                            celebration_emote = work_success_emotes[celebrate_index]
                            # Change the answer from index to actual worded string
                            answer = qstor['answers'][question_index][answer]
                            
                            message_str = f':white_check_mark: {client.get_user(uid).mention} Question **#{question_index}** correct! {celebration_emote}'
                            message_str += f'\n**{num_correct}/{num_answered}/{num_questions}**.'
                            await message.channel.send(message_str)
                    # If answered incorrectly, store answer in array of incorrect answers
                    else:
                        # If the person actually answered the manual question
                        if answer != None:
                            
                            # Find the right answer in _question_storage.json, set it to the correct index
                            # Substring to remove number and accurately compare stored question
                            actual_answer_str = answers[answer]
                            actual_answer_str = actual_answer_str[1:len(actual_answer_str)]
                            
                            answer = get_correct_answer_index(qstor, actual_answer_str, question_index)
                            
                            # If the function: get_correct_answer_index() returns None, due to no matching answer found 
                            if answer == None:
                                error_str = f'> :no_entry: {client.get_user(uid).mention} Something has gone **terribly wrong** with the `Karuta` and `_question_storage.json` answer comparison tests. '
                                error_str += f'\n> Please contact bot developer. {client.get_user(admin_whitelist[2]).mention}'
                                error_str += f'\n`{question}` \n#{question_index} \n{answers} \n{character}'
                                await message.channel.send(error_str)
                                return None
                            
                            # If there have already been past answers,
                            # And it isnt a duplicate of any past incorrect answer
                            # Set the answer to include the most recent incorrect answer
                            
                            # If there are previous incorrect answers in an array already,
                            if isinstance(char_file['answers'][question_index], list) == True:
                                if not answer in char_file['answers'][question_index]:
                                    char_file['answers'][question_index].append(answer)
                            # If there was no entry / If the answer was correct, but upon double-check it is proven false
                            elif char_file['answers'][question_index] == None or char_file['answers'][question_index].isdigit():
                                # Change "None" to an array of wrong answers
                                char_file['answers'][question_index] = [answer]
                            
                            # Set the 'correct?' status to false
                            char_file['correct?'][question_index] = False
                            write_json(char_file, char_file_path)
                            answer = qstor['answers'][question_index][answer]
                            await message.channel.send(f':no_entry: {client.get_user(uid).mention} #**{question_index}** \nCharacter: `{char}` Answer: `{answer}`')
                        # If the person did not answer the manual question, and got it wrong
                        # else:
                            # await message.channel.send(f':no_entry: {client.get_user(uid).mention} You got the question wrong, and you **did not answer** the `Manual Question`.')
                # elif answered_question_entry == False:
                #     print('> comment 3: here is where i would put an incorrect koibito question checker. but no')
                    # await message.channel.send(f'> :no_entry: Question was answered incorrectly. \n> There was no manual question to answer. \nDid you answer incorrectly? Did Bot mistake the correct answer? \n\n*Please dm for any problem :pray:*')


# for work reminder, karuta work message edited
@client.event
async def on_message_edit(before, after):
    # karuta work reminder message checker part 2
    message = after
    
    # if there are any work messages, and message edited is the work message
    if message.author.id == 646937666251915264:
        # Check msg for work reminder
        # if message.guild.id == karuta_server_id and len(work_messages) > 0 and message.id in work_messages:
        
        if len(work_messages) > 0 and message.id in work_messages:
            wr_file = open_json(work_reminder_file)
            if str(message.guild.id) in wr_file: 
                work_messages.remove(message.id)
                await karuta_injury_check(message)
        
        # koibito check, visit char embed title
        await koibito_check(message, before)
        
        

@client.event 
async def on_message(message):
    # every message, check for karuta work reminder
    await karuta_injury_setup(message)
    
    # koibito check
    if message.author.id == 646937666251915264:
        await koibito_check(message)
    
    # egg reminder (outdated event)
    # await egg_claimed(message)
    await client.process_commands(message)
      

@client.event
async def on_ready():
    print('Mai Sakurajima Bot is  <online>\n')
    
    # time loop beginning for work reminder
    init_time_loop()
    await client.change_presence(activity=discord.Game(f'Ara Ara~ :heart:'))

client.run('<insert_bot_token_here>')
