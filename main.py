import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import nextcord
from nextcord.ext import commands
from nextcord.utils import get

# โหลด Token และข้อมูลจาก Config.json
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)


TOKEN = config["token"]
ROLE_IDS = config["role_ids"]  # role_ids ควรเป็น dictionary ที่ mapping ระดับชั้นเรียนกับ role_id
LOGIN_URL = "https://sgs6.bopp-obec.info/sgss/Security/SignIn.aspx"
STUDENT_INFO_URL = "https://sgs6.bopp-obec.info/sgss/TblStudents/Show-TblStudents.aspx"
REDIRECT_URL = "https://sgs6.bopp-obec.info/sgss/TblStudentsInfo/Show-TblStudentsInfo-Table.aspx"

# ตั้งค่าบอทดิสคอร์ด
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

def safe_find_next_text(soup, label):
    """
    ค้นหา <td> ที่มีข้อความระบุ แล้วดึงข้อมูลใน <td> ถัดไป
    """
    cell = soup.find("td", text=label)
    if cell and cell.find_next_sibling("td"):
        return cell.find_next_sibling("td").text.strip()
    return None

def get_student_data(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(LOGIN_URL)

        # รอจนหน้าโหลดครบ
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # ใส่ Username และ Password
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "ctl00$PageContent$UserName"))
        ).send_keys(username)
        driver.find_element(By.NAME, "ctl00$PageContent$Password").send_keys(password)

        # พยายามคลิกปุ่ม "ตกลง"
        try:
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "ctl00_PageContent_OKButton__Button"))
            ).click()
        except TimeoutException:
            driver.execute_script(
                "WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions('ctl00$PageContent$OKButton$_Button', '', true, '', '', false, true))"
            )

        # ตรวจสอบว่าเปลี่ยนไปหน้า REDIRECT_URL หรือไม่
        WebDriverWait(driver, 30).until(
            lambda d: REDIRECT_URL in d.current_url
        )

        # Redirect ไปยัง STUDENT_INFO_URL
        driver.get(STUDENT_INFO_URL)

        # ใช้ BeautifulSoup วิเคราะห์ HTML ในหน้าที่ถูกเปลี่ยนเส้นทาง
        soup = BeautifulSoup(driver.page_source, "html.parser")
        student_id = safe_find_next_text(soup, "เลขประจำตัวนักเรียน")
        student_grade = safe_find_next_text(soup, "เข้าเรียนชั้น")
        student_first_name = safe_find_next_text(soup, "ชื่อ")
        student_last_name = safe_find_next_text(soup, "นามสกุล")

        if student_id and student_grade and student_first_name and student_last_name:
            return {
                "id": student_id,
                "grade": student_grade,
                "first_name": student_first_name,
                "last_name": student_last_name
            }
        else:
            raise ValueError("ไม่สามารถดึงข้อมูลนักเรียนได้ครบถ้วน")
    finally:
        driver.quit()

GUILD_ID = config["guild_id"]  # เพิ่มการโหลด GUILD_ID จาก config

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    # ตรวจสอบว่า Guild ID ถูกต้องหรือไม่
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print(f"Guild ID: {GUILD_ID} Not found! Please check config.json!")
    else:
        print(f"Bot ready at: {guild.name}")

@bot.slash_command(name="verify", description="ยืนยันตัวตนและเพิ่มยศตามชั้นเรียน")
async def verify(interaction: nextcord.Interaction, username: str, password: str):
    await interaction.response.defer(ephemeral=True)  # ตอบกลับแบบส่วนตัว

    try:
        student_data = get_student_data(username, password)
        if student_data:
            embed = nextcord.Embed(title="ยืนยันข้อมูลนักเรียน", color=0x00FF00)
            embed.add_field(name="เลขประจำตัว", value=student_data["id"], inline=False)
            embed.add_field(name="ชั้นเรียน", value=student_data["grade"], inline=False)
            embed.add_field(name="ชื่อ", value=student_data["first_name"], inline=True)
            embed.add_field(name="นามสกุล", value=student_data["last_name"], inline=True)
            embed.set_footer(text="กรุณากดยืนยันหากข้อมูลถูกต้อง")

            # ส่งข้อความ embed พร้อมกับ View แบบ ephemeral
            await interaction.followup.send(embed=embed, view=ConfirmView(student_data), ephemeral=True)
        else:
            await interaction.followup.send("ไม่สามารถดึงข้อมูลได้! กรุณาตรวจสอบชื่อผู้ใช้และรหัสผ่าน.", ephemeral=True)
    except ValueError as e:
        await interaction.followup.send(f"เกิดข้อผิดพลาด: {e}", ephemeral=True)


class ConfirmView(nextcord.ui.View):
    def __init__(self, student_data):
        super().__init__(timeout=False)
        self.student_data = student_data

    @nextcord.ui.button(label="ยืนยัน", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        guild = bot.get_guild(GUILD_ID)  # ดึง guild จาก GUILD_ID
        if not guild:
            await interaction.response.send_message("ไม่พบเซิร์ฟเวอร์ที่ระบุ!", ephemeral=True)
            return

        member = guild.get_member(interaction.user.id)
        if not member:
            await interaction.response.send_message("ไม่พบสมาชิกในเซิร์ฟเวอร์นี้!", ephemeral=True)
            return

        grade = self.student_data["grade"]
        role_id = ROLE_IDS.get(grade)
        if not role_id:
            await interaction.response.send_message(f"ไม่สามารถหายศสำหรับชั้นเรียน: {grade}", ephemeral=True)
            return

        # ดึง Role object จาก role_id
        role = get(guild.roles, id=role_id)
        if not role:
            await interaction.response.send_message("ไม่พบ Role ที่กำหนดไว้ใน config.json!", ephemeral=True)
            return

        try:
            # ใช้ add_roles() เพื่อเพิ่ม Role ให้กับสมาชิก
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ ยืนยันตัวตนสำเร็จ! เพิ่มยศ: {role.name}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ เกิดข้อผิดพลาดในการเพิ่ม Role: {e}", ephemeral=True)
            print(f"Error: {e}")


bot.run(TOKEN)