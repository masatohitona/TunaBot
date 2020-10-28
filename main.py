# -*- coding: utf-8 -*-
# tsuna bot
from discord.ext import commands
from datetime import datetime, timedelta
from discord.ext import tasks
import discord
import rtutil
import json
import os


print('Now loading...')


with open("data.json",mode="r") as f:
    td = json.load(f)

color = 0xe2af65

team_id = [739702692393517076,634763612535390209]
class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id in team_id:
            return True
        return await super().is_owner(user)


bot = MyBot(command_prefix="2!")
bot.load_extension("jishaku")
bot.remove_command("help")


def get_line(content,line):
    return content.splitlines()[line-1]


@bot.event
async def on_ready():
    activity = discord.Activity(
        name=f"2!help | {len(bot.guilds)}server", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    asend.start()
    print("Started")


@bot.command()
async def tasuren(ctx):
    await ctx.send("BOT開発者が仕込んだ隠しメッセージ!")


# 招待リンク
@bot.command()
async def invite(ctx):
    await ctx.send("このBOTの招待リンク\nhttps://discord.com/api/oauth2/authorize?client_id=756435800845058109&permissions=8&scope=bot")


# HELP コマンド
@bot.command()
async def help(ctx,arg=None):
    print(f"-Help\n|<Author>{ctx.author}")
    if arg is None:
        # ノーマル
        embed = discord.Embed(
            title="tsuna Bot HELP",
            description="**`2!help 見たい機能の名前`** で機能の詳細を見ることができます。",
            color=color)
        with open("help/cmd.txt","r",encoding="utf-8_sig") as f:
            cont = f.read()
        name = get_line(cont,1)
        value = cont.replace(get_line(cont,1),"",1)
        embed.add_field(
            name=name,
            value=value)
        await ctx.send(embed=embed)
    else:
        # 機能詳細
        if (os.path.exists(f"help/{arg}.txt")):
            with open(f"help/{arg}.txt",encoding="utf-8_sig") as f:
                cont = f.read()
            name = get_line(cont,1)
            value = cont.replace(get_line(cont,1),"",1)
            embed = discord.Embed(
                title=name,
                description=value,
                color=color)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"`{arg}`の名前の機能が見つかりませんでした。")


# ユーザー取得
@bot.command()
async def user(ctx,uid):
    print(f"-user\n|<Author>{ctx.author}")
    user = await bot.fetch_user(int(uid))
    s = ""
    if user.bot:
        s = "`BOT`"
    embed = discord.Embed(title=f"{user}{s}",color=color)
    time = user.created_at+timedelta(hours=9)
    embed.add_field(name="アイコンURL",value=user.avatar_url_as(format="png"),inline=False)
    embed.add_field(name="タグ",value=user.discriminator)
    embed.add_field(name="ID",value=user.id)
    embed.set_footer(text=f"Discord参加日：{time.strftime('%Y-%m-%d')}")
    embed.set_thumbnail(url=user.avatar_url_as(format="png"))
    await ctx.send(embed=embed)


# タイマーチャット
@bot.command()
async def tmchat(ctx,mes,time):
    print(f"-tmchat\n|<Author>{ctx.author}\n|<Time>{time}\n|<mes>{mes}")
    async with ctx.typing():
        time = datetime.now() + timedelta(minutes=int(time))
        time = time.strftime('%Y-%m-%d %H:%M')
        embed = discord.Embed(title="タイマーチャット",description="タイマーチャットをセットしました。",color=color)
        embed.add_field(name="予定時間",value=time)
        embed.add_field(name="メッセージ",value=mes)
        td["timer"][str(ctx.channel.id)] = {}
        td["timer"][str(ctx.channel.id)]["time"] = time
        td["timer"][str(ctx.channel.id)]["mes"] = mes
        td["timer"][str(ctx.channel.id)]["author"] = str(ctx.author.id)
        await rtutil.jwrite("data.json",td)
    await ctx.send(embed=embed)


# GBAN 追加、削除コマンド
@bot.command()
async def gban(ctx,mode,uid,reason):
    if ctx.author.id in [739702692393517076,634763612535390209]:
        if mode == "add":
            try:
                user = await bot.fetch_user(int(uid))
            except:
                user = None
            if user is not None:
                if td["gban"].get(uid) is None:
                    async with ctx.typing():
                        td["gban"][uid] = reason
                        await rtutil.jwrite("data.json",td)
                        embed = discord.Embed(
                            title=f"GBANリストにユーザーが追加されました",
                            description=f"追加ユーザー：{user} ({user.id})",
                            color=0xf78279)
                        embed.add_field(name="理由",value=td["gban"][uid])
                        embed.set_thumbnail(url=user.avatar_url_as(format="png"))
                        for tg in bot.guilds:
                            for tc in tg.text_channels:
                                if tc.name == "tsuna-gban":
                                    if user in tc.guild.members:
                                        await tc.guild.ban(user,reason=f"<TUNA-GBAN>{td['gban'][uid]}")
                                    await tc.send(embed=embed)
                    await ctx.send(f"`{uid}`のユーザーをGBANに追加しました。")
                else:
                    await ctx.send(f"`{uid}`のユーザーは既に追加されています。")
            else:
                await ctx.send(f"`{uid}`のユーザーが見つかりませんでした。")
        elif mode == "rm":
            if td["gban"].get(uid) is not None:
                del td["gban"][uid]
                await rtutil.jwrite("data.json",td)
                await ctx.send(f"`{uid}`のユーザーをGBANから削除しました。")
            else:
                await ctx.send(f"`{uid}`のユーザーはまだ追加されていません。")
    else:
        await ctx.send("GBANコマンドを実行できるのはツナ缶さんだけです。\nGBAN追加してほしい場合,ツナ缶さんに申請してください。")


# タイマーチャット送信用
@tasks.loop(seconds=30)
async def asend():
    rm_list = []
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    for t in td["timer"].keys():
        if now == td["timer"][t]["time"]:
            channel = bot.get_channel(int(t))
            mes = td["timer"][t]["mes"]
            user = bot.get_user(int(td["timer"][t]["author"]))
            ch_webhooks = await channel.webhooks()
            webhook = discord.utils.get(ch_webhooks, name="tuna-tmchat")
            if webhook is None:
                webhook = await channel.create_webhook(name="tsuna-tmchat")
            await webhook.send(
                content=mes,
                username=f"{user} (タイマーチャット機能)",
                avatar_url=user.avatar_url_as(format="png"))
            rm_list.append(t)
    for t in rm_list:
        del td["timer"][t]
    await rtutil.jwrite("data.json",td)


# メンバーが入った時
@bot.event
async def on_member_join(member):
    # GBANリストにいるか
    channel = discord.utils.get(member.guild.text_channels, name="tsuna-gban")
    if td["gban"].get(str(member.id)) is not None and channel is not None:
        await member.guild.ban(member,reason=f"<TUNA-GBAN>{td['gban'][str(member.id)]}")
        embed = discord.Embed(
            title=f"GBAN実行のお知らせ",
            description=f"{member}をGBANリストにいたためBANしました。",
            color=0xf78279)
        embed.add_field(name="理由",value=td["gban"][str(member.id)])
        embed.set_thumbnail(url=member.avatar_url_as(format="png"))
        await channel.send(embed=embed)


# メッセージが来たとき
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    # BOTはreturn
    if message.author.bot:
        return


    ### グローバルチャット ###
    # 1.tsuna-globalというのがチャンネルにあるか 2.あったらすべてのサーバーでtsuna-globalのチャンネルを探す
    # 3.ウェブフックがない場合作り送信する
    # tg - サーバー    tc - サーバーのチャンネル
    if "tsuna-global" in message.channel.name:
        print(f"-Global Chat\n|<Author>{message.author}\n|<Guild> {message.guild.name}")
        for tg in bot.guilds:
            for tc in tg.text_channels:
                if "tsuna-global" in tc.name and tc.id != message.channel.id:
                    # 画像あったら画像送信
                    pic = ""
                    if message.attachments != []:
                        for at in message.attachments:
                            pic = pic + at.url + "\n"
                    # ウェブフックを探す
                    ch_webhooks = await tc.webhooks()
                    webhook = discord.utils.get(ch_webhooks, name="tuna-global-webhook")
                    # ウェブフックがなかったら作る
                    if webhook is None:
                        webhook = await tc.create_webhook(name="tuna-global-webhook")
                    # ウェブフックを送信
                    await webhook.send(
                        content=f"{message.content}\n{pic}",
                        username=f"{message.author} ({message.author.id}) From:{message.guild.name}",
                        avatar_url=message.author.avatar_url_as(format="png"))


# Main
bot.run("token")
# Test
#bot.run("token")
