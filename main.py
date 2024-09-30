from flask import Flask, request, jsonify
import math
import pandas as pd

app = Flask(__name__)

# Função para calcular a diferença de cor usando a fórmula Delta E
def delta_e(lab1, lab2):
    L1, a1, b1, C1, h1 = lab1
    L2, a2, b2, C2, h2 = lab2
    delta_L = L1 - L2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_C = C1 - C2
    delta_h = h1 - h2
    return (delta_L ** 2 + delta_a ** 2 + delta_b ** 2 + delta_C ** 2 + delta_h ** 2) ** 0.5

# Função para encontrar a tinta mais próxima
def encontrar_tinta_desejada(lab_desejado, dados_tintas):
    menor_diferenca = float('inf')
    tinta_selecionada = None
    for _, row in dados_tintas.iterrows():
        lab_tinta = (float(row['L']), float(row['a']), float(row['b']), float(row['C']), float(row['h']))
        diferenca = delta_e(lab_desejado, lab_tinta)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            tinta_selecionada = row
    return tinta_selecionada

# Endpoint para cálculo
@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    lab_desejado = (data['L'], data['a'], data['b'], data['C'], data['h'])
    dados_tintas = pd.read_excel('dados_tintas.xlsx')  # substitua com o caminho correto
    tinta_selecionada = encontrar_tinta_desejada(lab_desejado, dados_tintas)

    if tinta_selecionada is not None:
        resposta = {
            'SAP': tinta_selecionada['SAP'],
            'descricao': tinta_selecionada['DESCRICAO'],
            'cor': tinta_selecionada['COR'],
            'tipo_verni': tinta_selecionada['TIPO DE VERNIZ']
        }
    else:
        resposta = {'erro': 'Nenhuma tinta encontrada'}

    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)
