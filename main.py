from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Hardcoded data as an example
data = [
    {'SAP': '100001', 'vL': 50.1, 'va': -2.3, 'vb': 1.5, 'vC': 48.2, 'vh': 230, 'local': '6*5*2'},
    {'SAP': '100002', 'vL': 60.2, 'va': 1.0, 'vb': -0.5, 'vC': 60.0, 'vh': 200, 'local': '6*5*3'},
    # Add all other rows here similarly
]

# Function to calculate Delta E
def calculate_delta_e(inputL, inputA, inputB, inputC, inputH, row):
    deltaL = inputL - row['vL']
    deltaA = inputA - row['va']
    deltaB = inputB - row['vb']
    deltaC = math.sqrt(inputC**2 + inputH**2) - math.sqrt(row['vC']**2 + row['vh']**2)
    deltaH = math.sqrt(abs(deltaA**2 + deltaB**2 - deltaC**2))
    return math.sqrt(deltaL**2 + deltaC**2 + deltaH**2)

@app.route('/calculate', methods=['POST'])
def calculate():
    data_input = request.json
    inputL = data_input.get('inputL')
    inputA = data_input.get('inputA')
    inputB = data_input.get('inputB')
    inputC = data_input.get('inputC')
    inputH = data_input.get('inputH')

    best_delta_e = float('inf')
    best_sap = None
    best_local = None

    for row in data:
        delta_e = calculate_delta_e(inputL, inputA, inputB, inputC, inputH, row)
        if delta_e < best_delta_e:
            best_delta_e = delta_e
            best_sap = row['SAP']
            best_local = row['local']
    
    return jsonify({
        'best_sap': best_sap,
        'best_local': best_local,
        'best_delta_e': best_delta_e
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
