import os
import sys

import tensorflow as tf
from termcolor import colored

from lib import data_utils
from lib.seq2seq_model_utils import create_model, get_predicted_sentence


def chat(args):
  with tf.Session() as sess:
    # Созддание модели и загрузка параметров.
    args.batch_size = 1  # Декодируется одно предложение за раз.
    model = create_model(sess, args)

    # Загрузка словарей.
    vocab_path = os.path.join(args.data_dir, "vocab%d.in" % args.vocab_size)
    vocab, rev_vocab = data_utils.initialize_vocabulary(vocab_path)

    # Декодировать из стандартного ввода.
    print(colored('Чат запущен.\nЧтобы завершить ручное тестирование ввежите "ЗАКОНЧИТЬ ТЕСТ".'))
    sys.stdout.write(colored("Админ > ", 'green'))
    sys.stdout.flush()
    sentence = sys.stdin.readline()

    while True:
        if sentence.upper() == 'ЗАКОНЧИТЬ ТЕСТ':
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

