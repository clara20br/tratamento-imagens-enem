"""
Propósito: concatenar verticalmente as imagens de cada pasta vinda do passo 5
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "divididas-sem-bordas-do-meio" do passo 5 para essa pasta do passo 6
OBS2: não compensa concatenar as páginas inteiras. Tenha isso em mente para o passo 7
"""

"""
Propósito: Concatenar verticalmente as páginas inteiras da prova do ENEM
Autor: Adaptado para ENEM (Página Única)
"""

from PIL import Image
import os
import re

# Substitua pelo nome real da pasta onde estão as suas páginas processadas
pasta_imagens = "divididas-sem-bordas-do-meio" 
pasta_saida = "."
os.makedirs(pasta_saida, exist_ok=True)

def get_sort_key(nome_arquivo):
    """
    Extrai o número da página (ex: 'pagina_enem_5.jpg' -> 5) 
    para garantir que a ordenação seja numérica e não alfabética.
    """
    busca = re.search(r'pagina_enem_(\d+)', nome_arquivo)
    if busca:
        return int(busca.group(1))
    return 0  # Caso o arquivo não siga o padrão, vai para o início

# Captura arquivos .png, .jpg ou .jpeg
formatos_suportados = ('.png', '.jpg', '.jpeg')
arquivos = [f for f in os.listdir(pasta_imagens) if f.lower().endswith(formatos_suportados)]

# Ordena as páginas de forma crescente (1, 2, 3... 10, 11...)
arquivos.sort(key=get_sort_key)

if not arquivos:
    print(f"Nenhuma imagem encontrada na pasta '{pasta_imagens}'!")
    exit()

# Abrir todas as imagens na ordem correta
imagens = []
for arquivo in arquivos:
    caminho = os.path.join(pasta_imagens, arquivo)
    imagens.append(Image.open(caminho))
    print(f"Adicionando na fila: {arquivo}")

# Encontrar a largura máxima para o fundo da colagem
largura_max = max(img.width for img in imagens)

# Calcular a altura total somando todas as páginas
altura_total = sum(img.height for img in imagens)

# Cria o canvas final em branco (fundo branco para o ENEM)
imagem_final = Image.new('RGB', (largura_max, altura_total), color=(255, 255, 255))

# Cola uma imagem abaixo da outra
y = 0
for img in imagens:
    # Centraliza horizontalmente caso alguma página tenha largura ligeiramente menor
    x_offset = (largura_max - img.width) // 2
    imagem_final.paste(img, (x_offset, y))
    y += img.height

# Salva o resultado final que será usado no Passo 7
caminho_final = os.path.join(pasta_saida, 'colunas_concatenadas_verticalmente.png')
imagem_final.save(caminho_final)

print("\n--- Processo Concluído! ---")
print(f"Imagens concatenadas verticalmente com sucesso em: {caminho_final}")
print(f"Total de páginas unidas: {len(arquivos)}")