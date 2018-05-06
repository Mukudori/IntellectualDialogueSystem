import os
import sys

import tensorflow as tf
from termcolor import colored

from ai_subsystem.lib import data_utils
from ai_subsystem.lib.seq2seq_model_utils import create_model, get_predicted_sentence
from ai_subsystem.lib.config import configDevice
from ai_subsystem.works import ModelGetter
import sys
from ai_subsystem.lib.config import params_setup

def refreshWidget(wid):
    wid.refreshListWidget()

def chat(args, parent_form=0):
  con = configDevice(args=args,CPU=True)
  with tf.Session(config=con) as sess:
    # Созддание модели и загрузка параметров.
    stop_word = 'ЗАКОНЧИТЬ_ТЕСТ'
    args.batch_size = 1  # Декодируется одно предложение за раз.
    model = create_model(sess, args)

    # Загрузка словарей.
    vocab_path = os.path.join(args.data_dir, "vocab%d.in" % args.vocab_size)
    vocab, rev_vocab = data_utils.initialize_vocabulary(vocab_path)

    # Декодировать из стандартного ввода.
    print(colored('Чат запущен.\nЧтобы завершить ручное тестирование введите %s.'%stop_word))
    sys.stdout.write(colored("Админ > ", 'green'))
    sys.stdout.flush()
    sentence = sys.stdin.readline()

    while True:

        sentence = sentence[:-1]
        if  sentence.upper() == stop_word:
            sys.stdout.write(colored("Завершение ручного теста ...", 'yellow'))
            sys.stdout.flush()
            if parent_form:
                parent_form.clearWidget()
            break
        else:
            predicted_sentence = get_predicted_sentence(args, sentence, vocab, rev_vocab, model, sess)
            # print(predicted_sentence)
            if isinstance(predicted_sentence, list):
                for sent in predicted_sentence:
                    print(colored("Система-> %s", 'blue') % sent['dec_inp'])
            else:
                print(sentence, ' -> ', predicted_sentence)

            sys.stdout.write(colored("Админ > ", 'green'))
            sys.stdout.flush()
            sentence = sys.stdin.readline()

class ChatWithModel(object):
    def __init__(self):
        super().__init__()
        self.initArgs()

        

    def StartTerminaleChat(self):
        stop_word = 'ЗАКОНЧИТЬ_ТЕСТ'
        # Декодировать из стандартного ввода.
        print(colored('Чат запущен.\nЧтобы завершить ручное тестирование\
         введите %s.' % stop_word))
        sys.stdout.write(colored("Админ > ", 'green'))
        sys.stdout.flush()
        sentence = sys.stdin.readline()

        while True:

            sentence = sentence[:-1]
            if sentence.upper() == stop_word:
                sys.stdout.write(colored("Завершение ручного теста ...", 'yellow'))
                sys.stdout.flush()
               # if parent_form:
               #     parent_form.clearWidget()
                break
            else:
                predicted_sentence = get_predicted_sentence(self.args,
                        sentence, self.vocab, self.rev_vocab, self.model,
                                                            self.sess)
                # print(predicted_sentence)
                if isinstance(predicted_sentence, list):
                    for sent in predicted_sentence:
                        print(colored("Система-> %s", 'blue') % sent['dec_inp'])
                else:
                    print(sentence, ' -> ', predicted_sentence)

                sys.stdout.write(colored("Админ > ", 'green'))
                sys.stdout.flush()
                sentence = sys.stdin.readline()

    def GetAnswer(self, text):
        predicted_sentence = get_predicted_sentence(self.args,
                                                    text, self.vocab, self.rev_vocab, self.model,
                                                    self.sess)
        # print(predicted_sentence)
        if isinstance(predicted_sentence, list):
            return [sent['dec_inp'] for sent in predicted_sentence ]
        else:
            return [predicted_sentence,]
    
    def startSession(self):
        con = configDevice(args=self.args, CPU=True)
        self.sess = tf.InteractiveSession(config=con)
        self.args.batch_size = 1  # Декодируется одно предложение за раз.
        self.model = create_model(self.sess, self.args)

        # Загрузка словарей.
        vocab_path = os.path.join(self.args.data_dir, "vocab%d.in" % self.args.vocab_size)
        self.vocab, self.rev_vocab = data_utils.initialize_vocabulary(vocab_path)
        print('Модель готова к работе')

    def initArgs(self):
        b = sys.argv[0]
        sys.argv.clear()
        sys.argv.append(b)
        sys.argv.append('--mode')
        sys.argv.append('chat')
        sys.argv.append('--model_name')
        #sys.argv.append('First_model')
        sys.argv.append(ModelGetter.getActiveModelName())
        self.args = params_setup()


