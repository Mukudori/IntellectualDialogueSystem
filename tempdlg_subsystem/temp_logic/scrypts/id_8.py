# -*- coding: utf-8 -*-


def execute(args):
    tempLogic = args[0]
    client = tempLogic.client
    idGroup = client['idClientGroup']
    if idGroup==1:
        answer = 'Вы администратор.'
    elif idGroup ==2:
        answer = "Вы преподаватель РИИ. \n" \
                 "Ваше ФИО : %s \n" \
                 "Ваша кафедра : %s" % (client['shortfio'],
                                        client['nameCath'])
    elif idGroup ==  3:
        answer = "Вы студент. \n" \
                 "Ваша группа : %s \n" \
                 "Вы учитесь на %s курсе" % (client['name'],
                                             client['course'])
    else:
        answer = "Вы незарегистрированный клиент, который идентефицируется как \"гость\"."
    return answer