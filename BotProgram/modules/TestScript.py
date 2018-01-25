from database import DataBaseModule

if __name__ == '__main__':
    print(DataBaseModule.ExecuteSQL('''
            INSERT INTO questiontab (question)
             VALUES("Тестовый вопрос");'''))

