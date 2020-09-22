#RT Util
from json import dump
from os import path
import discord


async def error(title,description,color=None,footer=None,image=None,author=None):
    try:
        title = f"<:error:757081926111854722> {title}"
        if color is None:
            color = 0xf00000
        embed = discord.Embed(title=title,description=description,color=color)
        if footer is not None:
            embed.set_footer(text=footer[0],icon_url=footer[1])
        if image is not None:
            embed.set_image(url=image)
        if author is not None:
            embed.set_author(name=author)
    except Exception as e:
        embed = discord.Embed(title="<:error:757081926111854722>RTエラー",description="すみませんがRTにエラーが発生しました。\nできれば[サポートサーバー](https://discord.gg/ugMGw5w)で以下のエラーログを伝えてほしいです。\n```{e}```",color=0xf00000)
    return embed


async def jwrite(fpath,content):
    if (path.exists(fpath)):
        with open(fpath, 'w') as f:
            dump(content, f, indent=4)


async def jread(fpath):
    if (path.exists(fpath)):
        with open(fpath,mode="r",encoding="utf-8") as f:
            return json.load(f)


async def hasamu(content, banzu):
    print("Hamburger Taking")
    ban = content.count(banzu)
    sta = []
    if ban > 1:
        if ban == 2:
            x = content.find(banzu)
            y = content.find(banzu, x+2)
            sta.append(content[x + 1 : y])
            print(f"-=-=-=-=-=-=-=-=\nTake -> {content[x + 1 : y]}")
        elif ban % 2 == 0:
            for i in range(int(ban/2)):
                x = content.find(banzu)
                y = content.find(banzu, x+2)
                kek = content[x + 1 : y]
                sta.append(kek)
                content = content.replace(f"{banzu}{kek}{banzu}", "")
                print(f"-=-=-=-=-=-=-=-=\nTake -> {kek}\nUpdata -> {content}")
    print(f"-=-=-=-=-=-=-=-=\nResults -> {sta}\nTaiking is end.")
    return sta


async def get_line(s, line_number):
    return s.splitlines()[line_number - 1]