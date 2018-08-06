import discord
from discord.ext import commands
import asyncio
import time
import platform

TOKEN = "NDc1ODQ4NzQ0NzY0NDQwNTc2.DklCJA.Pa5XVHX8gnAGRhyx4HGXv6nJnnA"

Client = discord.Client()
client = commands.Bot(command_prefix = ">")



@client.event
async def on_ready() :
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}' . format(discord.__version__, platform.python_version()))
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
            title = 'Welcome to JANJAN Bot',
            description = '**>addchar** - Add characters to the databse (Requires Moderator Permissions) \n\
**>char** - View a character using their char id. \n\
**>charid** - Find the id of a character.',
            colour = discord.Color.orange()
            )
        helpembed.set_footer(text='If you have any queries ping @Blaz#7282')

        await client.send_message(message.channel, embed=helpembed)

    ###ADD CHARACTERS mod role id :474557125977178112 admin role id:469766370159099904
    if message.content.upper() == ">ADDCHAR":
        if "474557125977178112" or "469766370159099904" in [role.id for role in message.author.roles]:
            addcharembed = discord.Embed(
                title = 'Add a Character',
                description = ' **Enter the values in the following order:** \n\
Image Link, Name, Lvl, Atk, Def,Combo Count, Jump Count, Dash Count, Strong Attack, Char number in logs \n\
\n **Eg:** ``https://i.imgur.com/7gKVRAP.png, naruto uzumaki, 50, 30, 20, 10, 10, 10, 20, 001`` ',
                colour = discord.Colour.orange()
                )
            
            
            await client.send_message(message.channel, embed=addcharembed)
                         
            response = await client.wait_for_message(author=message.author, timeout=30) #wait for response

            try:
                args = response.content.split(", ") #split response
                if len(args) != 10 or args == None:
                               await client.send_message(message.channel, "You have not passed the right parameters")
                else: 
                    img = args[0]
                    name = args[1]
                    lvl = int(float(args[2]))
                    atk = int(float(args[3]))
                    dfnc = int(float(args[4]))
                    cmb = int(float(args[5]))
                    jmp = int(float(args[6]))
                    dsh = int(float(args[7]))
                    satk = int(float(args[8]))
                    charnum = int(float(args[9]))
            
        #append Character List File   
                charalistfile = open('charlist.txt', 'at')
                charalistfile.write(("%d, %s, %s, %d, %d, %d, %d, %d, %d, %d, \n---\n")% (charnum, img, name, lvl, atk, dfnc, cmb, jmp, dsh, satk))
                charalistfile.close()

                charIDfile = open('charID.txt', 'at')
                charIDfile.write(("%03d. %s\n") % (charnum, name.upper()))
                charIDfile.close()

        #Preview in discord

                dispcharembed = discord.Embed(
                title = '%s' % (name.upper()),
                colour = discord.Colour.orange()
                )
                dispcharembed.set_thumbnail(url='%s' % (img))
                dispcharembed.add_field(name='LVL', value='%d'%(lvl), inline=False)
                dispcharembed.add_field(name='ATK', value='%d'%(atk), inline=True)
                dispcharembed.add_field(name='DEF', value='%d'%(dfnc), inline=True)
                dispcharembed.add_field(name='CMB Count', value='%d'%(cmb), inline=False)
                dispcharembed.add_field(name='JMP Count', value='%d'%(jmp), inline=True)
                dispcharembed.add_field(name='Dash', value='%d'%(dsh), inline=True)
                dispcharembed.add_field(name='Strong ATK', value='%d'%(satk), inline=False)
                dispcharembed.set_footer(text='No: %03d' % (charnum))

                await client.send_message(message.channel,embed=dispcharembed)
            except AttributeError:
                await client.send_message(message.channel, "<@%s> Your request has timed out." %(userID))
                        
        else:
            await client.send_message(message.channel, "**You do not have the permissions required to use this command**")
    ###END ADD CHARS

    ###REQUEST CHARS
    if message.content.upper() == ">CHAR":
                #ask user to type the number
        charembed = discord.Embed(
            title = 'View a character',
            description = 'Enter the ID of the character you would like to view. \n\
If you do not know their id, type ``>charidlist`` to pull up a list of characters and their ID',
            colour = discord.Colour.orange()
            )

        
        await client.send_message(message.channel, embed=charembed)

                
                #wait for response
        response = await client.wait_for_message(author=message.author, timeout=10)

        try: #check if input is a number
            charnum = int(float(response.content))       
            if charnum > 0:
                charalistloaded = open('charlist.txt', 'rt')
                try:
                #after response                
                    charchunk = charalistloaded.read().split("---\n")
                    args = charchunk[charnum - 2].split(", ")
                    charnum = int(float(args[0]))                
                    img = args[1]
                    name = args[2]
                    lvl = int(float(args[3]))
                    atk = int(float(args[4]))
                    dfnc = int(float(args[5]))
                    cmb = int(float(args[6]))
                    jmp = int(float(args[7]))
                    dsh = int(float(args[8]))
                    satk = int(float(args[9]))

                    dispcharembed = discord.Embed(
                    title = '%s' % (name.upper()),
                    colour = discord.Colour.orange()
                    )   
                    dispcharembed.set_thumbnail(url='%s' % (img))
                    dispcharembed.add_field(name='LVL', value='%d'%(lvl), inline=True)
                    dispcharembed.add_field(name='ATK', value='%d'%(atk), inline=True)
                    dispcharembed.add_field(name='DEF', value='%d'%(dfnc), inline=False)
                    dispcharembed.add_field(name='CMB Count', value='%d'%(cmb), inline=True)
                    dispcharembed.add_field(name='JMP Count', value='%d'%(jmp), inline=True)
                    dispcharembed.add_field(name='Dash', value='%d'%(dsh), inline=False)
                    dispcharembed.add_field(name='Strong ATK', value='%d'%(satk), inline=True)
                    dispcharembed.set_footer(text='No: %03d' % (charnum))
    
                    await client.send_message(message.channel,embed=dispcharembed)

                
                except IndexError:
                    await client.send_message(message.channel, "That value doesnt exist in the databse")
                
            else:
                await client.send_message(message.channel, "**<@%s> Please enter a valid character ID**" % (userID))
        except ValueError:
            await client.send_message(message.channel, "<@%s> You have entered an invalid char ID" % (userID))
        except AttributeError:
            await client.send_message(message.channel, "<@%s> The command has timed out" % (userID))
                               
    ###REQUEST CHARS EN
    
    ###Character ID List
    if message.content.upper() == ">CHARIDLIST":
         charIDfile = open('charID.txt', 'rt')
         idlistembed = discord.Embed(
             title = 'Character ID List',
             description = '%s' % (charIDfile.read()),
             colour = discord.Colour.orange()
             )

         await client.send_message(message.channel, embed = idlistembed)
         

           
       

client.run(TOKEN)
