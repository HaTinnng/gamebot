import discord
from discord.ext import commands
import os

class GameLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 호스팅 사이트 설정창에 입력한 'GAME_URL'을 가져옵니다.
        self.game_url = os.getenv("GAME_URL")

    @commands.command(name="커넥트포")
    async def connect_four(self, ctx):
        """커넥트 포 멀티플레이 링크를 전송합니다."""
        if not self.game_url:
            await ctx.send("⚠️ 환경 변수 'GAME_URL'이 설정되지 않았습니다.")
            return

        # 임베드(Embed)를 사용해 깔끔하게 디자인합니다.
        embed = discord.Embed(
            title="🎮 실시간 커넥트 포 (Connect 4)",
            description="친구와 함께 대결하세요! 아래 링크 중 하나를 선택해 접속하세요.",
            color=0x0055ff
        )
        
        # 주소 뒤에 ?color=...를 붙여서 플레이어 역할을 나눕니다.
        link_red = f"{self.game_url}/index.html?color=red"
        link_yellow = f"{self.game_url}/index.html?color=yellow"

        embed.add_field(name="🔴 1번 플레이어 (Red)", value=f"[게임 접속]({link_red})", inline=True)
        embed.add_field(name="🟡 2번 플레이어 (Yellow)", value=f"[게임 접속]({link_yellow})", inline=True)
        embed.set_footer(text="구글 서버를 통해 실시간으로 동기화됩니다.")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GameLink(bot))
