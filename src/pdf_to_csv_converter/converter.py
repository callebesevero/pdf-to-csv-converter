import pdfplumber
import pandas as pd
import io


def extract_statements(text):
    get_all = False
    statements = []
    for line in text:
        if 'SALDO ANTERIOR' in line:
            get_all = True
        elif get_all == True and 'SAC CAIXA' not in line:
            statements.append(line)
        elif 'SAC CAIXA' in line:
            break
    return statements


def convert_to_csv(statements):
    for i, st in enumerate(statements):
        st = st.split(' ')
        date = st[0]
        number = st[1]
        value = ' '.join(st[-4:-2]).replace(',', '.')
        sold = ' '.join(st[-2:]).replace(',', '.')
        # delete from the list to know history
        del st[0]
        del st[0]
        del st[-4:-2]
        del st[-2:]
        history = ' '.join(st)
        # Creating a 'csv string'
        statements[i] = f'{date},{number},{history},{value},{sold}'

    csv_file = ['Data Mov.,Nr. Doc.,Histórico,Valor,Saldo'] + statements
    csv_file = [line.split(',') for line in csv_file]

    df = pd.DataFrame(csv_file[1:], columns=csv_file[0])

    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8')
    return output.getvalue()


def main(archive):
    with pdfplumber.open(archive) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

    # Conveting to list
    text = text.split('\n')

    archive = extract_statements(text)
    archive = convert_to_csv(archive)
    return archive


if __name__=='__main__':
    main('/home/leanl/Documents/Code/pdf-to-csv-converter/database/extrato_caixa.pdf')