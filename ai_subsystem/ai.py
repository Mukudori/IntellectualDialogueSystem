import os, sys, argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf

from ai_subsystem.lib.config import params_setup
from ai_subsystem.lib.train import train
from ai_subsystem.lib.predict import predict
from ai_subsystem.lib.chat import chat
# from ai_subsystem.lib.mert import mert



def main():
    #line = '--mode train --model_name name'
    '''sys.argv.append('--mode')
    sys.argv.append('train')
    sys.argv.append('--model_name')
    sys.argv.append('name')'''

    args = params_setup()
    print("[args]: ", args)

    '''if args.mode == 'train':
      train(args)
    elif args.mode == 'test':
      predict(args)
    elif args.mode == 'chat':
      chat(args)
    '''
    # elif args.mode == 'mert':
    #   mert(args)


if __name__ == "__main__":
    main()
   # tf.app.run()