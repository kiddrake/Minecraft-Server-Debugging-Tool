import discord
from discord.ext import commands, tasks
from pathlib import Path
import re
import asyncio
import os

client = commands.Bot(command_prefix = "$")
client.remove_command('help')
client.last_rank_up = None

client.server_log_dir_dict = {'survival': r'C:\Users\Administrator\Desktop\CardboardCraft\Survival\logs\latest.log',
                              'creative': r'C:\Users\Administrator\Desktop\CardboardCraft\Creative\logs\latest.log',
                              'minigame': r'C:\Users\Administrator\Desktop\CardboardCraft\Minigames\logs\latest.log',
                              'minigames': r'C:\Users\Administrator\Desktop\CardboardCraft\Minigames\logs\latest.log',
                              'skyblock': r'C:\Users\Administrator\Desktop\CardboardCraft\Skyblock\logs\latest.log',
                              'hub': r'C:\Users\Administrator\Desktop\CardboardCraft\Hub\logs\latest.log',
                              'build': r'C:\Users\Administrator\Desktop\CardboardCraft\Build Server\logs\latest.log',
                              'proxy': r'Z:\Proxy\proxy.log.0'}

client.server_command_txt_file_dict = {'survival': r'C:\Users\Administrator\Desktop\CardboardCraft\Survival\plugins\DiscordCommands\cmd.txt',
                                       'creative': r'C:\Users\Administrator\Desktop\CardboardCraft\Creative\plugins\DiscordCommands\cmd.txt',
                                       'minigame': r'C:\Users\Administrator\Desktop\CardboardCraft\Minigames\plugins\DiscordCommands\cmd.txt',
                                       'minigames': r'C:\Users\Administrator\Desktop\CardboardCraft\Minigames\plugins\DiscordCommands\cmd.txt',
                                       'skyblock': r'C:\Users\Administrator\Desktop\CardboardCraft\Skyblock\plugins\DiscordCommands\cmd.txt',
                                       'hub': r'C:\Users\Administrator\Desktop\CardboardCraft\Hub\plugins\DiscordCommands\cmd.txt',
                                       'build': r'C:\Users\Administrator\Desktop\CardboardCraft\Build Server\plugins\DiscordCommands\cmd.txt'}

client.status_element = ["Uptime", "TPS", "Free Memory", "Chunks Loaded", "Entities", "Allocated Memory"]

#status dict element: uptime, tps, free memory, chunks loaded, entities, allocated memory, status, log file path

client.server_status_dict = {'survival': ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 'Offline', r'C:\Users\Administrator\Desktop\CardboardCraft\Survival\logs\latest.log'],
                             'creative': ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 'Offline', r'C:\Users\Administrator\Desktop\CardboardCraft\Creative\logs\latest.log'],
                             'minigame': ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 'Offline', r'C:\Users\Administrator\Desktop\CardboardCraft\Minigames\logs\latest.log'],
                             'skyblock': ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 'Offline', r'C:\Users\Administrator\Desktop\CardboardCraft\Skyblock\logs\latest.log'],
                             'hub': ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 'Offline', r'C:\Users\Administrator\Desktop\CardboardCraft\Hub\logs\latest.log'],
                             'build': ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", 'Offline', r'C:\Users\Administrator\Desktop\CardboardCraft\Build Server\logs\latest.log']}

client.server_batch_file_dict = {'survival': r'C:\Users\Administrator\Desktop\CardboardCraft\Survival\start.bat',
                                 'creative': r'C:\Users\Administrator\Desktop\CardboardCraft\Creative\start.bat',
                                 'minigame': r'C:\Users\Administrator\Desktop\CardboardCraft\Minigames\start.bat',
                                 'skyblock': r'C:\Users\Administrator\Desktop\CardboardCraft\Skyblock\start.bat',
                                 'hub': r'C:\Users\Administrator\Desktop\CardboardCraft\Hub\start.bat',
                                 'build': r'C:\Users\Administrator\Desktop\CardboardCraft\Build Server\start.bat'}

def return_embed_color(status):
    if status == "Online":
        return 0x33FF33
    elif status == "Offline":
        return 0xFF3333

def all_lowercase(text):
    for f in re.findall("[A-Z]", text):
        text = text.replace(f, f.lower())
    return text

def slice_per(source, step):
    for i in range(0, len(source), step):
        yield source[i:i + step]

def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def replace_section_sign(line):
    return re.sub(".", "", line)

def get_timestamp(log):
    return re.findall("\[\d{2}:\d{2}:\d{2}\]", escape_ansi(log))[0]

def get_uptime(log):
    original = re.search("Uptime: (.+)", escape_ansi(log)).group(1)
    original = re.sub("day[s]?", 'd', original)
    original = re.sub("hour[s]?", 'hr', original)
    original = re.sub("minute[s]?", "min", original)
    original = re.sub("second[s]?", "sec", original)
    return original

def get_TPS(log):
    return re.search("Current TPS = (\d+)", escape_ansi(log)).group(1)

def get_allocated_memory(log):
    return re.search("Allocated memory: (.{3,5} MB)", escape_ansi(log)).group(1)

def get_free_memory(log):
    return re.search("Free memory: (.{3,5} MB)", escape_ansi(log)).group(1)

def get_chunks(log):
    return re.sub(r',', '', re.search('": (.{1,5}) chunks,', escape_ansi(log)).group(1))

def get_entities(log):
    return re.sub(r',', '', re.search("chunks, (.{1,5}) entities,", escape_ansi(log)).group(1))

@client.event
async def on_ready():
    print("MC Bot online")
    client.survival_status_message = await client.get_channel(783573003559632906).send("Survival Server Placeholder")
    await client.survival_status_message.add_reaction('<:grass_block:783039337896869888>')
    client.creative_status_message = await client.get_channel(783573003559632906).send("Creative Server Placeholder")
    await client.creative_status_message.add_reaction('<:grass_block:783039337896869888>')
    client.minigame_status_message = await client.get_channel(783573003559632906).send("Minigame Server Placeholder")
    await client.minigame_status_message.add_reaction('<:grass_block:783039337896869888>')
    client.skyblock_status_message = await client.get_channel(783573003559632906).send("Skyblock Server Placeholder")
    await client.skyblock_status_message.add_reaction('<:grass_block:783039337896869888>')
    client.hub_status_message = await client.get_channel(783573003559632906).send("Hub Server Placeholder")
    await client.hub_status_message.add_reaction('<:grass_block:783039337896869888>')
    client.build_status_message = await client.get_channel(783573003559632906).send("Build Server Placeholder")
    await client.build_status_message.add_reaction('<:grass_block:783039337896869888>')
    print("Status Messages Sent")
    client.loop.create_task(server_status())
    print("Server Status Updater Initiated")
    client.loop.create_task(level_up_message())
    print("Level Up Message Background Task Initiated")

async def level_up_message():
    while True:
        with open(Path(r'Z:\Proxy\proxy.log.0'), 'r') as file:
            last_messages = file.readlines()[-10:]
            for log in last_messages:
                if 'has ranked up to' and 'CardboardCraft' in log:
                    if log == client.last_rank_up or "kicked" in log:
                        pass
                    else:
                        try:
                            player_name = re.search("[CardboardCraft] (.*?) has ranked up to (.+)", replace_section_sign(escape_ansi(log))).group(1)
                            rank = re.sub('[^a-zA-Z]+', '', re.search("[CardboardCraft] (.*?) has ranked up to (.+)", replace_section_sign(escape_ansi(log))).group(2))
                        except:
                            print(f"Had some trouble wit {log}")
                        main_channel = client.get_channel(695925991599505421)
                        await main_channel.send(f"Congratulations to {player_name} for ranking up to {rank}!")
                        client.last_rank_up = log
            file.close()
        await asyncio.sleep(5)

async def server_status():
    while True:
        uptime_command_index = 0
        for server_type in client.server_status_dict:
            with open(Path(client.server_status_dict[server_type][7])) as log_file_fileobject:
                log_file = log_file_fileobject.readlines()
                if server_type == "survival":
                    for log in log_file[-60:]:
                        if r"CONSOLE issued server command: /uptime" in log:
                            uptime_command_index = log_file.index(log)
                            content = log_file[uptime_command_index:uptime_command_index+9]
                            for i in content:
                                print(escape_ansi(i))
                            client.server_status_dict[server_type][0] = get_uptime(log_file[uptime_command_index + 1])
                            client.server_status_dict[server_type][1] = get_TPS(log_file[uptime_command_index + 2])
                            client.server_status_dict[server_type][2] = get_free_memory(log_file[uptime_command_index + 5])
                            client.server_status_dict[server_type][3] = int(get_chunks(log_file[uptime_command_index + 6])) + int(get_chunks(log_file[uptime_command_index + 7])) + int(get_chunks(log_file[uptime_command_index + 8]))
                            client.server_status_dict[server_type][4] = int(get_entities(log_file[uptime_command_index + 6])) + int(get_entities(log_file[uptime_command_index + 7])) + int(get_entities(log_file[uptime_command_index + 8]))
                            client.server_status_dict[server_type][5] = get_allocated_memory(log_file[uptime_command_index + 4])
                            client.server_status_dict[server_type][6] = "Online"
                        elif "[WorldEdit] Disabling WorldEdit" in log:
                            client.server_status_dict[server_type][0] = "N/A"
                            client.server_status_dict[server_type][1] = "N/A"
                            client.server_status_dict[server_type][2] = "N/A"
                            client.server_status_dict[server_type][3] = "N/A"
                            client.server_status_dict[server_type][4] = "N/A"
                            client.server_status_dict[server_type][5] = "N/A"
                            client.server_status_dict[server_type][6] = "Offline"
                            break
                elif server_type == "creative":
                    for log in log_file[-60:]:
                        if r"CONSOLE issued server command: /uptime" in log:
                            uptime_command_index = log_file.index(log)
                            content = log_file[uptime_command_index:uptime_command_index+10]
                            for i in content:
                                print(escape_ansi(i))
                            client.server_status_dict[server_type][0] = get_uptime(log_file[uptime_command_index + 1])
                            client.server_status_dict[server_type][1] = get_TPS(log_file[uptime_command_index + 2])
                            client.server_status_dict[server_type][2] = get_free_memory(log_file[uptime_command_index + 5])
                            client.server_status_dict[server_type][3] = int(get_chunks(log_file[uptime_command_index + 10]))
                            client.server_status_dict[server_type][4] = int(get_entities(log_file[uptime_command_index + 10]))
                            client.server_status_dict[server_type][5] = get_allocated_memory(log_file[uptime_command_index + 4])
                            client.server_status_dict[server_type][6] = "Online"
                        elif "[WorldEdit] Disabling WorldEdit" in log:
                            client.server_status_dict[server_type][0] = "N/A"
                            client.server_status_dict[server_type][1] = "N/A"
                            client.server_status_dict[server_type][2] = "N/A"
                            client.server_status_dict[server_type][3] = "N/A"
                            client.server_status_dict[server_type][4] = "N/A"
                            client.server_status_dict[server_type][5] = "N/A"
                            client.server_status_dict[server_type][6] = "Offline"
                            break
                elif server_type == "minigame":
                    for log in log_file[-100:]:
                        if r"CONSOLE issued server command: /uptime" in log:
                            uptime_command_index = log_file.index(log)
                            content = log_file[uptime_command_index:uptime_command_index+12]
                            for i in content:
                                print(escape_ansi(i))
                            client.server_status_dict[server_type][0] = get_uptime(log_file[uptime_command_index + 1])
                            client.server_status_dict[server_type][1] = get_TPS(log_file[uptime_command_index + 2])
                            client.server_status_dict[server_type][2] = get_free_memory(log_file[uptime_command_index + 5])
                            client.server_status_dict[server_type][3] = int(get_chunks(log_file[uptime_command_index + 6])) + int(get_chunks(log_file[uptime_command_index + 7])) + int(get_chunks(log_file[uptime_command_index + 8])) + int(get_chunks(log_file[uptime_command_index + 9])) + int(get_chunks(log_file[uptime_command_index + 10])) + int(get_chunks(log_file[uptime_command_index + 11])) + int(get_chunks(log_file[uptime_command_index + 12]))
                            client.server_status_dict[server_type][4] = int(get_entities(log_file[uptime_command_index + 6])) + int(get_entities(log_file[uptime_command_index + 7])) + int(get_entities(log_file[uptime_command_index + 8])) + int(get_entities(log_file[uptime_command_index + 9])) + int(get_entities(log_file[uptime_command_index + 10])) + int(get_entities(log_file[uptime_command_index + 11])) + int(get_entities(log_file[uptime_command_index + 12]))
                            client.server_status_dict[server_type][5] = get_allocated_memory(log_file[uptime_command_index + 4])
                            client.server_status_dict[server_type][6] = "Online"
                        elif "[WorldEdit] Disabling WorldEdit" in log:
                            client.server_status_dict[server_type][0] = "N/A"
                            client.server_status_dict[server_type][1] = "N/A"
                            client.server_status_dict[server_type][2] = "N/A"
                            client.server_status_dict[server_type][3] = "N/A"
                            client.server_status_dict[server_type][4] = "N/A"
                            client.server_status_dict[server_type][5] = "N/A"
                            client.server_status_dict[server_type][6] = "Offline"
                            break
                elif server_type == "skyblock":
                    for log in log_file[-200:]:
                        if r"CONSOLE issued server command: /uptime" in log:
                            uptime_command_index = log_file.index(log)
                            content = log_file[uptime_command_index:uptime_command_index+12]
                            for i in content:
                                print(escape_ansi(i))
                            client.server_status_dict[server_type][0] = get_uptime(log_file[uptime_command_index + 1])
                            client.server_status_dict[server_type][1] = get_TPS(log_file[uptime_command_index + 2])
                            client.server_status_dict[server_type][2] = get_free_memory(log_file[uptime_command_index + 5])
                            client.server_status_dict[server_type][3] = int(get_chunks(log_file[uptime_command_index + 6])) + int(get_chunks(log_file[uptime_command_index + 7])) + int(get_chunks(log_file[uptime_command_index + 8])) + int(get_chunks(log_file[uptime_command_index + 9])) + int(get_chunks(log_file[uptime_command_index + 10])) + int(get_chunks(log_file[uptime_command_index + 11])) + int(get_chunks(log_file[uptime_command_index + 12]))
                            client.server_status_dict[server_type][4] = int(get_entities(log_file[uptime_command_index + 6])) + int(get_entities(log_file[uptime_command_index + 7])) + int(get_entities(log_file[uptime_command_index + 8])) + int(get_entities(log_file[uptime_command_index + 9])) + int(get_entities(log_file[uptime_command_index + 10])) + int(get_entities(log_file[uptime_command_index + 11])) + int(get_entities(log_file[uptime_command_index + 12]))
                            client.server_status_dict[server_type][5] = get_allocated_memory(log_file[uptime_command_index + 4])
                            client.server_status_dict[server_type][6] = "Online"
                        elif "[WorldEdit] Disabling WorldEdit" in log:
                            client.server_status_dict[server_type][0] = "N/A"
                            client.server_status_dict[server_type][1] = "N/A"
                            client.server_status_dict[server_type][2] = "N/A"
                            client.server_status_dict[server_type][3] = "N/A"
                            client.server_status_dict[server_type][4] = "N/A"
                            client.server_status_dict[server_type][5] = "N/A"
                            client.server_status_dict[server_type][6] = "Offline"
                            break
                elif server_type == "hub":
                    for log in log_file[-120:]:
                        if r"CONSOLE issued server command: /uptime" in log:
                            uptime_command_index = log_file.index(log)
                            content = log_file[uptime_command_index:uptime_command_index+6]
                            for i in content:
                                print(escape_ansi(i))
                            client.server_status_dict[server_type][0] = get_uptime(log_file[uptime_command_index + 1])
                            client.server_status_dict[server_type][1] = get_TPS(log_file[uptime_command_index + 2])
                            client.server_status_dict[server_type][2] = get_free_memory(log_file[uptime_command_index + 5])
                            client.server_status_dict[server_type][3] = int(get_chunks(log_file[uptime_command_index + 6]))
                            client.server_status_dict[server_type][4] = int(get_entities(log_file[uptime_command_index + 6]))
                            client.server_status_dict[server_type][5] = get_allocated_memory(log_file[uptime_command_index + 4])
                            client.server_status_dict[server_type][6] = "Online"
                        elif "[WorldEdit] Disabling WorldEdit" in log:
                            client.server_status_dict[server_type][0] = "N/A"
                            client.server_status_dict[server_type][1] = "N/A"
                            client.server_status_dict[server_type][2] = "N/A"
                            client.server_status_dict[server_type][3] = "N/A"
                            client.server_status_dict[server_type][4] = "N/A"
                            client.server_status_dict[server_type][5] = "N/A"
                            client.server_status_dict[server_type][6] = "Offline"
                            break
                elif server_type == "build":
                    for log in log_file[-150:]:
                        if r"CONSOLE issued server command: /uptime" in log:
                            uptime_command_index = log_file.index(log)
                            content = log_file[uptime_command_index:uptime_command_index+9]
                            for i in content:
                                print(escape_ansi(i))
                            client.server_status_dict[server_type][0] = get_uptime(log_file[uptime_command_index + 1])
                            client.server_status_dict[server_type][1] = get_TPS(log_file[uptime_command_index + 2])
                            client.server_status_dict[server_type][2] = get_free_memory(log_file[uptime_command_index + 5])
                            client.server_status_dict[server_type][3] = int(get_chunks(log_file[uptime_command_index + 6])) + int(get_chunks(log_file[uptime_command_index + 7])) + int(get_chunks(log_file[uptime_command_index + 8])) + int(get_chunks(log_file[uptime_command_index + 9]))
                            client.server_status_dict[server_type][4] = int(get_entities(log_file[uptime_command_index + 6])) + int(get_entities(log_file[uptime_command_index + 7])) + int(get_entities(log_file[uptime_command_index + 8])) + int(get_entities(log_file[uptime_command_index + 9]))
                            client.server_status_dict[server_type][5] = get_allocated_memory(log_file[uptime_command_index + 4])
                            client.server_status_dict[server_type][6] = "Online"
                        elif "[WorldEdit] Disabling WorldEdit" in log:
                            client.server_status_dict[server_type][0] = "N/A"
                            client.server_status_dict[server_type][1] = "N/A"
                            client.server_status_dict[server_type][2] = "N/A"
                            client.server_status_dict[server_type][3] = "N/A"
                            client.server_status_dict[server_type][4] = "N/A"
                            client.server_status_dict[server_type][5] = "N/A"
                            client.server_status_dict[server_type][6] = "Offline"
                            break
                log_file_fileobject.close()

        survival_embed = discord.Embed(title = "Survival Server", color = return_embed_color(client.server_status_dict["survival"][6]))
        for index in range(6):
            survival_embed.add_field(name = client.status_element[index], value = client.server_status_dict["survival"][index])
        survival_embed.set_footer(text = "React to this message with grassblock emoji to start/restart server")

        creative_embed = discord.Embed(title = "Creative Server", color = return_embed_color(client.server_status_dict["creative"][6]))
        for index in range(6):
            creative_embed.add_field(name = client.status_element[index], value = client.server_status_dict["creative"][index])
        creative_embed.set_footer(text = "React to this message with grassblock emoji to start/restart server")

        minigame_embed = discord.Embed(title = "Minigame Server", color = return_embed_color(client.server_status_dict["minigame"][6]))
        for index in range(6):
            minigame_embed.add_field(name = client.status_element[index], value = client.server_status_dict["minigame"][index])
        minigame_embed.set_footer(text = "React to this message with grassblock emoji to start/restart server")

        skyblock_embed = discord.Embed(title = "Skyblock Server", color = return_embed_color(client.server_status_dict["skyblock"][6]))
        for index in range(6):
            skyblock_embed.add_field(name = client.status_element[index], value = client.server_status_dict["skyblock"][index])
        skyblock_embed.set_footer(text = "React to this message with grassblock emoji to start/restart server")

        hub_embed = discord.Embed(title = "Hub Server", color = return_embed_color(client.server_status_dict["hub"][6]))
        for index in range(6):
            hub_embed.add_field(name = client.status_element[index], value = client.server_status_dict["hub"][index])
        hub_embed.set_footer(text = "React to this message with grassblock emoji to start/restart server")

        build_embed = discord.Embed(title = "Build Server", color = return_embed_color(client.server_status_dict["build"][6]))
        for index in range(6):
            build_embed.add_field(name = client.status_element[index], value = client.server_status_dict["build"][index])
        build_embed.set_footer(text = "React to this message with grassblock emoji to start/restart server")

        await client.survival_status_message.edit(content = None, embed = survival_embed)
        await client.creative_status_message.edit(content = None, embed = creative_embed)
        await client.minigame_status_message.edit(content = None, embed = minigame_embed)
        await client.skyblock_status_message.edit(content = None, embed = skyblock_embed)
        await client.hub_status_message.edit(content = None, embed = hub_embed)
        await client.build_status_message.edit(content = None, embed = build_embed)
        await asyncio.sleep(20)

@client.event
async def on_reaction_add(reaction, user):
    if user != client.user and reaction.message.channel == client.get_channel(783573003559632906) and reaction.emoji == client.get_emoji(783039337896869888):
        if client.server_status_dict[reaction.message.embeds[0].title.lower().split()[0]][6] == 'Online':

            cmd_file = open(Path(client.server_command_txt_file_dict[reaction.message.embeds[0].title.lower().split()[0]]), 'w')
            cmd_file.write('stop')
            cmd_file.close()
        else:
            os.startfile(client.server_batch_file_dict[reaction.message.embeds[0].title.lower().split()[0]])

@client.command(aliases = ['cmd', 'CMD', 'Cmd'])
async def server_command(ctx, server, *commands):
    if not ctx.channel.id == 780646254019477536:
        return
    final_message_list = []
    final_message = ''
    file_path = client.server_command_txt_file_dict[all_lowercase(server)]
    command = ''
    if len(commands) == 0:
        return
    elif len(commands) == 1:
        command = commands[0]
    elif len(commands) > 1:
        for word in commands:
            command += word + ' '
    cmd_file = open(Path(file_path), 'w')
    cmd_file.write(command.strip())
    cmd_file.close()
    await ctx.send(f'`{command.strip()}` command sent to {server} console!')
    await asyncio.sleep(0.5)
    with open(Path(client.server_log_dir_dict[server.lower()]), 'r') as file_object:
        file = file_object.readlines()
        command_log_position = -1
        for log in reversed(file):
            if "[DiscordCommands]" in log:
                break
            else:
                command_log_position -= 1
        timestamp = get_timestamp(file[command_log_position])
        for message in file[command_log_position:]:
            if timestamp in escape_ansi(message):
                final_message_list.append(escape_ansi(message))
        if len(final_message_list) <= 15:
            for message in final_message_list:
                final_message += escape_ansi(message)
            await ctx.send(f"```{final_message}```")
        else:
            sliced_list = slice_per(final_message_list, 10)
            for parsed_list in sliced_list:
                for message in parsed_list:
                    final_message += escape_ansi(message)
                await ctx.send(f"```{final_message}```")
                final_message = ''
        file_object.close()

@client.command(aliases = ['Log', 'log'])
async def server_log_search(ctx, server, traceback_log_count, *args):
    if not ctx.channel.id == 780646254019477536:
        return
    final_message_list = []
    final_message = ''
    await ctx.send(f"```Searching for {server.lower()} server log...```")
    with open(Path(client.server_log_dir_dict[server.lower()]), 'r') as file:
        if len(args) == 0:
            for line in (file.readlines() [-int(traceback_log_count):]):
                final_message_list.append(line)
            if len(final_message_list) <= 15:
                for message in final_message_list:
                    final_message += replace_section_sign(escape_ansi(message))
                await ctx.send(f"```{final_message}```")
            else:
                sliced_list = slice_per(final_message_list, 10)
                for parsed_list in sliced_list:
                    for message in parsed_list:
                        final_message += replace_section_sign(escape_ansi(message))
                    await ctx.send(f"```{final_message}```")
                    final_message = ''
        else:
            found = None
            for line in (file.readlines() [-int(traceback_log_count):]):
                bool_list = []
                for keyword in args:
                    bool_list.append(all_lowercase(keyword) in all_lowercase(line))
                if all(bool_list):
                    final_message_list.append(line)
                    found = True
            if not found:
                await ctx.send("```Nothing found!```")
            elif len(final_message_list) <= 15:
                for message in final_message_list:
                    final_message += replace_section_sign(escape_ansi(message))
                await ctx.send(f"```{final_message}```")
                await ctx.send("```Done!```")
            elif len(final_message_list) > 15:
                sliced_list = slice_per(final_message_list, 10)
                for parsed_list in sliced_list:
                    for message in parsed_list:
                        final_message += replace_section_sign(escape_ansi(message))
                    await ctx.send(f"```{final_message}```")
                    final_message = ''
                await ctx.send("```Done!```")
        file.close()

client.run('NzgwNTgyMjQxMjM5MTcxMDcy.X7xL3A.OGS2b_6lw-CeKeMnmSwXgpjkl9w')
