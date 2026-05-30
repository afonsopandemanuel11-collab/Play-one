import os
import psycopg2
from psycopg2 import Error

def conectar_banco():
    try:
        conexao = psycopg2.connect(
            host="localhost",
            port="5432",
            database="reprodutor_filmes",
            user="postgres",
            password="emir"
        )
        return conexao
    except Error as e:
        print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
        return None
def cadastrar_filme():
    print("\n--- CADASTRAR NOVO FILME ---")
    titulo = input("Título do Filme: ")
    genero = input("Género: ")
    ano = input("Ano de Lançamento: ")
    caminho = input("Caminho completo do arquivo (ex: C:/Filmes/video.mp4): ")

    conexao = conectar_banco()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando = "INSERT INTO filmes (titulo, genero, ano, caminho_arquivo) VALUES (%s, %s, %s, %s);"
            cursor.execute(comando, (titulo, genero, ano, caminho))
            conexao.commit()
            print(f"🎉 '{titulo}' cadastrado com sucesso!")
        except Error as e:
            print(f"Erro ao inserir: {e}")
        finally:
            cursor.close()
            conexao.close()

def listar_e_reproduzir():
    conexao = conectar_banco()
    if not conexao:
        return

    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, genero, ano, caminho_arquivo FROM filmes;")
    filmes = cursor.fetchall()
    
    cursor.close()
    conexao.close()

    if not filmes:
        print("\nNenhum filme cadastrado ainda.")
        return

    print("\n--- FILMES DISPONÍVEIS ---")
    for filme in filmes:
        print(f"[{filme[0]}] {filme[1]} ({filme[3]}) - {filme[2]}")

    try:
        escolha = int(input("\nDigite o ID do filme para dar PLAY (ou 0 para voltar): "))
        if escolha == 0:
            return

        # Encontrar o filme escolhido
        filme_selecionado = next((f for f in filmes if f[0] == escolha), None)

        if filme_selecionado:
            caminho_video = filme_selecionado[4]
            
            if os.path.exists(caminho_video):
                print(f"🎬 Reproduzindo: {filme_selecionado[1]}... Aproveite a pipoca!")
                # Abre o arquivo no player padrão do sistema (Windows, Mac ou Linux)
                if os.name == 'nt': # Windows
                    os.startfile(caminho_video)
                else: # Mac ou Linux
                    os.system(f'xdg-open "{caminho_video}" 2>/dev/null || open "{caminho_video}"')
            else:
                print("❌ Erro: Arquivo de vídeo não encontrado no caminho especificado.")
        else:
            print("ID inválido.")
    except ValueError:
        print("Por favor, digite um número válido.")

def menu():
    while True:
        print("\n=============================")
        print("   MINI REPRODUTOR KUZOLA    ")
        print("=============================")
        print("1. Cadastrar Filme")
        print("2. Ver Filmes e Dar Play")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_filme()
        elif opcao == "2":
            listar_e_reproduzir()
        elif opcao == "3":
            print("Até à próxima! 👋")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()