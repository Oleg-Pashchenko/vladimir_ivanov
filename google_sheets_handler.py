from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import date


def get_titles(sheet_titles):
    answer = []
    for title in sheet_titles:
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                     range=title).execute()
        data = result.get('values', [])[0]
        for element in data:
            answer.append(element.lower())
    return answer


def write_element(title, sum1):
    today = str(date.today().strftime("%d.%m.%Y"))
    for sheet_title in sheet_titles:
        titles = get_titles([sheet_title])
        if title.lower() in titles:
            print(sheet_title)
            result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                         range=sheet_title).execute()
            data = result.get('values', [])
            row_index = len(data) + 1
            col_index = 0
            for t in range(len(data[0])):
                if data[0][t].lower() == title.lower():
                    col_index = t
                    break
            col_index = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[col_index]
            cell_address = f'{sheet_title}!{col_index}{row_index}'
            body = {
                'values': [[int(sum1)]]
            }
            result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=cell_address,
                                                            valueInputOption='RAW', body=body).execute()
            body = {
                'values': [[str(today)]]
            }
            result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=f""
                                                                                                f"{sheet_title}!"
                                                                                                f"A{row_index}",
                                                            valueInputOption='RAW', body=body).execute()
            break


creds = Credentials.from_service_account_file('service_account.json',
                                              scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = '16GLnsRnQkvp0_-In7MGq__jKrqyKYAEXD55q1L7qOBQ'
sheet_titles = ['Личное', 'Бизнес']