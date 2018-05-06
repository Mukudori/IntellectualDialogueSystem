import os, sys, argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf

from ai_subsystem.lib.config import params_setup
from ai_subsystem.lib.train import train
from ai_subsystem.lib.predict import predict
from ai_subsystem.lib.chat import chat, ChatWithModel
# from ai_subsystem.lib.mert import mert

parent_form = 0


def main(argv=0, mform=0):
    #line = '--mode train --model_name name'
    '''sys.argv.append('--mode')
    sys.argv.append('train')
    sys.argv.append('--model_name')
    sys.argv.append('name')'''
    if argv:
        sys.argv=argv

    args = params_setup()
    print("[args]: ", args)

    if args.mode == 'train':
      train(args)
    elif args.mode == 'test':
      predict(args)
    elif args.mode == 'chat':
      #chat(args, parent_form=parent_form)
        ChatWithModel(args).StartTerminaleChat();

    # elif args.mode == 'mert':
    #   mert(args)


if __name__ == "__main__":
    main()
   # tf.app.run()