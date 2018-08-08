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

####error loggig
#logging.basicConfig(filename='.\console.log', filemode='w', level=logging.INFO, format='%(asctime)s:%(levelname)s:%
#(message)s')
#@client.event
#async def on_error(event, *args, **kwargs):
#    message = args[0] #Gets the message object
#    logging.warning(traceback.format_exc()) #logs the error
#    await client.send_message(message.channel, "You caused an error!") #send the message to the channel
####error logging


@client.event
async def on_ready() :
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+
          ' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}' . format(discord.__version__,
                                                                                 platform.python_version()))
    print('--------')
    print('Created by Blaz#7282')

@client.event
async def on_message(message):
    userID = message.author.id
    
    if message.content.upper() == "PEACH":
        await client.send_message(message.channel, ":peach:")

    ###COMMAND LIST
    if message.content.upper() == ">HELP":

        helpembed = discord.Embed(
            title = 'Welcome to JumpStadium Bot',
            description = '**>addchar** - Add characters to the databse (Requires Moderator Permissions) \n\
**>char** - View a character using their char id. \n\
**>charid** - Find the id of a character.',
            colour = discord.Color.orange()
            )
        helpembed.set_footer(text='If you have any queries ping @Blaz#7282')

        await client.send_message(message.channel, embed=helpembed)

    ### ADD CHARACTERS mod role id :474557125977178112 admin role id:469766370159099904
    if message.content.upper() == ">ADDCHAR":
        if "474557125977178112" or "469766370159099904" in [role.id for role in message.author.roles]:
            addcharembed = discord.Embed(
                title = 'Add a Character',
                description = ' **Enter the values in the following order:** \n\
Image Link, Name, Lvl, Atk, Def,Hit Combo, Jump Count, Dash, Charge\n\
\n **Eg:** ``https://i.imgur.com/7gKVRAP.png, naruto uzumaki, 50, 30, 20, 1/5, 1/3, yes, no, naruto shippuden`` ',
                colour = discord.Colour.orange()
                )

            await client.send_message(message.channel, embed=addcharembed)
                         
            response = await client.wait_for_message(author=message.author, timeout=30) #wait for response

            try:
                args = response.content.split(", ") #split response
                if len(args) != 10 or args is None:
                               await client.send_message(message.channel, "You have not passed the right parameters")
                else: 
                    img = args[0]
                    name = args[1]
                    lvl = int(float(args[2]))
                    atk = int(float(args[3]))
                    dfnc = int(float(args[4]))
                    cmb = args[5]
                    jmp = args[6]
                    dsh = args[7]
                    chrg = args[8]
                    series = args[9]
   
        # get number of chars already in list
                    charalistfile = open('charlist.txt', 'r+')
                    charline = charalistfile.read().split("\n")
                    numchar  = len(charline)
        # append Character List File
                    charalistfile.write("%d, %s, %s, %d, %d, %d, %s, %s, %s, %s, %s \n"% (numchar, img, name, lvl,
                                                                                            atk, dfnc, cmb, jmp, dsh,
                                                                                            chrg, series))
                    charalistfile.close()
        # add char names to char id list
                    charIDfile = open('charID.txt', 'at')
                    charIDfile.write(("%03d. %s\n") % (numchar, name.upper()))
                    charIDfile.close()

        # Preview in discord
                    dispcharembed = discord.Embed(
                    title = '%s' % (name.upper()),
                    colour = discord.Colour.orange()
                    )
                    dispcharembed.set_thumbnail(url='%s' % (img))
                    dispcharembed.add_field(name='LVL', value='%d'%(lvl), inline=False)
                    dispcharembed.add_field(name='ATK', value='%d'%(atk), inline=True)
                    dispcharembed.add_field(name='DEF', value='%d'%(dfnc), inline=True)
                    dispcharembed.add_field(name='CMB Count', value='%s'%(cmb), inline=False)
                    dispcharembed.add_field(name='JMP Count', value='%s'%(jmp), inline=True)
                    dispcharembed.add_field(name='Dash', value='%s'%(dsh), inline=True)
                    dispcharembed.add_field(name='Charge', value='%s'%(chrg), inline=False)
                    dispcharembed.add_field(name='Series', value='%s' % (series), inline=True)
                    dispcharembed.set_footer(text='No: %03d' % (numchar))

                    await client.send_message(message.channel, embed=dispcharembed)
            except AttributeError:
                await client.send_message(message.channel, "<@%s> Your request has timed out." %(userID))
                        
        else:
            await client.send_message(message.channel, "**You do not have the permissions required to use this "
                                                       "command**")
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
                    # dispcharembed = printchar(int(float(args[0])), args[1], args[2], int(float(args[3])),
                    #                                               int(float(args[4])), int(float(args[5])), args[6], args[7], args[8],
                    #                                               args[9], args[10])


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
        if "475589371773452288" or "474557125977178112" or "469766370159099904" \
                in [role.id for role in message.author.roles]:

            delcharembed = discord.Embed(
                title='Delete a Character from the Database',
                description='Enter the ID of the character you would like to delete.',
                color=discord.Colour.orange()
            )
            delcharembed.set_footer(text='This action cannot be undone')
            await client.send_message(message.channel, embed=delcharembed)

            response = await client.wait_for_message(author=message.author, timeout=15)
            charid = int(float(response.content))

            yesornoembed = discord.Embed(
                title='Deletion Cofirmation',
                description='Are you sure you want to delete **Character No.%3d**? \n\n Type(y/n)' % charid
                )
            await client.send_message(message.channel, embed=yesornoembed)

            yesorno = await client.wait_for_message(author=message.author, timeout=10)

            if yesorno.content.upper() == "Y":
                charalistfile = open('charlist.txt', 'r+')
                charline = charalistfile.read().split("\n")
                charalistfile.close()
                charalistfile = open('charlist.txt', 'w')

                charidfile = open('charID.txt', 'w')

                if charid > 0 & charid < len(charline):
                    charline.pop(charid - 1)

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
                        charalistfile.write("%3d, %s, %s, %d, %d, %d, %s, %s, %s, %s, %s, \n" % (numchar, img, name, lvl,
                                                                                            atk, dfnc, cmb, jmp, dsh,
                                                                                            chrg, series))
                        charidfile.write("%3d. %s \n" % (numchar, name))

                else:
                    await client.send_messge(message.channel, "You have entered an invalid ID")
                charalistfile.close()
                charidfile.close()
            else:
                client.send_message(message.channel, "No character was deleted")
        else:
            await client.send_message(message.channel, "You do not have the permissions required to use that command.")


client.run(TOKEN)

###Looking for a way to have a common printembed method and calll it whenever chardata needs to be printed
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


client.run(TOKEN)
