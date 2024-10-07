from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Dados diretamente no código, convertidos do CSV
dados_tintas = [
    {'VERNIZ': None, 'SAP': 1079425, 'vL': 63.96, 'va': 17.94, 'vb': 44.7, 'vC': 48.16, 'vh': 68.13, 'local': '1.1.1'},
    {'VERNIZ': None, 'SAP': 1117901, 'vL': 71.01, 'va': 17.64, 'vb': 53.0, 'vC': 55.86, 'vh': 71.59, 'local': '1.1.2'},
    {'VERNIZ': None, 'SAP': 1186108, 'vL': 83.56, 'va': 2.44, 'vb': 25.11, 'vC': 25.23, 'vh': 84.44, 'local': '1.1.4'},
    {'VERNIZ': None, 'SAP': 1220256, 'vL': 64.09, 'va': 6.26, 'vb': 37.34, 'vC': 37.86, 'vh': 80.49, 'local': '1.2.1'}
]

# Função para calcular a diferença de cor usando a fórmula Delta E
def delta_e(lab1, lab2):
    L1, a1, b1, C1, h1 = lab1
    L2, a2, b2, C2, h2 = lab2
    
    # Calcular as diferenças
    delta_L = float(L1) - float(L2)
    delta_a = float(a1) - float(a2)
    delta_b = float(b1) - float(b2)
    delta_C = float(C1) - float(C2)
    delta_h = float(h1) - float(h2)
    
    # Retornar a diferença total calculada
    return math.sqrt(delta_L ** 2 + delta_a ** 2 + delta_b ** 2 + delta_C ** 2 + delta_h ** 2)

# Função para encontrar a tinta mais próxima com base nos valores de L*a*b*C*h
def encontrar_tinta_desejada(lab_desejado):
    menor_diferenca = float('inf')
    tinta_selecionada = None

    for tinta in dados_tintas:
        # Ignorar tintas com valores nulos
        if None in (tinta['vL'], tinta['va'], tinta['vb'], tinta['vC'], tinta['vh']):
            continue
        lab_tinta = (float(tinta['vL']), float(tinta['va']), float(tinta['vb']), float(tinta['vC']), float(tinta['vh']))
        diferenca = delta_e(lab_desejado, lab_tinta)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            tinta_selecionada = tinta

    return tinta_selecionada

# Endpoint para calcular a tinta ideal com base nos valores fornecidos
@app.route('/calculate', methods=['POST'])
def calcular():
    # Captura os dados JSON da requisição
    data = request.json
    
    # Extrai os valores de L, a, b, C e h
    try:
        lab_desejado = (float(data['L']), float(data['a']), float(data['b']), float(data['C']), float(data['h']))
    except KeyError as e:
        return jsonify({'erro': f'Parâmetro faltando: {str(e)}'}), 400
    except ValueError:
        return jsonify({'erro': 'Valores inválidos fornecidos'}), 400
    
    # Encontra a tinta mais próxima
    tinta_selecionada = encontrar_tinta_desejada(lab_desejado)

    # Retorna a tinta encontrada ou mensagem de erro se nenhuma for encontrada
    if tinta_selecionada:
        resposta = {
            'SAP': tinta_selecionada['SAP'],
            'local': tinta_selecionada['local'],
            'verniz': tinta_selecionada['VERNIZ'],
            'L': tinta_selecionada['vL'],
            'a': tinta_selecionada['va'],
            'b': tinta_selecionada['vb'],
            'C': tinta_selecionada['vC'],
            'h': tinta_selecionada['vh']
        }
    else:
        resposta = {'erro': 'Nenhuma tinta encontrada'}

    return jsonify(resposta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
