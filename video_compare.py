import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

YOUTUBE_API_KEY = 'SUA_CHAVE_API_AQUI'
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/videos"

def get_video_data_from_api(video_id):
    url = f"{YOUTUBE_API_URL}?part=snippet,statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['statistics']
        else:
            raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    else:
        raise HTTPException(status_code=500, detail="Erro ao acessar a API do YouTube")

def get_video_data_from_scraping(video_url):
    response = requests.get(video_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        title = soup.find("meta", property="og:title")['content']
        views = soup.find("meta", itemprop="interactionCount")['content']
        return {"title": title, "viewCount": views}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao processar o vídeo com scraping")

def generate_comparison_chart(video1_data, video2_data):
    try:
        views = [int(video1_data.get('viewCount', 0)), int(video2_data.get('viewCount', 0))]
        likes = [int(video1_data.get('likeCount', 0)), int(video2_data.get('likeCount', 0))]
        comments = [int(video1_data.get('commentCount', 0)), int(video2_data.get('commentCount', 0))]

        print("Views:", views)
        print("Likes:", likes)
        print("Comments:", comments)

        fig, ax = plt.subplots(figsize=(10, 6))
        index = ['Video 1', 'Video 2']
        bar_width = 0.2
        opacity = 0.8

        rects1 = ax.bar(index, views, bar_width, alpha=opacity, color='b', label='Views')
        rects2 = ax.bar(index, likes, bar_width, alpha=opacity, color='g', label='Likes', bottom=views)
        rects3 = ax.bar(index, comments, bar_width, alpha=opacity, color='r', label='Comments', bottom=[i+j for i,j in zip(views, likes)])

        ax.set_xlabel('Videos')
        ax.set_ylabel('Counts')
        ax.set_title('Comparison of Video Statistics')
        ax.legend()

        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        return img_base64

    except Exception as e:
        print("Erro ao gerar o gráfico:", e)
        raise HTTPException(status_code=500, detail="Erro ao gerar o gráfico")

@app.get("/compare/")
def compare_videos(video1: str, video2: str):
    try:
        video1_data = get_video_data_from_api(video1)
    except HTTPException:
        video1_url = f"https://www.youtube.com/watch?v={video1}"
        video1_data = get_video_data_from_scraping(video1_url)

    try:
        video2_data = get_video_data_from_api(video2)
    except HTTPException:
        video2_url = f"https://www.youtube.com/watch?v={video2}"
        video2_data = get_video_data_from_scraping(video2_url)

    print("Dados do Vídeo 1:", video1_data)
    print("Dados do Vídeo 2:", video2_data)

    chart_image_base64 = generate_comparison_chart(video1_data, video2_data)

    return {
        "video1": video1_data,
        "video2": video2_data,
        "chart": chart_image_base64
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)