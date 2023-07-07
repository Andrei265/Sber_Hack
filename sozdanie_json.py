import json
rassulka = {}
ra = []
spisok = ['daniligorevic@gmail.com', 'Kirill.vip23@gmail.com']
for i in spisok:
    rassulka = ({   
        "email": i,
        "subject": "Очень важное сообщение",
        "text": "Поздравляем вы приглашены на тестирование: https://t.me/resume_selection_bot",
        "attachment": [],
        "html": ""
   })
    ra.append(rassulka)
with open('data_1.json', 'w', encoding='utf-8') as outfile:
                json.dump(ra, outfile, ensure_ascii=False)
print(ra)