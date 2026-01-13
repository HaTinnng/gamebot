import discord
from discord.ext import commands
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# --- Firebase 초기화 설정 ---
# 주의: 봇을 실행하는 폴더에 'serviceAccountKey.json' 파일이 있어야 합니다.
# 파일이 없다면 Firebase 콘솔 -> 프로젝트 설정 -> 서비스 계정 -> 새 비공개 키 생성에서 다운로드하세요.
if not firebase_admin._apps:
    cred_path = "serviceAccountKey.json"
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        print("Warning: serviceAccountKey.json not found. Database connection will fail.")

class ServerStatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # DB 연결 (초기화 실패 시 None)
        try:
            self.db = firestore.client()
        except:
            self.db = None

    @commands.command(name="서버상태")
    @commands.is_owner()
    async def server_status(self, ctx):
        """HTML 게임과 연동된 Firestore DB의 상태를 점검합니다."""
        
        if not self.db:
            return await ctx.send("❌ 데이터베이스 연결 설정이 되어있지 않습니다. `serviceAccountKey.json`을 확인하세요.")

        await ctx.trigger_typing()

        try:
            # HTML 게임에서 사용하는 경로: artifacts/omok-ultimate/public/data/rooms
            # (appId가 'omok-ultimate'라고 가정, 변경 시 수정 필요)
            rooms_ref = self.db.collection('artifacts').document('omok-ultimate') \
                               .collection('public').document('data').collection('rooms')
            
            # 모든 문서 가져오기 (문서 수가 매우 많을 경우 count() 쿼리 사용 권장)
            docs = rooms_ref.stream()
            
            total_rooms = 0
            stagnant_1d = 0
            stagnant_7d = 0
            
            now = datetime.datetime.now(datetime.timezone.utc)
            one_day_ago = now - datetime.timedelta(days=1)
            seven_days_ago = now - datetime.timedelta(days=7)

            for doc in docs:
                total_rooms += 1
                data = doc.to_dict()
                
                # 'updatedAt' 필드 확인
                updated_at = data.get('updatedAt')
                
                # Firestore Timestamp는 datetime 객체로 변환됨
                if updated_at:
                    # 타임존 정보가 없는 경우를 대비해 UTC로 통일
                    if updated_at.tzinfo is None:
                        updated_at = updated_at.replace(tzinfo=datetime.timezone.utc)
                        
                    if updated_at < seven_days_ago:
                        stagnant_7d += 1
                        stagnant_1d += 1
                    elif updated_at < one_day_ago:
                        stagnant_1d += 1

            # 용량 계산 (방 1개당 약 1.2KB 가정 - JSON 문자열 크기 등 고려)
            estimated_size_kb = total_rooms * 1.2
            limit_kb = 1024 * 1024 # Firebase Spark 무료 용량 1GB (1,048,576 KB)
            percent = (estimated_size_kb / limit_kb) * 100

            # 프로그레스 바 생성 (20칸)
            bar_len = 20
            filled = int(round((percent / 100) * bar_len))
            # 100% 넘어가면 꽉 찬 걸로 표시
            if filled > bar_len: filled = bar_len
            
            bar_visual = "█" * filled + "░" * (bar_len - filled)

            # 임베드 출력
            embed = discord.Embed(title="📊 게임 서버(DB) 상태 리포트", color=discord.Color.gold(), timestamp=now)
            embed.description = "Firebase Firestore 'omok-ultimate' 컬렉션 조회 결과"
            
            embed.add_field(name="🏠 총 생성된 방", value=f"**{total_rooms}**개", inline=False)
            embed.add_field(name="💤 1일 이상 변동 없음", value=f"{stagnant_1d}개", inline=True)
            embed.add_field(name="🕸️ 7일 이상 변동 없음", value=f"{stagnant_7d}개", inline=True)
            
            embed.add_field(
                name="💾 저장소 용량 상태 (무료 티어 기준)", 
                value=f"`{bar_visual}` **{percent:.4f}%**\n(약 {estimated_size_kb:.2f} KB 사용 중)", 
                inline=False
            )
            
            embed.set_footer(text=f"요청자: {ctx.author} | 데이터 소스: Firestore")
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ 데이터 조회 중 오류가 발생했습니다:\n`{str(e)}`")

def setup(bot):
    bot.add_cog(ServerStatusCog(bot))
