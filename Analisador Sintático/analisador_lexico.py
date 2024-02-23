# LUCIANO PEREIRA DE OLIVEIRA FILHO e CASSIO ANDREZZA DE ALMEIDA

import re
import csv

# Expressões regulares para identificar os tokens
palavras_chave = r"\b(program|var|integer|real|boolean|procedure|begin|end|if|then|else|while|do|not)\b"
identificadores = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
inteiros = r"\b\d+\b"
reais = r"\b\d+\.\d*\b"
delimitadores = r"[;.:(),]"
atribuicao = r":="
relacionais = r"(=|<|>|<=|>=|<>)"
aditivos = r"(\+|-|or)"
multiplicativos = r"(\*|/|and)"
comentarios = r"(\{[^}]*\})|(\(\*[\s\S]*?\*\))"

def analisador_lexico(caminho_arquivo):
    tabela_simbolos = []
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
        conteudo = re.sub(comentarios, "", conteudo)  # Removendo comentários
        linhas = conteudo.split('\n')
        for numero_linha, linha in enumerate(linhas, 1):
            # Verificando tokens conhecidos
            for token in re.finditer(f"{palavras_chave}|{identificadores}|{inteiros}|{reais}|{delimitadores}|{atribuicao}|{relacionais}|{aditivos}|{multiplicativos}", linha):
                simbolo = token.group()  # Obtendo o token
                tipo_token = classificar_token(simbolo)  # Classificando o token
                tabela_simbolos.append([simbolo, tipo_token, numero_linha])  # Adicionando o token na tabela de símbolos
            
            # Verificando por caracteres ou sequências não reconhecidas
            linha_sem_tokens_conhecidos = re.sub(f"{palavras_chave}|{identificadores}|{inteiros}|{reais}|{delimitadores}|{atribuicao}|{relacionais}|{aditivos}|{multiplicativos}", "", linha)
            if not re.fullmatch(r"\s*", linha_sem_tokens_conhecidos):  # Se a linha sem os tokens conhecidos contém algo além de espaços em branco
                for nao_reconhecido in re.finditer(r"\S+", linha_sem_tokens_conhecidos):
                    tabela_simbolos.append([nao_reconhecido.group(), "Erro", numero_linha])
    return tabela_simbolos

# Classificação dos tokens
def classificar_token(token):
    if re.fullmatch(palavras_chave, token):
        return "Palavra reservada"
    elif re.fullmatch(identificadores, token):
        return "Identificador"
    elif re.fullmatch(inteiros, token):
        return "Número inteiro"
    elif re.fullmatch(reais, token):
        return "Número real"
    elif re.fullmatch(delimitadores, token):
        return "Delimitador"
    elif re.fullmatch(atribuicao, token):
        return "Atribuição"
    elif re.fullmatch(relacionais, token):
        return "Operador relacional"
    elif re.fullmatch(aditivos, token):
        return "Operador aditivo"
    elif re.fullmatch(multiplicativos, token):
        return "Operador multiplicativo"
    else:
        return "Erro"

# Exportando para CSV
def exportar_para_csv(tabela_simbolos, arquivo_saida):
    with open(arquivo_saida, 'w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['Token', 'Classificação', 'Linha'])
        escritor.writerows(tabela_simbolos)

def exportar_para_texto(tabela_simbolos, arquivo_saida):
    with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(f"{'Token':<20} {'Classificação':<20} {'Linha':<5}\n")
        arquivo.write("-" * 48 + "\n")

        for token, classificacao, linha in tabela_simbolos:
            arquivo.write(f"{token:<20} {classificacao:<20} {linha:<5}\n")

path = 'codigo.txt'
tabela_simbolos = analisador_lexico(path)
exportar_para_csv(tabela_simbolos, 'tabela_simbolos.csv')
exportar_para_texto(tabela_simbolos, 'tabela_simbolos.txt')
