import discord
from discord.ext import commands
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json

# --- Firebase 초기화 로직 (환경 변수 전용) ---
if not firebase_admin._apps:
    firebase_creds_json = os.environ.get("FIREBASE_CREDENTIALS")
    
    if firebase_creds_json:
        try:
            cred_dict = json.loads(firebase_creds_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✅ 환경 변수(FIREBASE_CREDENTIALS)를 통해 Firebase에 안전하게 연결되었습니다.")
        except Exception as e:
            print(f"❌ 환경 변수 로드 실패: {e}")
            print("환경 변수 내용이 올바른 JSON 형식인지 확인해주세요.")
    else:
        print("❌ 오류: 'FIREBASE_CREDENTIALS' 환경 변수가 설정되지 않았습니다.")
        print("배포하는 웹사이트의 설정 페이지(Secrets/Config Vars)에 환경 변수를 추가해주세요.")

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.db = firestore.client()
        except:
            self.db = None

    @commands.command(name="서버상태")
    @commands.is_owner()
    async def server_status(self, ctx):
        """HTML 게임과 연동된 Firestore DB의 상태를 점검합니다."""
        
        if not self.db:
            return await ctx.send("❌ 데이터베이스 연결 실패. 호스팅 사이트의 환경 변수(Secrets)를 확인하세요.")

        await ctx.trigger_typing()

        try:
            # Firestore 경로: artifacts -> omok-ultimate -> public -> data -> rooms
            rooms_ref = self.db.collection('artifacts').document('omok-ultimate') \
                               .collection('public').document('data').collection('rooms')
            
            # DB에서 모든 방 데이터 가져오기
            docs = rooms_ref.stream()
            
            total_rooms = 0
            stagnant_1d = 0
            stagnant_7d = 0
            
            # 현재 시간 (UTC 기준)
            now = datetime.datetime.now(datetime.timezone.utc)
            one_day_ago = now - datetime.timedelta(days=1)
            seven_days_ago = now - datetime.timedelta(days=7)

            for doc in docs:
                total_rooms += 1
                data = doc.to_dict()
                
                # 방의 마지막 업데이트 시간 확인
                updated_at = data.get('updatedAt')
                
                if updated_at:
                    if updated_at.tzinfo is None:
                        updated_at = updated_at.replace(tzinfo=datetime.timezone.utc)
                        
                    if updated_at < seven_days_ago:
                        stagnant_7d += 1
                        stagnant_1d += 1
                    elif updated_at < one_day_ago:
                        stagnant_1d += 1

            # 서버 용량 추산 (방 1개당 약 1.2KB로 가정)
            estimated_size_kb = total_rooms * 1.2
            limit_kb = 1024 * 1024 # 1GB (무료 티어 한도)
            percent = (estimated_size_kb / limit_kb) * 100

            bar_len = 20
            filled = int(round((percent / 100) * bar_len))
            if filled > bar_len: filled = bar_len
            bar_visual = "█" * filled + "░" * (bar_len - filled)

            embed = discord.Embed(title="📊 게임 서버(DB) 상태 리포트", color=discord.Color.gold(), timestamp=now)
            embed.description = "Firebase Firestore 'omok-ultimate' 상태"
            
            embed.add_field(name="🏠 총 생성된 방", value=f"**{total_rooms}**개", inline=False)
            embed.add_field(name="💤 1일 이상 미활동", value=f"{stagnant_1d}개", inline=True)
            embed.add_field(name="🕸️ 7일 이상 미활동", value=f"{stagnant_7d}개", inline=True)
            
            embed.add_field(
                name="💾 저장소 용량 (추정)", 
                value=f"`{bar_visual}` **{percent:.4f}%**\n(약 {estimated_size_kb:.2f} KB 사용 중)", 
                inline=False
            )
            
            embed.set_footer(text=f"관리자 전용 | {ctx.author}")
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ 데이터 조회 중 오류가 발생했습니다:\n`{str(e)}`")

# --- 수정된 부분 ---
# discord.py 2.0 이상에서는 setup 함수가 async여야 하고 add_cog를 await 해야 합니다.
async def setup(bot):
    await bot.add_cog(Admin(bot))
