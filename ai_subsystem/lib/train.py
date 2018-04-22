# -*- coding: utf-8 -*-
import sys, os, math, time, argparse, shutil, gzip
import numpy as np
import tensorflow as tf
from ai_subsystem.lib.config import configDevice

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from six.moves import xrange  # pylint: disable=redefined-builtin
from datetime import datetime
from ai_subsystem.lib import seq2seq_model_utils, data_utils


def setup_workpath(workspace):
  for p in ['data', 'nn_models', 'results']:
    wp = "%s/%s" % (workspace, p)
    if not os.path.exists(wp): os.mkdir(wp)

  data_dir = "%s/data" % (workspace)
  # Данные тренинга
  if not os.path.exists("%s/chat.in" % data_dir):
    n = 0
    f_zip   = gzip.open("%s/train/chat.txt.gz" % data_dir, 'rt')
    f_train = open("%s/chat.in" % data_dir, 'w')
    f_dev   = open("%s/chat_test.in" % data_dir, 'w')
    for line in f_zip:
      f_train.write(line)
      if n < 10000: 
        f_dev.write(line)
        n += 1

def CreateInfoFile(args):
    f = open(args.workspace+'/modelinfo.ini', 'w')

    f.write('[modelinfo]\n')
    f.write('model_name = %s\n' % args.model_name)
    f.write("date_time = %s\n" % datetime.now())
    f.write('num_layers = %s\n' % args.num_layers)
    f.write('size = %s\n' % args.size)


    f.close()




def train(args, parent=0):
    print("[%s] Подготовка диалогов в %s" % (args.model_name, args.data_dir))
    setup_workpath(workspace=args.workspace)
    train_data, dev_data, _ = data_utils.prepare_dialog_data(args.data_dir, args.vocab_size)

    if args.reinforce_learn:
      args.batch_size = 1  # Декодируется одно предложение одновременно.


    with tf.Session(config=configDevice(args=args, CPU=False)) as sess:

        CreateInfoFile(args)
        # Создается модель.
        print("Создание %d слоев на %d нейронов." % (args.num_layers, args.size))
        model = seq2seq_model_utils.create_model(sess, args, forward_only=False)

        # Читаются данные в партиях(buckets) и вычисляются их размеры.
        print("Чтение данных и обучение (limit: %d)." % args.max_train_data_size)
        dev_set = data_utils.read_data(dev_data, args.buckets, reversed=args.rev_model)
        train_set = data_utils.read_data(train_data, args.buckets, args.max_train_data_size, reversed=args.rev_model)
        train_bucket_sizes = [len(train_set[b]) for b in xrange(len(args.buckets))]
        train_total_size = float(sum(train_bucket_sizes))

        # Шкала партии представляет собой список увеличивающихся чисел от 0 до 1, которые будут использоваться
        # для выбора партии. Длина [scale[i], scale[i+1]]  пропорциональна
        # размеру если i-я тренировочная партия использована позднее.
        train_buckets_scale = [sum(train_bucket_sizes[:i + 1]) / train_total_size
                               for i in xrange(len(train_bucket_sizes))]

        # Тренировочный цикл.
        step_time, loss = 0.0, 0.0
        current_step = 0
        previous_losses = []

        # загрузка словарей.
        vocab_path = os.path.join(args.data_dir, "vocab%d.in" % args.vocab_size)
        vocab, rev_vocab = data_utils.initialize_vocabulary(vocab_path)

        while True:
          if parent:
              if not parent.TrainingInProcess:
                  print('Принята команда завершить обучение.')
                  break
          # Выберите партию в соответствии с распределением данных. Здесь выбирается случайное число
          # в[0, 1] и используется соответствующий интервал в train_buckets_scale.
          random_number_01 = np.random.random_sample()
          bucket_id = min([i for i in xrange(len(train_buckets_scale))
                           if train_buckets_scale[i] > random_number_01])

          # Получить партию и сделать шаг
          start_time = time.time()
          encoder_inputs, decoder_inputs, target_weights = model.get_batch(
              train_set, bucket_id)

          # print("[shape]", np.shape(encoder_inputs), np.shape(decoder_inputs), np.shape(target_weights))
          if args.reinforce_learn:
            _, step_loss, _ = model.step_rf(args, sess, encoder_inputs, decoder_inputs,
                                         target_weights, bucket_id, rev_vocab=rev_vocab)
          else:
            _, step_loss, _ = model.step(sess, encoder_inputs, decoder_inputs,
                                         target_weights, bucket_id, forward_only=False, force_dec_input=True)

          step_time += (time.time() - start_time) / args.steps_per_checkpoint
          loss += step_loss / args.steps_per_checkpoint
          current_step += 1

          # Время от времени мы сохраняем контрольную точку, печатаем статистику и запускаем оценки.
          if (current_step % args.steps_per_checkpoint == 0) and (not args.reinforce_learn):
            # Печатается статистика за предыдущую эпоху
            perplexity = math.exp(loss) if loss < 300 else float('inf')
            print ("Пройдено итераций %d, значение допустимой ошибки %.4f, шаг времени %.2f perplexity %.2f @ %s" %
                   (model.global_step.eval(), model.learning_rate.eval(), step_time, perplexity, datetime.now()))

            # Уменьшается скорость обучения, если за последние 3 раза не было улучшено.
            if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                sess.run(model.learning_rate_decay_op)
                print('Уменьшается скорость обучения..')

            previous_losses.append(loss)

            # # Сохранение контрольной точки, обнуление таймера и потерь
            checkpoint_path = os.path.join(args.model_dir, "model.ckpt")
            print('Сохранение контрольной точки ...')
            model.saver.save(sess, checkpoint_path, global_step=model.global_step)
            step_time, loss = 0.0, 0.0

            # запуск оценки на наборе и вывод perplexity.
            for bucket_id in xrange(len(args.buckets)):
              encoder_inputs, decoder_inputs, target_weights = model.get_batch(dev_set, bucket_id)
              _, eval_loss, _ = model.step(sess, encoder_inputs, decoder_inputs, 
                                          target_weights, bucket_id, forward_only=True, force_dec_input=False)

              eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
              print("  Оценка : bucket %d perplexity %.2f" % (bucket_id, eval_ppx))



            sys.stdout.flush()
