import json
import os
import platform
import random
import sys
from datetime import datetime, timedelta

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context


def get_week_dates(base_date, start_day=1, end_day=7):
    monday = base_date - timedelta(days=base_date.isoweekday() - 1)
    week_dates = [monday + timedelta(days=i) for i in range(7)]
    return week_dates[start_day - 1:end_day or start_day]


class Logs(commands.Cog, name="logs-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="getlist",
        description="Get list",
    )
    async def getlist(self, context: Context, date: str, *, channel_id: int = None) -> None:
        embed = discord.Embed(color=0x9C84EF, type="article")
        if channel_id:
            channel = self.bot.get_channel(channel_id)
        else:
            channel = context.channel
        day = datetime.strptime(date, "%d/%m/%y")
        count_messages = 0
        day = day.replace(tzinfo=None)
        reaction_logs = {}
        async for message in channel.history(limit=4000, before=day + timedelta(days=1)):
            msg_created = message.created_at.replace(tzinfo=None) + timedelta(hours=3)
            if msg_created > day:
                if message.reactions:
                    for reaction in message.reactions:
                        async for user in reaction.users():
                            if int(user.id) in reaction_logs.keys():
                                reaction_logs[int(user.id)] += 1
                            else:
                                reaction_logs[int(user.id)] = 1
                count_messages += 1
            else:
                break
        embed.set_author(name=f"Reaction Statistics in <#{channel.name}>")
        embed.add_field(name=f"Messages at {date}", value=f"{count_messages}", inline=False)
        out = ""
        for unit in reaction_logs.items():
            out += f"<@{unit[0]}> - **{unit[1]}**\n"
        embed.add_field(name=f"Statistics", value=out, inline=False)
        await context.send(embed=embed)

    @commands.command(
        name="getlist_night",
        description="Get list",
    )
    async def getlist_night(self, context: Context, date: str, *, channel_id: int = None) -> None:
        embed = discord.Embed(color=0x9C84EF, type="article")
        if channel_id:
            channel = self.bot.get_channel(channel_id)
        else:
            channel = context.channel
        day = datetime.strptime(date, "%d/%m/%y")
        count_messages = 0
        day = day.replace(tzinfo=None)
        reaction_logs = {}
        async for message in channel.history(limit=500, before=day + timedelta(hours=6, minutes=30)):
            msg_created = message.created_at.replace(tzinfo=None) + timedelta(hours=3)
            if msg_created > day:
                if message.reactions:
                    for reaction in message.reactions:
                        async for user in reaction.users():
                            if int(user.id) in reaction_logs.keys():
                                reaction_logs[int(user.id)] += 1
                            else:
                                reaction_logs[int(user.id)] = 1
                count_messages += 1
            else:
                break
        embed.set_author(name=f"Night Reaction Statistics in <#{channel.name}>")
        embed.add_field(name=f"Messages at {date}", value=f"{count_messages}", inline=False)
        out = ""
        for unit in reaction_logs.items():
            out += f"<@{unit[0]}> - **{unit[1]}**\n"
        embed.add_field(name=f"Statistics", value=out, inline=False)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="allticketsday",
        description="Статистика тикетов за день",
    )
    async def allticketsday(self, context: Context, date: str = None) -> None:
        sembed = discord.Embed(color=0x9C84EF, type="article")
        channel = context.bot.get_channel(1008047856000716810)
        if date:
            day = datetime.strptime(date, "%d/%m/%y")
        else:
            date = datetime.now().strftime("%d/%m/%y")
            day = datetime.strptime(date, "%d/%m/%y")
        sembed.set_author(name=f"Ticket Stats")
        sembed.add_field(name=f"Tickets at {date}", value=f"###", inline=False)
        sembed.add_field(name=f"Statistics", value="Wait for stats.....", inline=False)
        msg = await context.send(embed=sembed)
        count_messages = 0
        day = day.replace(tzinfo=None)
        ticket_logs = {}
        async for message in channel.history(limit=3000, before=day + timedelta(days=1)):
            msg_created = message.created_at.replace(tzinfo=None) + timedelta(hours=3)
            if msg_created > day:
                if message.embeds:
                    for embed in message.embeds:
                        if 'Action: Deleted' in embed.to_dict()['fields'][0]['value']:
                            moder = embed.to_dict()['author']['name']
                            if moder in ticket_logs.keys():
                                ticket_logs[moder] += 1
                            else:
                                ticket_logs[moder] = 1
                            count_messages += 1
            else:
                break
        sembed.set_author(name=f"Ticket Stats")
        sembed.remove_field(-1)
        sembed.remove_field(-1)
        sembed.add_field(name=f"Tickets at {date}", value=f"{count_messages}", inline=False)
        out = ""
        for unit in sorted(ticket_logs.items(), key=lambda x: x[1], reverse=True):
            out += f"{unit[0]} - **{unit[1]}**\n"
        sembed.add_field(name=f"Statistics", value=out, inline=False)
        await msg.edit(embed=sembed)

    @commands.hybrid_command(
        name="ticketsday",
        description="Личная статистика тикетов за день",
    )
    async def ticketsday(self, context: Context, date: str = None, *, user: str = None) -> None:
        sembed = discord.Embed(color=0x9C84EF, type="article")
        channel = context.bot.get_channel(1008047856000716810)
        if user:
            user = context.bot.get_user(int(user.replace("<@", "").replace(">", ""))).name
        else:
            user = context.author.name
        if date:
            day = datetime.strptime(date, "%d/%m/%y")
        else:
            date = datetime.now().strftime("%d/%m/%y")
            day = datetime.strptime(date, "%d/%m/%y")
        sembed.set_author(name=f"Ticket Stats - {user}")
        sembed.add_field(name=f"Tickets at {date}", value=f"###", inline=False)
        sembed.add_field(name=f"Statistics", value="Wait for stats.....", inline=False)
        msg = await context.send(embed=sembed)
        count_messages = 0
        day = day.replace(tzinfo=None)
        async for message in channel.history(limit=3000, before=day + timedelta(days=1)):
            msg_created = message.created_at.replace(tzinfo=None) + timedelta(hours=3)
            if msg_created > day:
                if message.embeds:
                    for embed in message.embeds:
                        if 'Action: Deleted' in embed.to_dict()['fields'][0]['value']:
                            moder = embed.to_dict()['author']['name']
                            if moder.split("#")[0] == user:
                                count_messages += 1
            else:
                break
        sembed.set_author(name=f"Ticket Stats - {user}")
        sembed.remove_field(-1)
        sembed.remove_field(-1)
        sembed.add_field(name=f"Tickets at {date}", value=f"{count_messages}", inline=False)
        await msg.edit(embed=sembed)

    @commands.hybrid_command(
        name="allmutesday",
        description="Статистика мутов за день",
    )
    async def allmutesday(self, context: Context, date: str = None) -> None:
        sembed = discord.Embed(color=0x9C84EF, type="article")
        channel = context.bot.get_channel(894299368834879488)
        if date:
            day = datetime.strptime(date, "%d/%m/%y")
        else:
            date = datetime.now().strftime("%d/%m/%y")
            day = datetime.strptime(date, "%d/%m/%y")
        sembed.set_author(name=f"Mute Stats")
        sembed.add_field(name=f"Mutes at {date}", value="###", inline=False)
        sembed.add_field(name=f"Statistics", value="Wait for stats.....", inline=False)
        msg = await context.send(embed=sembed)
        count_messages = 0
        day = day.replace(tzinfo=None)
        mute_logs = {}
        async for message in channel.history(limit=3000, before=day + timedelta(days=1)):
            msg_created = message.created_at.replace(tzinfo=None) + timedelta(hours=3)
            if msg_created > day:
                if "#mute" in message.content.lower():
                    if message.author.id in mute_logs.keys():
                        mute_logs[message.author.id] += 1
                    else:
                        mute_logs[message.author.id] = 1
                    count_messages += 1
                elif "#unmute" in message.content.lower():
                    if message.author.id in mute_logs.keys():
                        mute_logs[message.author.id] -= 1
                    else:
                        mute_logs[message.author.id] = -1
                    count_messages -= 1

            else:
                break

        out = ""
        for unit in sorted(mute_logs.items(), key=lambda x: (x[1]), reverse=True):
            if unit[1] > 0:
                out += f"<@{unit[0]}> - **{unit[1]}**\n"
            else:
                break
        sembed.remove_field(-1)
        sembed.remove_field(-1)
        sembed.add_field(name=f"Mutes at {date}", value=f"{count_messages}", inline=False)
        sembed.add_field(name=f"Statistics", value=out, inline=False)
        await msg.edit(embed=sembed)

    @commands.hybrid_command(
        name="mutesday",
        description="Личная статистика мутов за день",
    )
    async def mutesday(self, context: Context, date: str = None, user: str = None) -> None:
        sembed = discord.Embed(color=0x9C84EF, type="article")
        channel = context.bot.get_channel(894299368834879488)
        if user:
            user = int(user.replace("<@", "").replace(">", ""))
        else:
            user = context.author.id
        if date:
            day = datetime.strptime(date, "%d/%m/%y")
        else:
            date = datetime.now().strftime("%d/%m/%y")
            day = datetime.strptime(date, "%d/%m/%y")
        sembed.set_author(name=f"Mute Stats")
        sembed.add_field(name=f"Mutes at {date}", value="###", inline=False)
        sembed.add_field(name=f"Statistics", value="Wait for stats.....", inline=False)
        msg = await context.send(embed=sembed)
        count_messages = 0
        day = day.replace(tzinfo=None)
        async for message in channel.history(limit=3000, before=day + timedelta(days=1)):
            msg_created = message.created_at.replace(tzinfo=None) + timedelta(hours=3)
            if msg_created > day:
                if "#mute" in message.content.lower() and message.author.id == user:
                    count_messages += 1
                elif "#unmute" in message.content.lower() and message.author.id == user:
                    count_messages -= 1
            else:
                break
        sembed.remove_field(-1)
        sembed.remove_field(-1)
        sembed.set_author(name=f"Mute Stats - {context.bot.get_user(user).display_name}")
        sembed.add_field(name=f"Mutes at {date}", value=f"{count_messages}", inline=False)
        await msg.edit(embed=sembed)

    @commands.command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    async def sync(self, context: Context) -> None:
        await context.bot.tree.sync()
        embed = discord.Embed(
            title="Slash Commands Sync",
            color=0x9C84EF,
        )
        await context.send(embed=embed)
        return

    @commands.command(
        name="allweekmutes",
        description="Общая статистика мутов за неделю",
    )
    async def allweekmutes(self, context: Context, date: str = None) -> None:
        sembed = discord.Embed(color=0x9C84EF, type="article")
        channel = context.bot.get_channel(894299368834879488)
        if date:
            day = datetime.strptime(date, "%d/%m/%y")
        else:
            date = datetime.now().strftime("%d/%m/%y")
            day = datetime.strptime(date, "%d/%m/%y")
        sembed.set_author(name=f"Mute Stats")
        sembed.add_field(name=f"Mutes at {date}", value="###", inline=False)
        sembed.add_field(name=f"Statistics", value="Wait for stats.....", inline=False)
        msg = await context.send(embed=sembed)
        days = get_week_dates(day)
        count_messages = 0
        mute_logs = {}
        for wday in days:
            wday = wday.replace(tzinfo=None)
            async for message in channel.history(limit=3000, before=wday + timedelta(days=1)):
                msg_created = message.created_at.replace(tzinfo=None) + timedelta(hours=3)
                if msg_created > wday:
                    if "#mute" in message.content.lower():
                        if message.author.id in mute_logs.keys():
                            mute_logs[message.author.id] += 1
                        else:
                            mute_logs[message.author.id] = 1
                        count_messages += 1
                    elif "#unmute" in message.content.lower():
                        if message.author.id in mute_logs.keys():
                            mute_logs[message.author.id] -= 1
                        else:
                            mute_logs[message.author.id] = -1
                        count_messages -= 1
                else:
                    break
        out = ""
        for unit in sorted(mute_logs.items(), key=lambda x: (x[1]), reverse=True):
            if unit[1] > 0:
                out += f"<@{unit[0]}> - **{unit[1]}**\n"
            else:
                break
        sembed.remove_field(-1)
        sembed.remove_field(-1)
        sembed.add_field(name=f"Mutes at {days[0].strftime('%d/%m/%y')} - {days[-1].strftime('%d/%m/%y')}", value=f"{count_messages}", inline=False)
        sembed.add_field(name=f"Statistics", value=out, inline=False)
        await msg.edit(embed=sembed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
