import discord
from discord.ext import commands

class GameMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="게임", aliases=["게임목록", "games", "game"])
    async def show_game_list(self, ctx):
        """
        현재 봇에서 플레이 가능한 모든 게임 목록을 보여줍니다.
        사용법: #게임
        """
        embed = discord.Embed(
            title="🎮 멀티플레이 게임 라운지",
            description="친구와 함께 즐길 수 있는 게임 목록입니다.\n각 게임의 **명령어**를 입력하면 게임 링크가 생성됩니다.",
            color=0x00ff00  # 초록색 테두리
        )

        # ---------------------------------------------------------
        # 1. 커넥트 포 (이미 만드신 기능)
        # ---------------------------------------------------------
        embed.add_field(
            name="1️⃣ 커넥트 포 (Connect 4)", 
            value="> **명령어:** `!커넥트포`, `!사목` \n> **설명:** 칩을 4개 연속으로 놓으면 승리하는 두뇌 게임!", 
            inline=False
        )

        # ---------------------------------------------------------
        # 2. (추후 추가될 게임 예시 - 지금은 준비중으로 표시)
        # ---------------------------------------------------------
        embed.add_field(
            name="2️⃣ 오목", 
            value="> **명령어:** `!오목`\n> **설명:** 5개의 돌을 먼저 놓는 사람이 승리!", 
            inline=False
        )

        # ---------------------------------------------------------
        # 3. (추후 추가될 게임 예시)
        # ---------------------------------------------------------
        embed.add_field(
            name="3️⃣ 틱택토", 
            value="> **명령어:** `!틱택토`, `!틱` \n> **설명:** 무한으로 이어지는 틱택토에서 승리해보세요!", 
            inline=False
        )

        embed.add_field(
            name="4️⃣ 포켓몬타입", 
            value="> **명령어:** `!틱택토`, `!틱` \n> **설명:** 각 지방 네임드 트레이너의 타입을 맞춰보세요!", 
            inline=False
        )

        embed.add_field(
            name="5️⃣ 1인 포커", 
            value="> **명령어:** `!포커`, `!틱` \n> **설명:** 혼자서 하는 1인 포커! 베팅을 통해 많은 돈을 얻어보세요!", 
            inline=False
        )

        embed.set_footer(text="💡 원하는 게임의 명령어를 채팅창에 입력해보세요!")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GameMenu(bot))
