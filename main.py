# main.py
import cs_bot
from cs_bot import StartupConfig
from cs_bot.adapters import sop_bot

# Konfigurasi menggunakan App ID dan App Secret dari kredensial Anda
# Catatan: Signing Secret bisa didapatkan di menu Event Callback pada portal SeaTalk Open Platform Anda
config = {
    "adapter": {
        "app_id": "NDAwNzUwNzc4MDMgMDg4", 
        "app_secret": "Vi_qJVS4fs2JdO1oWnCxXLnRftq_-WY",
        "signing_secret": "MASUKKAN_SIGNING_SECRET_ANDA_DI_SINI"
    }
}

cs_bot.init(StartupConfig.parse_obj(config))

# Memuat plugin jadwal sholat
cs_bot.load_plugin("plugins.sholat")

if __name__ == '__main__':
    # Dijalankan pada port default (bisa disesuaikan dengan platform hosting Anda)
    cs_bot.run(host="0.0.0.0", port=8080)