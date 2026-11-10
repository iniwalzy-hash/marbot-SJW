# plugins/sholat.py
import cs_bot
from cs_bot import MessageSession
import requests
from datetime import datetime

# ID Kota Sleman di API MyQuran/Kemenag
SLEMAN_CITY_ID = "1217" 

# Dictionary sementara untuk menyimpan status reminder pengguna (Key: user_id, Value: True/False)
reminder_users = set()

@cs_bot.on_keyword(["/start"])
def cmd_start(sess: MessageSession):
    pesan = (
        "🤖 **Selamat datang di Bot Jadwal Sholat Sleman, Yogyakarta!**\n\n"
        "Gunakan perintah berikut:\n"
        "• `/jadwal` - Melihat jadwal sholat hari ini di wilayah Sleman\n"
        "• `/setreminder` - Mengaktifkan pengingat sholat otomatis\n"
        "• `/unsetreminder` - Menonaktifkan pengingat sholat otomatis"
    )
    sess.reply(pesan)

@cs_bot.on_keyword(["/jadwal"])
def cmd_jadwal(sess: MessageSession):
    try:
        tanggal_hari_ini = datetime.now().strftime("%Y/%m/%d")
        url = f"https://api.myquran.com/v2/sholat/jadwal/{SLEMAN_CITY_ID}/{tanggal_hari_ini}"
        
        response = requests.get(url)
        data = response.json()
        
        if data.get("status"):
            jadwal = data["data"]["jadwal"]
            pesan = (
                f"🕌 **Jadwal Sholat Sleman & Sekitarnya**\n"
                f"📅 Tanggal: {jadwal['tanggal']}\n\n"
                f"• Imsak: {jadwal['imsak']}\n"
                f"• Subuh: {jadwal['subuh']}\n"
                f"• Terbit: {jadwal['terbit']}\n"
                f"• Dhuha: {jadwal['dhuha']}\n"
                f"• Dzuhur: {jadwal['dzuhur']}\n"
                f"• Ashar: {jadwal['ashar']}\n"
                f"• Maghrib: {jadwal['maghrib']}\n"
                f"• Isya: {jadwal['isya']}"
            )
        else:
            pesan = "❌ Gagal mengambil data jadwal sholat saat ini."
    except Exception as e:
        pesan = f"⚠️ Terjadi kesalahan sistem: {str(e)}"
        
    sess.reply(pesan)

@cs_bot.on_keyword(["/setreminder"])
def cmd_set_reminder(sess: MessageSession):
    user_id = sess.get_user_id()
    if user_id in reminder_users:
        pesan = "⚠️ Pengingat sholat untuk Anda sudah aktif sebelumnya."
    else:
        reminder_users.add(user_id)
        pesan = (
            "✅ **Berhasil Mengaktifkan Reminder!**\n"
            "Anda akan menerima notifikasi pengingat otomatis ketika memasuki waktu sholat di wilayah Sleman."
        )
    sess.reply(pesan)

@cs_bot.on_keyword(["/unsetreminder"])
def cmd_unset_reminder(sess: MessageSession):
    user_id = sess.get_user_id()
    if user_id in reminder_users:
        reminder_users.remove(user_id)
        pesan = (
            "🔕 **Berhasil Menonaktifkan Reminder!**\n"
            "Anda tidak akan lagi menerima notifikasi pengingat otomatis waktu sholat."
        )
    else:
        pesan = "⚠️ Anda belum mengaktifkan pengingat sholat sebelumnya. Gunakan `/setreminder` untuk mengaktifkannya."
    sess.reply(pesan)