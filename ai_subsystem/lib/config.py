# -*- coding: utf-8 -*-
import argparse
import tensorflow as tf
#from ai_subsystem.aiMainFormModule import AiMainForm
from PyQt5.QtWidgets import QMainWindow
def params_setup(cmdline=None):
  parser = argparse.ArgumentParser()
  parser.add_argument('--mode', type=str, required=True, help='work mode: train/test/chat')
  
  # path ctrl
  parser.add_argument('--model_name', type=str, default='test_dialogs', help='Имя модели, affects data, модель, путь сохранения результата')
  parser.add_argument('--scope_name', type=str, help='Отдельное пространство имен для совместной работы нескольких моделей')
  parser.add_argument('--work_root', type=str, default='works', help='Корневой каталог тестовых данных, модели и сохранения результатов')

  # Параметры тренинга
  parser.add_argument('--learning_rate', type=float, default=0.5, help='Коэфициент обучения.')
  parser.add_argument('--learning_rate_decay_factor', type=float, default=0.99, help='Коэфициент обучения снижен значительно.')
  parser.add_argument('--max_gradient_norm', type=float, default=5.0, help='Clip gradients to this norm.')
  parser.add_argument('--batch_size', type=int, default=64, help='Размер пакета во время обучения.')

  parser.add_argument('--vocab_size', type=int, default=100000, help='Размер словаря диалогов.')
  parser.add_argument('--size', type=int, default=256, help='Размерность слоя каждой модели.')
  parser.add_argument('--num_layers', type=int, default=4, help='Количество слоев в модели.')

  parser.add_argument('--max_train_data_size', type=int, default=0, help='Лимит размера данных для обучения (0: нет лимита)')
  parser.add_argument('--steps_per_checkpoint', type=int, default=500, help='Количество шагов обучения до контрольной точки')

  # Параметры прогноза
  parser.add_argument('--beam_size', type=int, default=1, help='Размер луча поиска')
  parser.add_argument('--antilm', type=float, default=0, help='Вес анти-язычной модели')
  parser.add_argument('--n_bonus', type=int, default=0, help='Бонус с длиной предложения')

  # Параметры окружения
  parser.add_argument('--gpu_usage', type=float, default=1.0, help='tensorflow gpu для использованой памяти')
  parser.add_argument('--rev_model', type=int, default=0, help='перевернутая пара вопрос-ответ для двунаправленной модели')
  parser.add_argument('--reinforce_learn', type=int, default=0, help='1 для включения усиленного обучения')
  parser.add_argument('--en_tfboard', type=int, default=0, help='Включить запись мета данных tensorboard')

  # Дополнительные параметры
 # parser.add_argument('--parent_form', type=QMainWindow, default=0, help='Ссылка на родительскую форму')
  parser.add_argument('--device', type=str, default='GPU', help='Вычислительное устройство CPU/GPU')

  if cmdline:
    args = parser.parse_args(cmdline)
  else:
    args = parser.parse_args()
  
  if not args.scope_name: args.scope_name = args.model_name
  if args.rev_model: args.model_name += '_bidi' # двунаправленная модель
  
  # Используется несколько партий(buckets) и выравниваний(pad) для повышения эффективности.
  # Смотреть seq2seq_model.Seq2SeqModel для получения дополнительной информации.
  args.buckets = [(5, 10), (10, 15), (20, 25), (40, 50)]

  # Пост-процесс
  args.workspace = '%s/%s' % (('ai_subsystem/'+args.work_root), args.model_name)
  args.test_dataset_path = '%s/data/test/test_set.txt' % (args.workspace)
  args.mert_dataset_path = '%s/data/test/mert_set.txt' % (args.workspace)
  args.data_dir = '%s/data' % args.workspace
  args.model_dir = '%s/nn_models' % args.workspace
  args.results_dir = '%s/results' % args.workspace
  args.tf_board_dir = '%s/tf_board' % args.workspace
  return args

def configDevice(args,CPU = False):
    """Принудительное переключение вычислительного устройства"""
    if not CPU:
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=args.gpu_usage)
        return tf.ConfigProto(gpu_options=gpu_options)
    else:
        num_cores = 4
        config = tf.ConfigProto(intra_op_parallelism_threads=num_cores, \
                                inter_op_parallelism_threads=num_cores, allow_soft_placement=True, \
                                device_count={'CPU': 1, 'GPU': 0})
        return config

