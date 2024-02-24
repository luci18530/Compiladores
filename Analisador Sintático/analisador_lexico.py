import re
import csv

# Expressões regulares para identificar os tokens
palavras_chave = r"\b(program|var|integer|real|boolean|procedure|begin|end|if|then|else|while|do|not)\b"
identificadores = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
reais = r"\b\d+\.\d+\b"
inteiros = r"\b\d+\b"
delimitadores = r"[;.,()]"  # ':' foi movido para ser tratado junto com ':='
atribuicao = r":="  # Garante que ':=' seja capturado corretamente
relacionais = r"(=|<|>|<=|>=|<>)"
aditivos = r"(\+|-|or)"
multiplicativos = r"(\*|/|and)"
comentarios = r"(\{[^}]*\})|(\(\*[\s\S]*?\*\))"

# Ajustando a função de classificação de token
def classificar_token(token):
    if re.fullmatch(palavras_chave, token):
        return "Palavra reservada"
    elif re.fullmatch(identificadores, token):
        return "Identificador"
    elif re.fullmatch(inteiros, token):
        return "Número inteiro"
    elif re.fullmatch(reais, token):
        return "Número real"
    elif token == ":":
        return "Delimitador"  # Trata ':' explicitamente como delimitador
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

def analisador_lexico(caminho_arquivo):
    tabela_simbolos = []
    with open(caminho_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
        conteudo = re.sub(comentarios, "", conteudo)  # Removendo comentários
        linhas = conteudo.split('\n')
        for numero_linha, linha in enumerate(linhas, 1):
            linha_processada = linha
            for token in re.finditer(f"{atribuicao}|{palavras_chave}|{identificadores}|{reais}|{inteiros}|[:]|{delimitadores}|{relacionais}|{aditivos}|{multiplicativos}", linha):
                simbolo = token.group()
                tipo_token = classificar_token(simbolo)
                tabela_simbolos.append([simbolo, tipo_token, numero_linha])
                linha_processada = linha_processada.replace(simbolo, '', 1)

            # Verificação de caracteres não reconhecidos
            linha_processada = linha_processada.strip()
            if linha_processada:  # Se sobrar algo na linha, então é um erro
                for caractere in linha_processada:
                    if not caractere.isspace():  # Ignora espaços
                        tabela_simbolos.append([caractere, "Erro", numero_linha])

    exportar_para_texto(tabela_simbolos, 'tabela_simbolos.txt')
    return tabela_simbolos

# Exportando para CSV
def exportar_para_csv(tabela_simbolos, arquivo_saida):
    with open(arquivo_saida, 'w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(['Token', 'Classificação', 'Linha'])
        escritor.writerows(tabela_simbolos)

def exportar_para_texto(tabela_simbolos, arquivo_saida):
    try:
        with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
            arquivo.write(f"{'Token':<20} {'Classificação':<20} {'Linha':<5}\n")
            arquivo.write("-" * 48 + "\n")

            for token, classificacao, linha in tabela_simbolos:
                arquivo.write(f"{token:<20} {classificacao:<20} {linha:<5}\n")
        print(f"Arquivo {arquivo_saida} exportado com sucesso.")
    except Exception as e:
        print(f"Erro ao exportar para texto: {e}")

    

    


        


