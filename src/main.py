import pdfplumber
import pandas


def extract_statements(text):
    get_all = False
    for line in text:
        if 'SALDO ANTERIOR' in line:
            get_all = True
        elif get_all == True and 'SAC CAIXA' not in line:
            statements.append(line)
        elif 'SAC CAIXA' in line:
            break


def convert_to_csv(statements):
    for i, st in enumerate(statements):
        st = st.split(' ')
        date = st[0]
        number = st[1]
        value = ' '.join(st[-4:-2]).replace('.', '').replace(',', '.')
        sold = ' '.join(st[-2:]).replace('.', '').replace(',', '.')
        # delete from the list
        del st[0]
        del st[0]
        del st[-4:-2]
        del st[-2:]
        history = ' '.join(st)
        # Creating a 'csv strings'
        statements[i] = f'{date},{number},{history},{value},{sold}'


with pdfplumber.open('./database/Extrato_Caixa.pdf') as pdf:
    page = pdf.pages[0]
    text = page.extract_text()

# Conveting to list
text = text.split('\n')
statements = []

extract_statements(text)
convert_to_csv(statements)

csv_file = ['Data Mov.,Nr. Doc.,Histórico,Valor,Saldo'] + statements
csv_file = [line.split(',') for line in csv_file]

df = pandas.DataFrame(csv_file[1:], columns=csv_file[0])
df.to_csv('./database/statements.csv', index=False, encoding='utf-8')