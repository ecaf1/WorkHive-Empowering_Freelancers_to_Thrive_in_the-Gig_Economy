from database import create_table, add_user, confirm_user

create_table()
if add_user("joeão", "1234"):
    print("user adicionado com sucesso !")
else:
    print("Nome de usuario já existente  !")