- 👋 Hi, I’m @AdrianoNill
- 👀 I’m interested in ...
- 🌱 I’m currently learning ...
- 💞️ I’m looking to collaborate on ...
- 📫 How to reach me ...

<!---
AdrianoNill/AdrianoNill is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

from iqoptionapi.stable_api import IQ_Option
import random
import math
import time
import numpy as np
from datetime import datetime
import pandas as pd

API = IQ_Option('login', 'senha')
API.connect()

API.change_balance('PRACTICE')  # PRACTICE / REAL

operacao = 1
valor_entrada = float(1.0)  # float(input(' Indique um valor para entrar: '))
valor_entrada_b = float(valor_entrada)
martingale = 12
par = 'EURUSD-OTC'


def Martingale(valor, payout):
    lucro_esperado = valor * payout
    perda = float(valor)

    while True:
        if round(valor * payout, 2) > round(abs(perda) + lucro_esperado, 2):
            return round(valor, 2)
            break
        valor += 0.01


def Payout(par):
    API.subscribe_strike_list(par, 1)
    while True:
        d = API.get_digital_current_profit(par, 1)
        if d != False:
            d = round(int(d) / 100, 2)
            break
        time.sleep(1)
    API.unsubscribe_strike_list(par, 1)

    return d


def VerificaVelas():
    API.start_candles_stream(par, 300, 10)

    """
    velas[0] = 'g' if velas[0]['open'] < velas[0]['close'] else 'r' if velas[0]['open'] > velas[0]['close'] else 'd'
    velas[1] = 'g' if velas[1]['open'] < velas[1]['close'] else 'r' if velas[1]['open'] > velas[1]['close'] else 'd'
    velas[2] = 'g' if velas[2]['open'] < velas[2]['close'] else 'r' if velas[2]['open'] > velas[2]['close'] else 'd'
    velas[3] = 'g' if velas[3]['open'] < velas[3]['close'] else 'r' if velas[3]['open'] > velas[3]['close'] else 'd'
    velas[4] = 'g' if velas[4]['open'] < velas[4]['close'] else 'r' if velas[4]['open'] > velas[4]['close'] else 'd'
    velas[5] = 'g' if velas[5]['open'] < velas[5]['close'] else 'r' if velas[5]['open'] > velas[5]['close'] else 'd'
    velas[6] = 'g' if velas[6]['open'] < velas[6]['close'] else 'r' if velas[6]['open'] > velas[6]['close'] else 'd'
    velas[7] = 'g' if velas[7]['open'] < velas[7]['close'] else 'r' if velas[7]['open'] > velas[7]['close'] else 'd'
    velas[8] = 'g' if velas[8]['open'] < velas[8]['close'] else 'r' if velas[8]['open'] > velas[8]['close'] else 'd'
    velas[9] = 'g' if velas[9]['open'] < velas[9]['close'] else 'r' if velas[9]['open'] > velas[9]['close'] else 'd'
    cores_martin = velas[0] + ' ' + velas[1] + ' ' + velas[2] + ' ' + velas[3] + ' ' + velas[4] + ' ' + velas[5] \
                   + ' ' + velas[6] + ' ' + velas[7] + ' ' + velas[8] + ' ' + velas[9]
    tamanho_vela_0 = velas[0]['close'] - velas[0]['open']
    print('Velas verdes ', cores_martin.count('g'))
    print('Velas vermelhas ', cores_martin.count('r'))
    tamanho_vela_0 = (velas[0]['open'] - velas[0]['close']) * 1000
    tamanho_vela_1 = (velas[1]['open'] - velas[1]['close']) * 1000
    tamanho_vela_2 = (velas[2]['open'] - velas[2]['close']) * 1000
    tamanho_vela_3 = (velas[3]['open'] - velas[3]['close']) * 1000
    tamanho_vela_4 = (velas[4]['open'] - velas[4]['close']) * 1000
    tamanho_vela_5 = (velas[5]['open'] - velas[5]['close']) * 1000
    tamanho_vela_6 = (velas[6]['open'] - velas[6]['close']) * 1000
    tamanho_vela_7 = (velas[7]['open'] - velas[7]['close']) * 1000
    tamanho_vela_8 = (velas[8]['open'] - velas[8]['close']) * 1000
    tamanho_vela_9 = (velas[9]['open'] - velas[9]['close']) * 1000
    print('Vela size primeira ', round(tamanho_vela_0, 7),
          ' 1 ', round(tamanho_vela_1, 7),
          ' 2 ', round(tamanho_vela_2, 7),
          ' 3 ', round(tamanho_vela_3, 7),
          ' 4 ', round(tamanho_vela_4, 7),
          ' 5 ', round(tamanho_vela_5, 7),
          ' 6 ', round(tamanho_vela_6, 7),
          ' 7 ', round(tamanho_vela_7, 7),
          ' 8 ', round(tamanho_vela_8, 7),
          ' 9 ', round(tamanho_vela_9, 7))
    """

    while True:
        candles = API.get_realtime_candles(par, 300)
        inputs = {
            'open': np.array([]),
            'high': np.array([]),
            'low': np.array([]),
            'close': np.array([]),
            'volume': np.array([]),
            'at': np.array([])
        }

        for timestamp in candles:
            inputs['open'] = np.append(inputs['open'], candles[timestamp]['open'])
            inputs['close'] = np.append(inputs['close'], candles[timestamp]['close'])
            inputs['volume'] = np.append(inputs['volume'], candles[timestamp]['volume'])

        """
        print('Open das velas ', round(inputs['open'][0], 5), 'Open da segunda ', round(inputs['open'][1], 5),
              round(inputs['open'][2], 5), 'Open da terceira ', round(inputs['open'][3], 5),
              round(inputs['open'][4], 5), 'Open da quarta ', round(inputs['open'][5], 5))
        """
        #       tempo_vela = int(inputs['at'][9])
        #       tempo_vela_str = str(tempo_vela)[:10]
        #       tempo_vela_int = int(tempo_vela_str)
        soma_verde = 0.0
        soma_vermelha = 0.0

        close_vela_9 = str(inputs['close'][9])[:7]
        open_vela_9 = str(inputs['open'][9])[:7]

        tamanho_vela_9 = float(close_vela_9) - float(open_vela_9)

        close_vela_8 = str(inputs['close'][8])[:7]
        open_vela_8 = str(inputs['open'][8])[:7]

        tamanho_vela_8 = float(close_vela_8) - float(open_vela_8)
        if tamanho_vela_8 > 0:
            soma_verde += tamanho_vela_8
        elif tamanho_vela_8 < 0:
            soma_vermelha += -tamanho_vela_8

        close_vela_7 = str(inputs['close'][7])[:7]
        open_vela_7 = str(inputs['open'][7])[:7]

        tamanho_vela_7 = float(close_vela_7) - float(open_vela_7)
        if tamanho_vela_7 > 0:
            soma_verde += tamanho_vela_7
        elif tamanho_vela_7 < 0:
            soma_vermelha += -tamanho_vela_7

        razao_verde_vermelha = 0
        if soma_vermelha > 0:
            razao_verde_vermelha = float(soma_verde / soma_vermelha)

        print("Tamanho da ultima vela 10 ", format(tamanho_vela_9, '.6f'),
              " tamanho vela 9 ", format(tamanho_vela_8, '.6f'),
              " tamanho vela 8 ", format(tamanho_vela_7, '.6f'),
              " Soma verdes ", format(soma_verde, '.6f'),
              " Soma vermelhas ", format(soma_vermelha, '.6f'),
              " Porcentagem verde/vermelha ", format(razao_verde_vermelha, '.6f'),
              )

        # print(" Tempo ", datetime.datetime.fromtimestamp(tempo_vela_int).strftime("%Y-%m-%d, %H:%M:%S"),
        #      " preco atual ", inputs['close'][19], " anterior ", close_vela_9)
        # print("O que temos nas velas ", datetime.datetime.fromtimestamp(tempo_vela) )
        #  datetime.datetime.fromtimestamp(int(round(float(tempo_vela)))
        # API.stop_candles_stream(par, 300)
        time.sleep(5)


# print('Close da vela 0 ', velas[0]['close'])
# print('O stream ', vela_stream[0]['close'])


payout = Payout(par)
print(payout)
VerificaVelas()
