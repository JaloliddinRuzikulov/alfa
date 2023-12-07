import datetime
from modules import *
import fuzzywuzzy
from fuzzywuzzy import fuzz
import sys

current_time = datetime.datetime.now()

def sttoint(data):
    try:
        return f"ID{int(data)}"
    except Exception as err:
        print(err)
        

try:
    df = pd.read_excel(f"docs/{current_time.strftime('%b%d').lower()}bux.xlsx", sheet_name='2-kurs', skiprows=2)
except:
    df = pd.read_excel(f"docs/{current_time.strftime('%b%d').lower()}bux.xls", sheet_name='1-kurs', skiprows=2)
    
    
# df['ID'] = df['ID'].apply(sttoint)

try:
    setter = pd.read_excel(f"docs/{current_time.strftime('%b%d').lower()}.xlsx", sheet_name='umumiy', skiprows=2)
except:
    setter = pd.read_excel(f"docs/{current_time.strftime('%b%d').lower()}.xls", sheet_name='umumiy', skiprows=2)

counter_fish_set = 0
counter_id_set = 0

for index, row in df.iterrows():
    setter_row = setter[setter['ID'] == row['ID']]
    if setter_row.empty:
        print(row['ID'], row['F.I.Sh'], 'topilmadi')
        continue

    # Ensure that NaN values are replaced with 0
    try:
        converted_sum = setter_row["To'langan summa/grant"].fillna(0).astype(int)
        total_sum = converted_sum + int(row["to'langan summa"])
        setter.loc[setter_row.index, "To'langan summa/grant"] = total_sum
        counter_id_set += 1
    except Exception as err:
        print(f"Error processing row {index}: {err}")
    
print(counter_fish_set, counter_id_set)

df.to_excel(f'generates/oborotka_{current_time.strftime("%b%d_%H_%M")}.xlsx')
setter.to_excel(f'generates/student_{current_time.strftime("%b%d_%H_%M")}.xlsx')

# df['Student ID'] = df['Data'].apply(find_studentid)

# df.insert(3, 'FISH', '')

# for index, row in df.iterrows():
#     if row['Student ID'] == '':
#         df.iloc[index, 3] = fish_setter(row['Data'])

# df.to_excel('sad.xlsx')
# setter['FISH'] = setter['Familiyasi'] + ' ' + setter['Ismi'] + ' ' + setter['Otasining ismi']
# setter.insert(0, 'Student ID2', '')