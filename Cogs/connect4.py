import discord
from discord.ext import commands
import os
import random

class Connect4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = os.getenv("GAME_URL")

    @commands.command(name="커넥트포")
    async def play_connect4(self, ctx):
        """멀티 플레이: 커넥트 포"""
        if not self.base_url: 
            return await ctx.send("⚠️ GAME_URL 설정 필요")

        room_id = random.randint(1000, 9999)
        embed = discord.Embed(
            title="🔵 커넥트 포 멀티플레이", 
            description=f"방 번호: **{room_id}**\n상대방과 다른 색깔 링크를 눌러주세요!",
            color=0x0055ff
        )

        red_url = f"{self.base_url}/connect4/index.html?room={room_id}&color=red"
        yellow_url = f"{self.base_url}/connect4/index.html?room={room_id}&color=yellow"

        embed.add_field(name="🔴 1번 플레이어", value=f"[Red 접속]({red_url})", inline=True)
        embed.add_field(name="🟡 2번 플레이어", value=f"[Yellow 접속]({yellow_url})", inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Connect4(bot))
