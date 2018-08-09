import discord
from discord.ext import commands
import asyncio
import time
import platform
import sys
import traceback
import logging


TOKEN = "NDc1ODQ4NzQ0NzY0NDQwNTc2.DklbWA.jvV1kJp5nMoXFsneLFeMiVuAWAI"

Client = discord.Client()
client = commands.Bot(command_prefix = ">")
ver = '0.0.1'

@client.event
async def on_ready() :
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+
          ' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}' . format(discord.__version__,
                                                                                 platform.python_version()))
    print('--------')
    print('Created by Blaz#7282')
    await client.change_presence(game=discord.Game(name='with papa Blaz'))

@client.event
async def on_message(message):
    userID = message.author.id


    
    if message.content.upper() == "PEACH":
        await client.send_message(message.channel, ":peach:")
    if message.content.upper() == ">INTROB":
        if message.author.id == "195418249066840064":
            introembed = discord.Embed(
                title = 'A Database Bot for Weekly Shonen Jump Jikkyou Janjan Stadium',
                colour = discord.Colour.orange()
            )
            introembed.set_footer(text='Made by Blaz@7282', icon_url='https://images-ext-1.discordapp.net/external/TEXswBM7gzqMF0loi9_u4HgDdNZv1lFrlVm1zwQSpq8/%3Fsize%3D128/https/cdn.discordapp.com/avatars/195418249066840064/5eca17c1c5adc5d050c7aac68f28f85f.png')
            introembed.add_field(name='Hey There!', value='You can get a list of commands by using the ``>help`` in #bot-spoom')
            introembed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/mLR3X7fbTpDqBc9KFPJW-5K9Z71bUHKis9j7GGPJFw4/%3Fsize%3D128/https/cdn.discordapp.com/avatars/475848744764440576/584ca55e541d488af038d3e3cfb90b1d.png')
            introembed.set_author(name='JumpStadium Bot', icon_url='https://images-ext-2.discordapp.net/external/mLR3X7fbTpDqBc9KFPJW-5K9Z71bUHKis9j7GGPJFw4/%3Fsize%3D128/https/cdn.discordapp.com/avatars/475848744764440576/584ca55e541d488af038d3e3cfb90b1d.png')
            introembed.add_field(name='---', value='ver: %s' % ver)
            await client.send_message(client.get_channel('469908961085227008'), embed = introembed)

    ### EXIT BOT
    if message.content.upper() == "+SHUTDOWN":
        if message.author.id == "195418249066840064":
            await client.logout()
        else:
            await client.send_message(message.channel, "Buzz Off :unamused:")

    ###COMMAND LIST
    if message.content.upper() == ">HELP":

        helpembed = discord.Embed(
            title = 'Welcome to JumpStadium Bot',
            description = '__***Command List***__ \n\n\
            **>addchar** - Add characters to the database (Requires Moderator Permissions) \n\
**>char** - View a character using their char id. \n\
**>charid** - Find the id of a character.',
            colour = discord.Color.orange()
            )
        helpembed.set_footer(text='If you have any queries ping @Blaz#7282')

        await client.send_message(message.channel, embed=helpembed)

    ### ADD CHARACTERS mod role id :474557125977178112 admin role id:469766370159099904
    if message.content.upper() == ">ADDCHAR":
        if "474557125977178112" in [role.id for role in message.author.roles] or "469766370159099904" \
                in [role.id for role in message.author.roles] or "475589371773452288" in \
                [role.id for role in message.author.roles]:
            addcharembed = discord.Embed(
                title='Add a Character',
                description=' **Enter the values in the following order:** \n\
Char no., Image Link, Name, Lvl, Atk, Def,Hit Combo, Jump Count, Dash, Charge\n\
\n **Eg:** ``037, https://i.imgur.com/7gKVRAP.png, TEST , 50, 30, 20, 1/5, 1/3, yes, no, TEST`` ',
                colour=discord.Colour.orange()
            )

            await client.send_message(message.channel, embed=addcharembed)

            response = await client.wait_for_message(author=message.author, timeout=30)  # wait for response

            try:
                resplist = response.content.split(", ")  # split response
                numchar = int(float(resplist[0]))

                if numchar > 0:
                    if len(resplist) != 11 or resplist is None:
                        await client.send_message(message.channel, "You have not passed the right parameters")
                    else:
                        charalistfile = open('charlist.txt', 'r+')
                        charline = charalistfile.read().split("\n")
                        charline.insert(numchar - 1, '%s' % response.content)
                        charalistfile.close()
                        charalistfile = open('charlist.txt', 'w')
                        charidfile = open('charID.txt', 'w')

                        for x in range(0, len(charline) - 1):
                            args = charline[x].split(", ")
                            charnum = x + 1
                            img = args[1]
                            name = args[2].upper()
                            lvl = int(float(args[3]))
                            atk = int(float(args[4]))
                            dfnc = int(float(args[5]))
                            cmb = args[6]
                            jmp = args[7]
                            dsh = args[8]
                            chrg = args[9]
                            series = args[10]
                            charalistfile.write(
                                "%03d, %s, %s, %d, %d, %d, %s, %s, %s, %s, %s, \n" % (charnum, img, name, lvl,
                                                                                      atk, dfnc, cmb, jmp, dsh,
                                                                                      chrg, series))
                            charidfile.write("%03d. %s \n" % (charnum, name))

                        charalistfile.close()
                        charidfile.close()

                        # Preview in discord
                        dispcharembed = discord.Embed(
                            title='%s' % (resplist[2].upper()),
                            colour=discord.Colour.orange()
                        )
                        dispcharembed.set_thumbnail(url='%s' % (resplist[1]))
                        dispcharembed.add_field(name='LVL', value='%d' % (int(float(resplist[3]))), inline=False)
                        dispcharembed.add_field(name='ATK', value='%d' % (int(float(resplist[4]))), inline=True)
                        dispcharembed.add_field(name='DEF', value='%d' % (int(float(resplist[5]))), inline=True)
                        dispcharembed.add_field(name='CMB Count', value='%s' % (resplist[6]), inline=False)
                        dispcharembed.add_field(name='JMP Count', value='%s' % (resplist[7]), inline=True)
                        dispcharembed.add_field(name='Dash', value='%s' % (resplist[8]), inline=True)
                        dispcharembed.add_field(name='Charge', value='%s' % (resplist[9]), inline=False)
                        dispcharembed.add_field(name='Series', value='%s' % (resplist[10]), inline=True)
                        dispcharembed.set_footer(text='No: %03d' % (numchar))

                        await client.send_message(message.channel, embed=dispcharembed)

                else:
                    await client.send_messge(message.channel, "You have entered an invalid ID")

            except AttributeError:
                await client.send_message(message.channel, "<@%s> Your request has timed out." % (userID))
            except ValueError:
                await client.send_message(message.channel, "You have not passed the right parameters")

        else:
            await client.send_message(message.channel, "*<@%s>You do not have the permissions required to use this "
                                                       "command :shrug:*" % userID)
    ###END ADD CHARS

    ###REQUEST CHARS
    if message.content.upper() == ">CHAR":
                # ask user to type the number
        charembed = discord.Embed(
            title = 'View a character',
            description = 'Enter the ID of the character you would like to view. \n\
If you do not know their id, type ``>charidlist`` to pull up a list of characters and their ID',
            colour = discord.Colour.orange()
            )

        await client.send_message(message.channel, embed=charembed)

                # wait for response
        response = await client.wait_for_message(author=message.author, timeout=10)
        try:  # check if input is a number
            numchar = int(float(response.content))
            if numchar > 0:
                charalistloaded = open('charlist.txt', 'rt')
                try:
                    # after response
                    charline = charalistloaded.read().split("\n")
                    args = charline[numchar - 1].split(", ")
                    numchar = int(float(args[0]))
                    img = args[1]
                    name = args[2]
                    lvl = int(float(args[3]))
                    atk = int(float(args[4]))
                    dfnc = int(float(args[5]))
                    cmb = args[6]
                    jmp = args[7]
                    dsh = args[8]
                    chrg = args[9]
                    series = args[10]

                    dispcharembed = discord.Embed(
                                title='%s' % (name.upper()),
                                colour=discord.Colour.orange()
                            )
                    dispcharembed.set_thumbnail(url='%s' % (img))
                    dispcharembed.add_field(name='LVL', value='%d' % (lvl), inline=True)
                    dispcharembed.add_field(name='ATK', value='%d' % (atk), inline=True)
                    dispcharembed.add_field(name='DEF', value='%d' % (dfnc), inline=False)
                    dispcharembed.add_field(name='CMB Count', value='%s' % (cmb), inline=True)
                    dispcharembed.add_field(name='JMP Count', value='%s' % (jmp), inline=True)
                    dispcharembed.add_field(name='Dash', value='%s' % (dsh), inline=False)
                    dispcharembed.add_field(name='Charge', value='%s' % (chrg), inline=True)
                    dispcharembed.add_field(name='Series', value='%s' % (series), inline=True)
                    dispcharembed.set_footer(text='No: %03d' % (numchar))

                    await client.send_message(message.channel, embed=dispcharembed)
                    
                except IndexError:
                    await client.send_message(message.channel, "That value doesnt exist in the databse")

            else:
                await client.send_message(message.channel, "<@%s> Please enter a valid character ID" % (userID))
        except ValueError:
            await client.send_message(message.channel, "<@%s> Please enter a valid character ID" % (userID))
        except AttributeError:
            await client.send_message(message.channel, "<@%s> The command has timed out" % (userID))
                               
    ###Character ID List
    if message.content.upper() == ">CHARIDLIST":
        charIDfile = open('charID.txt', 'rt')
        idlistembed = discord.Embed(
             title = 'Character ID List',
             description = '%s' % (charIDfile.read()),
             colour = discord.Colour.orange()
             )
        await client.send_message(message.channel, embed = idlistembed)
        charIDfile.close()

    ### Del Char - DO NOT USE xD
    if message.content.upper() == ">DELCHAR":
        if "474557125977178112" in [role.id for role in message.author.roles] or "469766370159099904" \
                in [role.id for role in message.author.roles] or "475589371773452288" in \
                [role.id for role in message.author.roles]:

            charalistfile = open('charlist.txt', 'r+')
            charline = charalistfile.read().split("\n")
            charalistfile.close()
            listlength = len(charline) - 1
            delcharembed = discord.Embed(
                title='Delete a Character from the Database',
                description='Enter the ID of the character you would like to delete.',
                color=discord.Colour.orange()
            )
            delcharembed.set_footer(text='This action cannot be undone')

            await client.send_message(message.channel, embed=delcharembed)

            response = await client.wait_for_message(author=message.author, timeout=15)
            try:
#                if int(float(response.content)) < (len(charline) - 1) & int(float(response.content)) > 0:

                    charid = int(float(response.content))
                    yesornoembed = discord.Embed(
                        title='Deletion Cofirmation',
                        description='Are you sure you want to delete **Character No.%3d**? \n\n Type(y/n)' % charid
                    )
                    await client.send_message(message.channel, embed=yesornoembed)

                    yesorno = await client.wait_for_message(author=message.author, timeout=10)
                    try:
                        if yesorno.content.upper() == "Y":

                            if charid > 0 & charid < listlength:
                                delchar = charline.pop(charid - 1).split(", ")
                                charalistfile = open('charlist.txt', 'w')
                                charidfile = open('charID.txt', 'w')

                                for x in range(0, len(charline) - 1):
                                    args = charline[x].split(", ")
                                    numchar = x + 1
                                    img = args[1]
                                    name = args[2]
                                    lvl = int(float(args[3]))
                                    atk = int(float(args[4]))
                                    dfnc = int(float(args[5]))
                                    cmb = args[6]
                                    jmp = args[7]
                                    dsh = args[8]
                                    chrg = args[9]
                                    series = args[10]
                                    charalistfile.write(
                                        "%03d, %s, %s, %d, %d, %d, %s, %s, %s, %s, %s, \n" % (numchar, img, name, lvl,
                                                                                              atk, dfnc, cmb, jmp, dsh,
                                                                                              chrg, series))
                                    charidfile.write("%03d. %s \n" % (numchar, name))

                                await client.send_message(message.channel,
                                                          "**The character: ``%03d. %s`` from ``%s`` has been deleted from the  "
                                                          "database :cry:**" % (
                                                          int(float(delchar[0])), delchar[2], delchar[10]))
                                charalistfile.close()
                                charidfile.close()

                            else:
                                await client.send_messge(message.channel, "You have entered an invalid ID")



                        else:
                            await client.send_message(message.channel, "No character was deleted")

                    except AttributeError:
                        await client.send_message(message.channel, "You have failed to confirm your character deletion "
                                                                   "request")
#                else:
#                    await client.send_message(message.channel, "The id you entered doesnt exist in the database. SMH")

            except AttributeError:
                await client.send_message(message.channel, "No character was deleted. Bot timed Out")
            except ValueError:
                await client.send_message(message.channel, "You have entered an invalid ID")


        else:
            await client.send_message(message.channel,
                                      "You do not have the permissions required to use that command.")


client.run(TOKEN)


def printchar(numchar, img, name, lvl, atk, dfnc, cmb, jmp, dsh, chrg, series, ):

    dispcharembed = discord.Embed(
        title='%s' % (name.upper()),
        colour=discord.Colour.orange()
    )
    dispcharembed.set_thumbnail(url='%s' % (img))
    dispcharembed.add_field(name='LVL', value='%d' % (int(float(lvl))), inline=True)
    dispcharembed.add_field(name='ATK', value='%d' % (int(float(atk))), inline=True)
    dispcharembed.add_field(name='DEF', value='%d' % (int(float(dfnc))), inline=False)
    dispcharembed.add_field(name='CMB Count', value='%s' % (cmb), inline=True)
    dispcharembed.add_field(name='JMP Count', value='%s' % (jmp), inline=True)
    dispcharembed.add_field(name='Dash', value='%s' % (dsh), inline=False)
    dispcharembed.add_field(name='Charge', value='%s' % (chrg), inline=True)
    dispcharembed.add_field(name='Series', value='%s' % (series), inline=True)
    dispcharembed.set_footer(text='No: %03d' % (int(float(numchar))))

    return dispcharembed
