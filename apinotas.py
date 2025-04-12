import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/pesquisa", methods=["POST"])
def pesquisa():
    data = request.get_json()
    nota = data.get("nota")
    id_nota = data.get("id_nota")
    
    if nota is None or id_nota is None:
        return jsonify({"error": "Nota and id_nota are required fields."}), 400
    
    resultados = checagem_nota(nota, id_nota)

    return jsonify(resultados), 200


def checagem_nota(nota, id_nota):
    results = {
        "valid": False,
        "details": None,
        "error": None
    }

    nota_urls = {
        2: "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=1",
        5: "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=2",
        10: "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=3",
        20: "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=4",
        50: "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=5",
        100: "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=6",
        200: "https://www3.bcb.gov.br/mec-chancela/?Familia=9&Denominacao=7"
    }

    if nota not in nota_urls:
        results["error"] = "Nota não reconhecida."
        return results

    user_match = re.match(r'^([A-Z]{2})(\d{9})$', id_nota)
    if not user_match:
        results["error"] = "Número fora do intervalo."
        return results

    user_letter, user_number = user_match.groups()
    user_number = int(user_number)
    url = nota_urls[nota]

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        results["error"] = "Erro ao acessar o site. Verifique a URL ou sua conexão com a internet."
        return results

    soup = BeautifulSoup(response.content, "html.parser")
    td_elements = soup.find_all("td", class_="aesquerda")

    for i, td in enumerate(td_elements):
        match = re.search(r'([A-Z]{2})(\d{9}) a ([A-Z]{2})(\d{9})', td.text.strip())
        if match:
            start_code, start_number, _, end_number = match.groups()
            start_number = int(start_number)
            end_number = int(end_number)
            if start_code == user_letter and start_number <= user_number <= end_number:
                results["valid"] = True
                results["details"] = td.text.strip()
                break
        if "Ministro da Fazenda" in td.text.strip() or "Ministro da Economia" in td.text.strip():
            results["ministro_fazenda_economia"] = td_elements[i + 1].text.strip()
        if "Presidente do Banco Central" in td.text.strip():
            results["presidente_banco_central"] = td_elements[i + 1].text.strip()

    if not results["valid"]:
        results["error"] = "Número fora do intervalo."

    return results


if __name__ == "__main__":
    app.run(host='10.93.49.83', port=5000, debug=True)
