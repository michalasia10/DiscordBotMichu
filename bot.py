import discord
from discord import Member, Status, Embed, Color
import schedule
from random import choice
import time
intents = discord.Intents.all()
# client = commands.Bot(command_prefix='!')
client = discord.Client(intents=intents)

UWAGI = {
    'starostka': {
        "online": [" jest starostką, przyszła nam tutaj poszefowac także uwaga!"],
        "ofline": [" uwaga już sobie poszła szefowa można sie opierdalać!"]
    },
    'szefy': {
        "online": [" a kto to tu przyszedł? Pan szefu niszczyciel dobrej zabawy!"],
        "ofline": [" już wielki szef poszedł można go obsmarować :D"]
    },
    'geoinformatyk': {
        "online": [" przyszedł pan ważniak i będzie udawał że umie w GIS."],
        "ofline": [" poszedł już wielki pan geoinfromatyk."]
    },
    "streamer":
        {
            "online": [" przyszedł nasz ulubiony pato streamer :D"],
            "ofline": [" poszedł już chowajcie już tą wóde!"]},
    'impostor': {
        "online": [" przyszedł jakiś tajny szpieg."],
        "ofline": [" uciekł możecie spokojnie rozmawiać."]
    },
}

PLAN = {
           "Poniedziałek": "Laba / Ewentualnie Rachunek",
           "Wtorek": "10:15-12:00 WYKłAD - TELEDETEKCJA,\n 12:15-14:00  ĆWICZENIA - TELEDETEKCJA",
           "Środa":"9:15-11:00 WYKłAD - FIZYCZNA,\n11:15-12:15 WYKłAD - METODY POZYSKIWANIA DANYCH, "
                       "\n12:30-14:00  ĆWICZENIA - METODY POZYSKIWANIA DANYCH, \n14:15-16:00  ĆWICZENIA - FIZYCZNA",
            "Czwartek":"9:15-11:00 WYKłAD - INŻYNIERYJNA,\n11:15-13:00 WYKłAD - KARTOGRAFIA, "
                       "\n13:15-15:00  ĆWICZENIA - KARTOGRAFIA, \n15:15-17:00  ĆWICZENIA - INŻYNIERYJNA",
             "Piątek":"\n9:15-11:00 SEMINARIUM DYPLOMOWE ( co 2 tydzień) ,\n11:15-13:00 WYKłAD - PROGRAMOWANIE W GIS, "
                       "\n13:15-15:00  ĆWICZENIA - PROGRAMOWANIE W GIS",
}


EVEN_WEEK = False



def change_even_week():
    global EVEN_WEEK
    EVEN_WEEK = not EVEN_WEEK
    return EVEN_WEEK

def check_role(listRole: list):
    listRole = list(filter(lambda x: x != 'XD' or x != '@everyone', listRole))
    if 'starostka' in listRole:
        return 'starostka'
    elif 'szefy' in listRole:
        return 'szefy'
    elif 'geoinformatyk' in listRole:
        return 'geoinformatyk'
    elif "streamer" in listRole:
        return "streamer"
    else:
        return 'impostor'


@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_member_join(member):
    print(f"{member} dołączył do naszej paczki!")


@client.event
async def on_member_remove(member):
    print(f"{member} opśucił nasz serwer!")


@client.event
async def on_message(message):
    idServer = client.get_guild(691631172660363355)
    day = message.content[6:]
    if message.content == "!plan":
        embed = Embed(
            title="Plan zajęć",
            description="Plan dla GeoInfo",
            color=Color.blue()
        )
        embed.add_field(name="Poniedziałek",value=PLAN["Poniedziałek"])
        embed.add_field(name="Wtorek",value=PLAN["Wtorek"])
        embed.add_field(name="Środek",value=PLAN["Środa"])
        embed.add_field(name="Czwartek",value=PLAN["Czwartek"])
        embed.add_field(name="Piątek",value=PLAN["Piątek"])
        await message.channel.send(embed=embed)
    elif  day in list(PLAN.keys()):
        await message.channel.send(PLAN[day])

    elif message.content == '!parzysty':
        text = f"{'Tydzień jest parzysty' if EVEN_WEEK else 'Tydzień jest nie parzysty'}"
        await message.channel.send(text)

    elif message.content == '!help':
        embed = Embed(
            title ="Lista Komend",
            description="!plan - Wyświetla cały plan zajęć"
                        "\n!plan 'Dzień' - Wyświetla plan na dany dzień, dzień musi być napisany z dużej litery"
                        "\n!parzysty - Wyświetla czy mamy tydzień parzysty czy nie",
            color=Color.dark_magenta()
        )
        await message.channel.send(embed=embed)

@client.event
async def on_member_update(before, after):
    channel = client.get_channel(814607303126548520)
    rolesList = [role.name for role in after.roles]
    role = check_role(rolesList)

    if before.status != after.status:
        if after.status == Status.online:
            embed = Embed(
                title='***              UWAGA!!***',
                description=f"__**{after.name}**__ {choice(UWAGI[role]['online'])}",
                color=Color.green()
            )
            await channel.send(embed=embed)

        elif after.status == Status.offline:
            embed = Embed(
                title='***              UWAGA!!***',
                description=f"__**{after.name}**__ {choice(UWAGI[role]['ofline'])}",
                color=Color.red()
            )
            await channel.send(embed=embed)

client.run("ODE0NTE0MTkyMzg4MzI1Mzc3.YDe9dA.c89tsYLtIn62OAL7Ha8s1sgAiV8")
schedule.every().monday.at("6:00").do(change_even_week())
while True:
    schedule.run_pending()
    time.sleep(1)
