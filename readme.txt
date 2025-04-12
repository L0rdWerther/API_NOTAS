# Web Scraping API for Banco Central do Brasil - Note Batch Validation

Projeto realizado durante estágio na seção de perícia documentoscópica na Polícia Civil do DF.

## How to Run

1. Open the terminal and navigate to the folder containing the script.
2. Run the following command:

python apinotas.py


## Testing with Postman

1. Open Postman.
2. Create a new request.
3. Select the **POST** method.
4. Enter the URL: `http://127.0.0.1:5000/pesquisa`.
5. Go to the **Body** tab, select **raw**, and then choose **JSON** (application/json).
6. Enter the following request body:

```json
{
"nota": 100,
"id_nota": "JI068640000"
}

    nota: The value you wish to search for.

    id_nota: The identification of the note.
