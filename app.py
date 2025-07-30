"""
api_key : https://finnhub.io/dashboard

"""
import gradio as gr

# from langchain.tools import tool ## lancghain agent sisteminde kullanilacak fonksiyonlari tanimlamak icin
import requests 
import os 
from dotenv import load_dotenv

load_dotenv() # .env dosyasini yukleyerek icerisindeki api anahtarini erisilebilir hale getirir 


def get_stock_info(ticker:str) -> str : 
    """
        bir hisse senedi sembolu(orn: AAPL) icin guncel fiyat bilgisi doner 
        Parametre: 
            ticker (str): hisse senedinin sembolu(orn:"AAPL",  "GOOGL")
        Output:
            str : guncel hisse bilgilerini iceren metin 
    """
    try: 
        # .env dosyasindan Finnhub api anahtarini al 
        api_key = os.getenv("FINNHUB_API_KEY")

        # eger api anahtari yoksa kullaniciya hata mesaji return et 
        if not api_key : 
            return "API anahtari bulunamadi."

        ## Finnhub api'den belirli bir hisse senedi icin fiyat bilgilerini alan url tanimla 
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"

        # api'ye get istegi gonder 
        response = requests.get(url)

        # eger istek basarisiz ise 
        if response.status_code !=200:
            return f"API hatasi: {response.status_code}"
        
        # API'den gelen yaniti coz 
        data = response.json()

        # json icinden guncel fiyat(c) , acilis fiyati(o) , en yuksek fiyat(h) , en dusuk fiyat(l)
        current = data.get("c") ## current price 
        open_ = data.get("o") # opening price 
        high = data.get("h") # day's highest price
        low = data.get("l") # day's lowest price

        return (
            f"{ticker} Hisse Bilgisi: \n"
            f"- Guncel Fiyat: {current} USD \n" 
            f"- Açılış: {open_} USD \n" 
            f"- Gun ici en yüksek: {high} USD \n"
            f"- Gun ici en dusuk: {low} USD \n"
        )
    except Exception as e : 
        return f"Hata olustu: {e}"

with gr.Blocks(theme = gr.themes.Soft()) as demo: 
    gr.HTML("""
    <div style = 'text-align: center; '> 
    <h2>🤖 Hisse Senedi Bilgi Asistanı </h2> 
    </div>
    """)
    with gr.Row():
        with gr.Column():
            ticker = gr.Textbox(label = "Hisse Senedi Adı") 
            submit_btn = gr.Button("Hisse Bilgi Al")
            clear_btn = gr.Button("Temizle")
        with gr.Column():
            output = gr.Textbox(label = "Output")

    submit_btn.click(
        get_stock_info, # function
        [ticker] ,  # inputs
        [output] # output
    ) 

    clear_btn.click(
        lambda : (None , None) , 
        [], 
        [ticker,output]
    )

if __name__ == "__main__":
    # print(get_stock_info.run({"ticker" : "GOOGL"}))
    demo.launch(show_error = True)