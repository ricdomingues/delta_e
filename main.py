from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Dados diretamente no código, convertidos do CSV
dados_tintas = [
    {'VERNIZ': 'Brilho', 'SAP': 1079425.0, 'vL': 63.96, 'va': 17.94, 'vb': 44.7, 'vC': 48.16, 'vh': 68.13, 'local': '1*1*1'},
    {'VERNIZ': 'Brilho', 'SAP': 1117901.0, 'vL': 71.01, 'va': 17.64, 'vb': 53.0, 'vC': 55.86, 'vh': 71.59, 'local': '1*1*2'},
    {'VERNIZ': 'Brilho', 'SAP': None, 'vL': None, 'va': None, 'vb': None, 'vC': None, 'vh': None, 'local': '1*1*3'},
    {'VERNIZ': 'Brilho', 'SAP': 1186108.0, 'vL': 83.56, 'va': 2.44, 'vb': 25.11, 'vC': 25.23, 'vh': 84.44, 'local': '1*1*4'},
    {'VERNIZ': 'Brilho', 'SAP': 1220256.0, 'vL': 64.09, 'va': 6.26, 'vb': 37.34, 'vC': 37.86, 'vh': 80.49, 'local': '1*2*1'}
    # Adicione mais registros conforme necessário
]

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

# Função para encontrar a tinta mais próxima com base nos valores de L*a*b*C*h
def encontrar_tinta_desejada(lab_desejado):
    menor_diferenca = float('inf')
    tinta_selecionada = None

    for tinta in dados_tintas:
        # Ignorar tintas com valores nulos
        if None in (tinta['vL'], tinta['va'], tinta['vb'], tinta['vC'], tinta['vh']):
            continue
        lab_tinta = (tinta['vL'], tinta['va'], tinta['vb'], tinta['vC'], tinta['vh'])
        diferenca = delta_e(lab_desejado, lab_tinta)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            tinta_selecionada = tinta

    return tinta_selecionada

# Endpoint para calcular a tinta ideal com base nos valores fornecidos
@app.route('/calculate', methods=['POST'])
def calcular():
    data = request.json
    lab_desejado = (data['L'], data['a'], data['b'], data['C'], data['h'])
    
    tinta_selecionada = encontrar_tinta_desejada(lab_desejado)

    if tinta_selecionada:
        resposta = {
            'SAP': tinta_selecionada['SAP'],
            'local': tinta_selecionada['local'],
            'verniz': tinta_selecionada['VERNIZ']
        }
    else:
        resposta = {'erro': 'Nenhuma tinta encontrada'}

    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)

