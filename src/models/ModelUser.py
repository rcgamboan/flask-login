from .entities.User import User

class ModelUser():

    @classmethod
    def login(self,db,user):
        try:
            cursor = db.cursor()
            query = """SELECT * 
                    FROM usuarios 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(query)
            row = cursor.fetchone()
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.password))
                return user , row[3]
            else:
                return None
        except Exception as ex:
            raise Exception(ex)