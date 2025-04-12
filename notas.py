import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import ttk

def checagem_nota(nota, id_nota):
    ministro_fazenda = ''
    presidente_banco_central = ''
    
    code = 0

    user_match = re.search(r'^([A-Z]{2})(\d{9})$', id_nota)
    if user_match and len(user_match.group(2)) == 9 and len(user_match.group(1)) == 2:
        user_letter = user_match.group(1)
        user_number = int(user_match.group(2))

        correct = False
        ministro_fazenda = ""
        presidente_banco_central = ""

        if nota == 2:
            url = "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=1"
        elif nota == 5:
            url = "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=2"
        elif nota == 10:
            url = "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=3"
        elif nota == 20:
            url = "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=4"
        elif nota == 50:
            url = "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=5"
        elif nota == 100:
            url = "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=6"
        elif nota == 200:
            url = "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=7"
        else:
            result_label.config(text="Nota não reconhecida.")
            return

        # Fazendo a requisição HTTP
        response = requests.get(url)

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Parseando o conteúdo HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Encontrando todas as tags <td> com a classe "aesquerda"
            td_elements = soup.find_all("td", class_="aesquerda")

            # Iterar sobre os elementos e extrair os dados desejados
            for i, td in enumerate(td_elements):
                match = re.search(r'([A-Z]{2})(\d{9}) a ([A-Z]{2})(\d{9})', td.text.strip())
                if match:
                    start_code = match.group(1)
                    start_number = int(match.group(2))
                    end_number = int(match.group(4))
                    if start_code == user_letter:
                        if start_number <= user_number <= end_number:
                            result_label.config(text=f"{td.text.strip()}")
                            correct = True
                            break

                # Checagem "Ministro da Fazenda", "Ministro da Economia" e "Presidente do Banco Central"
                if "Ministro da Fazenda" in td.text.strip() or "Ministro da Economia" in td.text.strip():
                    if "Ministro da Fazenda" in td.text.strip():
                        code = 1
                    if "Ministro da Economia" in td.text.strip():
                        code = 2
                    ministro_fazenda = td_elements[i + 1].text.strip()

                if "Presidente do Banco Central" in td.text.strip():
                    presidente_banco_central = td_elements[i + 1].text.strip()

            if not correct:
                result_label.config(text="Número fora do intervalo.")
            else:
                # Display additional information
                if ministro_fazenda:
                    if code == 1:
                        result_label.config(text=f"{result_label.cget('text')}\nMinistro da Fazenda: {ministro_fazenda}")
                    elif code == 2:
                        result_label.config(text=f"{result_label.cget('text')}\nMinistro da Economia: {ministro_fazenda}")
                if presidente_banco_central:
                    result_label.config(text=f"{result_label.cget('text')}\nPresidente do Banco Central: {presidente_banco_central}")

        else:
            result_label.config(text="Erro ao acessar o site. Verifique a URL ou sua conexão com a internet.")
    else:
        result_label.config(text="Número fora do intervalo.")

def tem():
    nota = int(nota_var.get())
    id_nota = id_entry.get()
    if nota == '' or id_nota == '':
        result_label.config(text="Insira nota e id da nota.")
        return
    else:
        checagem_nota(nota, id_nota)

# Tkinter GUI setup
root = tk.Tk()
root.title("Chancelador de nota")

nota_label = ttk.Label(root, text="Valor da nota:")
nota_label.pack(pady=5)

nota_var = tk.StringVar()
nota_entry = ttk.Entry(root, textvariable=nota_var)
nota_entry.pack(pady=5)

id_label = ttk.Label(root, text="ID da nota:")
id_label.pack(pady=5)

id_entry = ttk.Entry(root)
id_entry.pack(pady=5)

checagem_button = ttk.Button(root, text="Verificar", command=tem)
checagem_button.pack(pady=10)

result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()