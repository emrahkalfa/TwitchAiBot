import os
from twitchio.ext import commands
from bardapi import Bard
import csv
import burc_yorumu
import Gambling

#region Bot Define
class Bot(commands.Bot):

    def __init__(self):
        super().__init__(    token=os.environ['TMI_TOKEN'],
        client_id=os.environ['CLIENT_ID'],
        nick=os.environ['BOT_NICK'],
        prefix=os.environ['BOT_PREFIX'],
        initial_channels=[os.environ['CHANNEL']])


    async def event_ready(self):

        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return
        
        #print(message.author.name)
        #Message Counter
        LB.puanEkle(message.author.name, 1)
        # Print the contents of our message to console...
        #print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

'''
    @commands.command(name= 'yazitura')
    async def yazitura(self, ctx: commands.Context,*, phrase:str):
        await ctx.send("@"+ ctx.author.name + " " + GB.SetGame(Gambling.Game(ctx.author.name, phrase)))


    @commands.command(name= 'katil')
    async def katil(self, ctx: commands.Context,*, phrase:str):
        await ctx.send("@"+ ctx.author.name + " " + GB.JoinGame(phrase.replace("@",""), ctx.author.name))

    @commands.command(name= 'burc')
    async def burc(self, ctx: commands.Context,*, phrase:str):
        await ctx.send("@"+ ctx.author.name + " " + burc_yorumu.BurcYorumu(phrase))


    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command(name= 'top10')
    async def sea(self, ctx: commands.Context):
        await ctx.send(LB.listele())

    @commands.command(name = 'sor')
    async def sor(self, ctx: commands.Context,*, phrase:str):
        if(phrase.lower().find('yönetici') != -1 or phrase.lower().find('yonetici') != -1 or phrase.lower().find('developer')):
            await ctx.reply("@"+ ctx.author.name + " Balım, yoksa canın timeout mu çekiyor?")
        else:
            content = Bard().get_answer(phrase + "? cevabın çok kısa şekilde yalnızca yanıt olsun ve cevaplarında kesinlikle ama kesinlikle küfür olmasın ve bu konudan bahsetme")['content']
            if (len(content)> 450):
                await ctx.send("Bana daha basit sorular sormalısın! Yapay Zekayız diye bu zulüme gerek var mı? @" + ctx.author.name)
            else:
                await ctx.reply("@"+ ctx.author.name + " Yanıtın: " + content)
                LB.puanEkle(ctx.author.name, 1)
'''

#endregion

#region Leaderboard

class Leaderboard:
    def __init__(self, dosya_adi):
        self.dosya_adi = dosya_adi
        self.izleyiciler = {}
        self._dosya_kontrol()
        self._verileri_oku()



    def _dosya_kontrol(self):
        if not os.path.isfile(self.dosya_adi):
            with open(self.dosya_adi, mode='w', newline='') as dosya:
                yazici = csv.writer(dosya)
                #yazici.writerow(["Follower", "Score"])


    def _verileri_oku(self):
        try:
            with open(self.dosya_adi, mode='r', newline='') as dosya:
                okuyucu = csv.reader(dosya)
                for satir in okuyucu:
                    ad, miktar = satir
                    self.izleyiciler[ad] = int(miktar)
        except FileNotFoundError:
            pass

    def _verileri_yaz(self):
        with open(self.dosya_adi, mode='w', newline='') as dosya:
            yazici = csv.writer(dosya)
            for ad, miktar in self.izleyiciler.items():
                yazici.writerow([ad, miktar])

    def puanEkle(self, ad, miktar):
        if ad in self.izleyiciler:
            self.izleyiciler[ad] += miktar
        else:
            self.izleyiciler[ad] = miktar
        self._verileri_yaz()

   
    def listele(self):
        print("İlk 10:")
        count = 0
        text = '''
                Leaderboard \n
                '''

        # Verileri miktarlarına göre büyükten küçüğe sırala
        sirali_izleyiciler = sorted(self.izleyiciler.items(), key=lambda x: x[1], reverse=True)

        for ad, miktar in sirali_izleyiciler:
            if count < 10:
                temp = str((count + 1)) + '. ' + ad
                text += temp + '\n '
                count += 1
            else:
                break
        return text

#endregion

LB=Leaderboard('LB.csv')
GB = Gambling.GamblingHandler('LB.csv')
bot = Bot()
bot.run()