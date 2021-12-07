import pandas as pd, requests as req, os, json, time
from selenium import webdriver

CSV_NAME = input('What is the name of the .CSV file to be imported (only the name, without the .csv extension)? ')

CSV_DF = pd.read_csv(CSV_NAME + '.csv')

FILE = 'last_UG_data.txt'

#DRIVER = webdriver.Firefox()

def program_end():
    print('\nEnd of the program.')
    time.sleep(5)

def confirm(text):
    confirm = input(text)
    print()
    
    if confirm not in ('n', 'N', 'no', 'No', 'NO', 'Não', 'NÃO', 'não'):
        return True
    else:
        return False

def check_csv():
    if CSV_DF.isnull() is not True:
        return True

def check_file(file = FILE):
    if os.path.isfile('./' + FILE):
        return True

def ask_for_data():
    data = {
        'ug' : input('Enter the UG code: '),
        'token' : input('Enter the PagTesouro token to the previous UG code: '),
        's_code' : input('Enter the service code: ')
        }

    open(FILE, 'w').write(json.dumps(data))

    return data

def ask_for_prices():
    prices = {
        1 : round(float(input('Enter the price to be charged to the residents of the first village: ')), 2),
        2 : round(float(input('Enter the price to be charged to the residents of the second village: ')), 2),
        3 : round(float(input('Enter the price to be charged to the residents of the third village: ')), 2),
        'm_date' : input('Enter the the maturity date for all the invoices (DDMMAAA): ')
        }

    return prices

def send_request(i, mil_data, prices, ug_data, log_name):
    url = 'https://valpagtesouro.tesouro.gov.br/api/gru/solicitacao-pagamento'
    headers = {
        'Authorization' : 'Bearer + ' ' + ug_data['token'],
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept' : 'application/json, text/plain, */*',
        'Accept-Language' : 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding' : 'gzip, deflate, br',
        'X-Requested-With' : 'XMLHttpRequest',
        'Content-Type' : 'application/json;charset=utf-8',
        'Connection' : 'keep-alive'
        }

    cpf, name = str(mil_data['CPF']), mil_data['Name']
    price = str(prices[mil_data['Village']])
    data = {
        'codigoServico' : ug_data['s_code'],
        'vencimento' : prices['m_date'],
        'cnpjCpf' : cpf,
        'nomeContribuinte' : name,
        'valorPrincipal' : price,
        }

    request = req.post(url, data = json.dumps(data), headers = headers)

    ok_msg = 'Request ' + str(i) + ' was successfully sent!'
    error_msg = 'Request ' + str(i) + ' has returned this status: ' + str(request.status_code)

    if request.ok:
        print(ok_msg)
        log_name.write(ok_msg)
        log_name.write('\n')
        time.sleep(0.2)
    else:
        print(error_msg)
        log_name.write(error_msg + ' ')
        for i in json.loads(request.text):
            for item in i.items():
                log_name.write(item[0] + ': ' + item[1] + ' ')
        log_name.write('\n')
                
        time.sleep(1)

    return request

def work_response(response):
    #DRIVER.get(response['proximaUrl'])
    print(response['proximaUrl'])
    time.sleep(5)
            
def start():
    if check_csv():
        if check_file() and confirm('Do you want to use the last used UG data? '):
            ug_data = json.loads(open(FILE, 'r').read())
        else:
            ug_data = ask_for_data()

        prices = ask_for_prices()

        log_time = str(int(time.time()))
        log_name = log_time + '_log.txt'

        for i in CSV_DF.index:
            write_file = open(log_name, 'a')
            request = send_request(i, CSV_DF.loc[i], prices, ug_data, write_file)
            response = json.loads(request.text)

            if request.ok:
                work_response(response)

            else:
                for i in response:
                    for item in i.items():
                        print(item[0], ': ', item[1], sep='')
            
            write_file.close()
        
if __name__ == '__main__':
    start()          
