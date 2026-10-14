import requests
import asyncio
from datetime import datetime
from telegram import Bot

TOKEN = "xd:cxd-E-AZtyqsM"
CHAT_ID = "xd"
URL = "https://thebox.com.pe/products/zapatillas-para-hombre-veja-campo-cp0501537-m-wht.json"
TALLA_OBJETIVO = "42"

async def enviar_telegram(mensaje):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=mensaje)
    print("Mensaje enviado a Telegram!")

def verificar_talla():
    try:
        response = requests.get(URL, timeout=10)
        data = response.json()
        variantes = data["product"]["variants"]
        
        for variante in variantes:
            if variante["title"] == TALLA_OBJETIVO:
                disponible = variante["available"]
                precio = variante["price"]
                print(f"{datetime.now().strftime('%H:%M')} — Talla {TALLA_OBJETIVO}: {'DISPONIBLE' if disponible else 'agotada'} | S/{precio}")
                return disponible
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

async def main():
    print("Monitor iniciado!")
    print(f"Buscando talla {TALLA_OBJETIVO} en VEJA Campo")
    print("-" * 40)
    
    alerta_enviada = False
    await enviar_telegram("Monitor iniciado! Te avisare cuando la talla 42 este disponible.")
    
    while True:
        disponible = verificar_talla()
        
        if disponible and not alerta_enviada:
            await enviar_telegram(
                "JAMPIER CORRE!\n\n"
                "Las zapatillas VEJA Campo talla 42 estan disponibles!\n\n"
                "Compra aqui: https://thebox.com.pe/products/zapatillas-para-hombre-veja-campo-cp0501537-m-wht\n\n"
                "Ve rapido antes de que se agoten!"
            )
            alerta_enviada = True
        
        if not disponible:
            alerta_enviada = False
        
        await asyncio.sleep(1800)

asyncio.run(main())
