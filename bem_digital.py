
import json
import os
import hashlib
import statistics
import secrets
import string
from datetime import date

ARQUIVO_JSON = "usuarios.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_JSON):
        return []
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(usuarios):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def gerar_senha_segura(tamanho=12):
    alfabeto = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alfabeto) for _ in range(tamanho))

def exibir_consentimento_lgpd():
    print("\nLGPD - Lei Geral de Proteção de Dados")
    print("Ao prosseguir com o cadastro, você concorda com o uso dos seus dados para fins educacionais.")
    consentimento = input("Você concorda? (S/N): ").strip().upper()
    return consentimento == "S"

def cadastrar_usuario():
    if not exibir_consentimento_lgpd():
        print("Cadastro cancelado por falta de consentimento.\n")
        return

    nome = input("Nome completo: ")
    usuario = input("Nome de usuário: ")
    senha = input("Crie uma senha (ou digite 'sugerir' para receber uma sugestão): ")
    if senha.lower() == "sugerir":
        senha = gerar_senha_segura()
        print(f"Sugestão de senha forte: {senha}")

    senha_hash = gerar_hash_senha(senha)
    idade = int(input("Idade: "))
    tempo_uso = int(input("Tempo médio de uso diário (em minutos): "))

    novo_usuario = {
        "nome": nome,
        "usuario": usuario,
        "senha_hash": senha_hash,
        "idade": idade,
        "tempo_uso": tempo_uso
    }

    usuarios = carregar_dados()
    usuarios.append(novo_usuario)
    salvar_dados(usuarios)
    print("Usuário cadastrado com sucesso!\n")

def login():
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    senha_hash = gerar_hash_senha(senha)

    usuarios = carregar_dados()
    for u in usuarios:
        if u["usuario"] == usuario and u["senha_hash"] == senha_hash:
            print(f"Bem-vindo, {u['nome']}!\n")
            return True
    print("Usuário ou senha incorretos.\n")
    return False

def listar_usuarios():
    usuarios = carregar_dados()
    if not usuarios:
        print("Nenhum usuário cadastrado.\n")
        return
    print("Lista de usuários cadastrados:")
    for i, u in enumerate(usuarios, 1):
        print(f"{i}. Nome: {u['nome']}, Idade: {u['idade']}, Tempo de uso: {u['tempo_uso']} minutos")
    print()

def gerar_estatisticas():
    usuarios = carregar_dados()
    if not usuarios:
        print("Nenhum dado para análise.\n")
        return

    idades = [u["idade"] for u in usuarios]
    tempos = [u["tempo_uso"] for u in usuarios]

    print("Estatísticas de Uso da Plataforma:")
    print(f"- Média de idade: {statistics.mean(idades):.2f} anos")
    print(f"- Moda de idade: {statistics.mode(idades)} anos")
    print(f"- Mediana de idade: {statistics.median(idades)} anos")
    print(f"- Média de tempo de uso: {statistics.mean(tempos):.2f} minutos")
    print(f"- Moda de tempo de uso: {statistics.mode(tempos)} minutos")
    print(f"- Mediana de tempo de uso: {statistics.median(tempos)} minutos\n")

def gerar_certificado():
    usuarios = carregar_dados()
    if not usuarios:
        print("Nenhum usuário cadastrado.\n")
        return

    print("Selecione o número do usuário para gerar o certificado:")
    for i, u in enumerate(usuarios, 1):
        print(f"{i}. {u['nome']}")

    try:
        escolha = int(input("Digite o número correspondente: "))
        usuario = usuarios[escolha - 1]
    except (IndexError, ValueError):
        print("Opção inválida.\n")
        return

    hoje = date.today().strftime("%d/%m/%Y")
    nome_arquivo = f"certificado_{usuario['usuario']}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"Certificado de Participação\n")
        f.write(f"\nConcedido a: {usuario['nome']}")
        f.write(f"\nData: {hoje}")
        f.write(f"\n\nA plataforma Bem Digital, em parceria com a ONG Amigos do Bem, certifica que o(a) participante concluiu as atividades de introdução à tecnologia e boas práticas digitais.\n")
        f.write(f"\nParabéns pela conquista!\n")

    print(f"Certificado gerado com sucesso: {nome_arquivo}\n")

def menu():
    while True:
        print("=== BEM DIGITAL - MENU PRINCIPAL ===")
        print("1. Cadastrar novo usuário")
        print("2. Fazer login")
        print("3. Listar usuários")
        print("4. Gerar estatísticas")
        print("5. Gerar certificado")
        print("6. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            login()
        elif opcao == "3":
            listar_usuarios()
        elif opcao == "4":
            gerar_estatisticas()
        elif opcao == "5":
            gerar_certificado()
        elif opcao == "6":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção inválida.\n")

if __name__ == "__main__":
    menu()
