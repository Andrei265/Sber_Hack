import smtplib
from email.message import EmailMessage
import json_handler

class postman():
    post_service : smtplib.SMTP
    email : str


    def __init__(self, email : str, password : str ) -> None: 
        try:
            self.email = email
            
            if email.find('yandex') != -1:
                print(f"--- Connected from Yandex")
                self.post_service = smtplib.SMTP_SSL('smtp.yandex.ru', 465) # , 465  , 587
                # self.post_service.login(email , password)
                # self.post_service.ehlo()
                # self.post_service.starttls()
            else:
                print(f"--- Connected from Gmail")
                self.post_service = smtplib.SMTP('smtp.gmail.com', 587)
                self.post_service.starttls()
                # self.post_service.login(email , password)
            
            self.post_service.login(email , password)
            
        except Exception as e:
            
            print(f"--- Can`t connect {email} with password {password} and error {e}")
        else:
            print(f'--- Connected to {email} with password {password}')
        


    def drop_service(self) -> None: # Завершение сеанса рассылки
        self.post_service.quit()
        print(f'--- Session closed')

    def broadcast(self, content) -> None :  # Рассылка множество писем по данным из словаря
        if type(content) == str:
            data = json_handler.read_json(content)
        elif  type(content) == list:
            data = content
        else:
            raise(TypeError)
            
        for dicts in data:
            m = massage(self)
            m.set_content(dicts["email"], dicts["subject"], dicts["text"])
            m.set_attachment(dicts["attachment"])
            m.send_mail()
    
    
class massage(postman):
    msg : EmailMessage
    man : postman

    def __init__(self, man : postman) -> None:
        self.msg = EmailMessage()
        self.man = man
        self.msg['From'] = self.man.email

    def set_text(self, text : str) -> None:
        self.msg.set_content(text)
    
    def set_subject(self, subject : str) -> None:
        self.msg['Subject'] = subject

    def set_receiver_email(self, receiver_email : str) -> None:
        self.msg['To'] = receiver_email

    def set_attachment(self, list_files) -> None:
        if len(list_files) != 0:
            for file_path in list_files:
                with open(file_path, 'rb') as attachment:
                    file_data = attachment.read()
                    file_type =  self.get_maintype(file_path)
                    file_name = attachment.name
                    self.msg.add_attachment(file_data, maintype=file_type[0], subtype=file_type[1], filename=file_name.split('.')[0])
            
    def set_content(self, receiver_email : str, subject : str, text : str) -> None:
        self.set_receiver_email(receiver_email)
        self.set_subject(subject)
        self.set_text(text)
    

    def send_mail(self) -> None:
        try :
            self.man.post_service.send_message(self.msg)
        except Exception:
            print(f'--- Can`t delevery message to {self.msg["To"]}')
        else:
            print(f'--- Message delivered message to {self.msg["To"]}')

def main():
    man = postman('volini.ru@gmail.com', 'abivrdtawkabqugg') # Создаём сессию "EP"
    



    man.broadcast('data_1.json')

    man.drop_service()

if __name__ == '__main__': 
    main()

print(f'{__name__} is here !')