from analisador_lexico import analisador_lexico
from PascalParser import PascalParser

def main():
    path = 'tests/Test1.pas'
    tokens = analisador_lexico(path)

    tokens_para_analise = [
    {'Token': token[0], 'Classificação': token[1], 'Linha': token[2]}
    for token in tokens]

    parser = PascalParser(tokens_para_analise)
    try:
        parser.parse()
        print("Análise sintática concluída com sucesso.")
    except SyntaxError as e:
        print(f"Erro de sintaxe: {e}")

if __name__ == "__main__":
    main()

