# /util/imageUtil.py
from PIL import Image

def transformar_em_quadrada(imagem_original, tamanho_maximo = 480):  
    # captura largura e altura da imagem original  
    largura, altura = imagem_original.size
    # obtém a menor das arestas (altura ou largura)
    tamanho_quadrado = min(largura, altura)    
    # cria uma imagem quadrada branca com lado 
    # do tamanho da menor aresta
    imagem_quadrada = Image.new('RGB', (tamanho_quadrado, tamanho_quadrado), (255, 255, 255))
    # computa o deslocamento vertical ou horizontal para
    # centralizar a imagem original na imagem quadrada
    x_offset = (tamanho_quadrado - largura) // 2
    y_offset = (tamanho_quadrado - altura) // 2
    # cola a imagem original na imagem quadrada considerando
    # os deslocamentos computados acima
    imagem_quadrada.paste(imagem_original, (x_offset, y_offset))
    # caso o lado da imagem quadrada seja maior que o tamanho máximo
    if imagem_quadrada.size[0] > tamanho_maximo:
        # redimensiona a imagem para que seu lado tenha o tamanho máximo
        imagem_quadrada = imagem_quadrada.resize((tamanho_maximo, tamanho_maximo), Image.Resampling.LANCZOS)
    # retorna a imagem quadrada e redimensionada (quando necessário)
    return imagem_quadrada


from PIL import Image, ImageDraw

def transformar_círculo(imagem_original, tamanho_maximo=480):
    # Captura largura e altura da imagem original
    largura, altura = imagem_original.size

    # Obtém a menor das arestas (altura ou largura)
    tamanho_menor = min(largura, altura)

    # Cria uma imagem circular branca com raio igual à metade da menor aresta
    imagem_circular = Image.new('RGB', (tamanho_menor, tamanho_menor), (255, 255, 255))
    draw = ImageDraw.Draw(imagem_circular)

    # Desenha um círculo preto no fundo branco
    draw.ellipse([(0, 0), (tamanho_menor, tamanho_menor)], fill=(0, 0, 0))

    # Calcula o deslocamento vertical ou horizontal para centralizar a imagem original no círculo
    x_offset = (tamanho_menor - largura) // 2
    y_offset = (tamanho_menor - altura) // 2

    # Cola a imagem original no círculo considerando os deslocamentos computados acima
    imagem_circular.paste(imagem_original, (x_offset, y_offset), mask=imagem_original)

    # Caso o raio do círculo seja maior que o tamanho máximo
    if tamanho_menor > tamanho_maximo:
        # Redimensiona o círculo para que seu raio seja igual ao tamanho máximo
        novo_raio = tamanho_maximo // 2
        imagem_circular = imagem_circular.resize((novo_raio * 2, novo_raio * 2), Image.Resampling.LANCZOS)

    # Retorna a imagem circular e redimensionada (quando necessário)
    return imagem_circular

from PIL import Image
# Importe a função transformar_círculo aqui, se não tiver sido feito anteriormente

def renderizar_imagem_usuario(usuario):
    caminho_imagem = f"/static/imagens/usuarios/{usuario.id}_img.jpg"

    # Abre a imagem original
    imagem_original = Image.open(caminho_imagem)

    # Aplica a transformação circular
    imagem_circular = transformar_círculo(imagem_original)

    # Salva a imagem transformada em um novo arquivo
    caminho_imagem_transformada = f"/static/imagens/usuarios/{usuario.id}_img_circular.jpg"
    imagem_circular.save(caminho_imagem_transformada)

    # Retorna o caminho da imagem transformada para ser usado no HTML
    return caminho_imagem_transformada
