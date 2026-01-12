import discord
from discord.ext import commands
import os
import random

class GameLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 호스팅 사이트에 등록한 기본 주소 (예: https://...web.app)
        self.base_url = os.getenv("GAME_URL")

    def create_game_embed(self, game_name, folder_name):
        """공통 임베드 생성 함수"""
        if not self.base_url:
            return discord.Embed(description="⚠️ 환경 변수 'GAME_URL'이 설정되지 않았습니다.", color=discord.Color.red())

        # 4자리 랜덤 방 번호 생성 (실시간 데이터베이스 경로 구분용)
        room_id = random.randint(1000, 9999)
        
        embed = discord.Embed(
            title=f"🎮 {game_name} 시작!",
            description=f"방 번호: **{room_id}**\n친구와 함께 아래 링크로 접속하세요!",
            color=0x00ff55
        )

        # 폴더 경로를 포함한 링크 조립
        # 예: https://주소/quiz/index.html?room=1234&color=red
        red_link = f"{self.base_url}/{folder_name}/index.html?room={room_id}&color=red"
        yellow_link = f"{self.base_url}/{folder_name}/index.html?room={room_id}&color=yellow"

        embed.add_field(name="🔴 1번 플레이어", value=f"[접속하기]({red_link})", inline=True)
        embed.add_field(name="🟡 2번 플레이어", value=f"[접속하기]({yellow_link})", inline=True)
        embed.set_footer(text="접속 후 상대방이 들어올 때까지 기다려주세요.")
        
        return embed

    @commands.command(name="퀴즈1")
    async def play_quiz1(self, ctx):
        """quiz 폴더의 게임 링크 전송"""
        await ctx.send(embed=self.create_game_embed("첫 번째 퀴즈 게임", "quiz"))

    @commands.command(name="퀴즈2")
    async def play_quiz2(self, ctx):
        """quiz2 폴더의 게임 링크 전송"""
        await ctx.send(embed=self.create_game_embed("두 번째 퀴즈 게임", "quiz2"))

async def setup(bot):
    await bot.add_cog(GameLink(bot))
