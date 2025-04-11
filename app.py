from flask import Flask, jsonify
import requests

# Criação da aplicação Flask
app = Flask(__name__)

#Cidades
weather_data_simulation = {
    "Curitiba": 12,
    "SaoPaulo": 25,
    "RioDeJaneiro": 32,
    "Brasilia": 28,
    "PortoAlegre": 18
}


# API B – Dados do Clima
@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    # Converte o nome da cidade
    city_title = city.title()
    
    # Busca a temperatura da cidade a partir do dicionário, ou usa 20 como valor padrão.
    temp = weather_data_simulation.get(city_title, 20)
    
    # Prepara o JSON de resposta com as informações do clima.
    response = {
        "city": city_title,
        "temp": temp,
        "unit": "Celsius"
    }
    
    return jsonify(response)


# API A – Recomendação Personalizada
@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    
    # Chama a função que retorna os dados de clima e converte a resposta em JSON.
    weather_response = get_weather(city)
    weather_json = weather_response.get_json()
    
    # Extrai a temperatura do JSON retornado.
    temp = weather_json.get("temp")
    
    # Gera a recomendação com base na temperatura.
    if temp > 30:
        suggestion = "Está quente. Recomenda-se hidratação e o uso de protetor solar."
    elif 15 < temp <= 30:
        suggestion = "O clima está agradável."
    else:  
        suggestion = "Está frio. Recomenda-se usar um casaco."
    
    # Prepara o JSON de resposta com as informações do clima e a recomendação.
    recommendation_response = {
        "city": weather_json.get("city", city.title()),
        "temperature": temp,
        "unit": "Celsius",
        "recommendation": suggestion
    }
    
    return jsonify(recommendation_response)


# Execução da Aplicação
if __name__ == '__main__':
    app.run(debug=True)
