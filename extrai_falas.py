import requests
from bs4 import BeautifulSoup
import pandas as pd


def adiciona_falas_de_reuniao(df_destino, url):
    df = pd.DataFrame()

    def adiciona_ao_csv(nome, partido, fala):
        df2 = pd.DataFrame({'Nome_Senador': [nome.strip()], 'Partido': [partido.strip()], 'Fala': [fala.strip()]})
        return pd.concat([df, df2], ignore_index=True)

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Não foi possível carregar a página')

    # Analisa o conteúdo HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')

    # TODO: Antes de ler as linhas, salvar dados do cabeçalho da reunião

    # Encontra todas as linhas da tabela que contêm informações do deputado
    linhas_falas = soup.find_all('div', class_='principalStyle')

    ultimo_nome = None
    ultimo_partido = None
    fala = ""

    for linha in linhas_falas:
        nome = linha.find('b')

        if(nome is not None):
            # Salvando ultimo senador
            if ultimo_nome and ultimo_partido:
                df = adiciona_ao_csv(ultimo_nome, ultimo_partido, fala)
            print(ultimo_nome, '--', ultimo_partido, '--', fala)

            ultimo_nome = nome.text
            fala = ""
            
            corpo_linha = linha.text.split(ultimo_nome)[1]

            partes_corpo = corpo_linha.split(') - ')

            ultimo_partido = partes_corpo[0].split('(')[1]
            fala += partes_corpo[1]
        else:
            fala += linha.text
    # Salvando ultimo senador
    df = adiciona_ao_csv(ultimo_nome, ultimo_partido, fala)
    print(ultimo_nome, '--', ultimo_partido, '--', fala)

    return pd.concat([df_destino, df], ignore_index=True)



def main():
    # URL da página
    # Ao invés de usar 1 url, percorrer lista de urls obtidas com selenium
    url = "https://www25.senado.leg.br/web/atividade/notas-taquigraficas/-/notas/s/25345#Quarto_9"

    df = pd.DataFrame()
    df = adiciona_falas_de_reuniao(df, url) # TODO: Tratar exceção caso url não for acessada
    df.to_csv('exemplo1.csv', index=False)


if __name__ == '__main__':
    main()
