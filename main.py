import flet as ft
import requests

BACKEND_URL = "http://127.0.0.1:8000/compare/"

def main(page):
    page.title = "YouTube Video Comparator"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Função para capturar os links e enviar a requisição ao backend
    def compare_videos(e):
        video_link1 = link1.value
        video_link2 = link2.value

        if not video_link1 or not video_link2:
            result_label.value = "Por favor, insira os links de ambos os vídeos."
            page.update()
            return
        
        video_id1 = video_link1.split("v=")[-1]
        video_id2 = video_link2.split("v=")[-1]

        try:
            response = requests.get(BACKEND_URL, params={"video1": video_id1, "video2": video_id2})
            response.raise_for_status()
            data = response.json()

            # Acesse diretamente os dados retornados
            video1_stats = data["video1"]
            video2_stats = data["video2"]

            result_label.value = f"""
            Comparação dos vídeos:
            - Vídeo 1:
                Visualizações: {video1_stats.get('viewCount', 'N/A')}
                Curtidas: {video1_stats.get('likeCount', 'N/A')}
                Comentários: {video1_stats.get('commentCount', 'N/A')}
                
            - Vídeo 2:
                Visualizações: {video2_stats.get('viewCount', 'N/A')}
                Curtidas: {video2_stats.get('likeCount', 'N/A')}
                Comentários: {video2_stats.get('commentCount', 'N/A')}
            """
            
            # Exibir o gráfico
            chart_image_base64 = data.get("chart", "")
            if chart_image_base64:
                chart_image.src_base64 = chart_image_base64
                chart_image.visible = True

        except requests.exceptions.RequestException as err:
            result_label.value = f"Erro ao comparar vídeos: {err}"

        page.update()

    # Campos de texto para inserir os links dos vídeos
    link1 = ft.TextField(label="Link do Vídeo 1", width=400)
    link2 = ft.TextField(label="Link do Vídeo 2", width=400)

    # Botão para acionar a comparação
    compare_button = ft.ElevatedButton(text="Comparar", on_click=compare_videos, width=200)
    
    # Label para exibir os resultados ou mensagens de erro
    result_label = ft.Text(value="Insira os links dos vídeos e clique em Comparar", width=800)
    
    # Imagem do gráfico de comparação
    chart_image = ft.Image(src_base64="", visible=False, width=800, height=400)

    # Layout
    page.add(
        ft.Column(
            controls=[
                ft.Text(value="Comparador de Vídeos do YouTube", size=24, weight="bold"),
                ft.Divider(),  # Separador

                # Linha com os campos de texto
                ft.Row(
                    controls=[
                        link1,
                        link2,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    wrap=True
                ),

                # Botão e rótulo de resultados
                compare_button,
                result_label,
                chart_image
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )

ft.app(target=main)