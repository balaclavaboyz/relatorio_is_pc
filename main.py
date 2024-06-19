from pprint import pp
from bs4 import BeautifulSoup
import re
import requests
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    url_post_login = 'https://intranet.ib.unicamp.br/intranet/index.php'
    load_dotenv()

    with requests.Session() as s:
        payload = {
            'login_tipo': 'IB',
            'usuario': os.getenv('user'),
            'senha': os.getenv('pass')
        }
        res = s.post(url_post_login, data=payload)

        if 'Busca de sistemas' in res.text:
            pp('login ok')
        else:
            exit('login fail')

        url_get_is = 'https://intranet.ib.unicamp.br/intranet/equipa_inform/cadastrar_micro.php?op=3&isnum='
        with open('is') as f:
            file = f.readlines()

        with open('res.txt', 'w', encoding='utf-8') as f:
            f.write('')

        for i in file:
            is_number = re.findall(r'\d+', i)[0]
            info_pc = s.get(f'{url_get_is}{is_number}')

            soup = BeautifulSoup(info_pc.content, features='lxml')
            res = soup.findAll('option', {'selected': True})
            sala = soup.findAll('input', {'name': 'sala'})

            new_info = []
            new_info.append(f'{is_number}\n')
            for i, v in enumerate(res):
                new_info.append(f'{v.text.strip()}\n')
            new_info.append(f'sala: {sala[0]['value']}\n')
            new_info.append('===\n\n')

            with open('res.txt', 'a', encoding='utf-8') as f:
                f.writelines(new_info)
