from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import RedirectResponse
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "তোমার ডাউনলোডার চালু!"}

@app.post("/get-formats")
def get_formats(url: str = Form(...)):
    try:
        ydl_opts = {'quiet': True, 'simulate': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        formats = []
        for f in info.get('formats', []):
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                res = f.get('resolution') or f.get('format_note') or 'ভিডিও'
                formats.append({'format_id': f['format_id'], 'resolution': res})
        
        return {"title": info.get('title'), "formats": formats[:8]}
    except:
        raise HTTPException(400, "ভুল লিঙ্ক!")

@app.get("/download")
def download(url: str, format_id: str):
    ydl_opts = {'format': format_id, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return RedirectResponse(info['url'])
