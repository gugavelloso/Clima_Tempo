from flask import Flask, jsonify
import requests


# Criação da aplicação Flask.
app = Flask(__name__)

# Criação da API B - Dados do Clima
@app.route('/weather/<city>', methods=['GET'])

def recommendation(city):
    """
    Consulta a API B para obter os dados do clima e gera uma recomendação
    personalizada com base na temperatura retornada.
    """
    try:
        # Constrói a URL para chamar a API B.
        # Como ambas as APIs estão na mesma aplicação, usamos localhost na porta 5000.
        url = f"http://localhost:5000/weather/{city}"
        weather_response = requests.get(url)
        
        # Caso a API B não responda com status 200 (OK), retorna um erro.
        if weather_response.status_code != 200:
            return jsonify({"error": "Erro ao obter dados de clima."}), 500
        
        # Converte a resposta para JSON.
        weather_data = weather_response.json()
    except Exception as e:
        # Em caso de exceção (por exemplo, se a API B não estiver disponível), retorna um erro.
        return jsonify({"error": "Exceção ao conectar com API B.", "details": str(e)}), 500

    # Extrai a temperatura do JSON retornado.
    temp = weather_data.get("temp", None)
    
    # Se por algum motivo o dado de temperatura não existir, retorna um erro.
    if temp is None:
        return jsonify({"error": "Dados de clima incompletos."}), 500

    # Gera a recomendação com base na temperatura.
    if temp > 30:
        suggestion = "Está quente. Recomenda-se hidratação e o uso de protetor solar."
    elif 15 < temp <= 30:
        suggestion = "O clima está agradável."
    else:  # temp <= 15
        suggestion = "Está frio. Recomenda-se usar um casaco."

    # Prepara o JSON de resposta contendo a cidade, a temperatura, a unidade e a recomendação.
    recommendation_data = {
        "city": weather_data.get("city", city),
        "temperature": temp,
        "unit": "Celsius",
        "recommendation": suggestion
    }

    # Retorna os dados em formato JSON.
    return jsonify(recommendation_data)

# ---------------------------
# Execução da Aplicação
# ---------------------------
# A aplicação será iniciada no localhost na porta 5000 com o modo debug ativo.
if __name__ == '__main__':
    app.run(debug=True)





