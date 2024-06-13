from argparse import ArgumentParser

def main():

  parser = ArgumentParser()
  parser.add_argument('-i', '--input', required=True, help='Path to input QueueKV.at')
  parser.add_argument('-o', '--output', required=True, help='Path to output AppendQueueKV.fs')
  parser.add_argument('--images', required=True, help='Path to images FilelystemKV')
  parser.add_argument('--protocol', default='sqlite', required=False, choices=['sqlite', 'fs'], help='Protocol used in input queue')

  parser.add_argument('-p', '--port', type=int, help='TensorFlow Serving port')
  parser.add_argument('--host', type=str, help='TensorFlow Serving host')
  parser.add_argument('-e', '--endpoint', type=str, help='TensorFlow Serving model endpoint')

  args = parser.parse_args()

  import os
  input_path = os.path.join(os.getcwd(), args.input)
  output_path = os.path.join(os.getcwd(), args.output)
  images_path = os.path.join(os.getcwd(), args.images)
  proto = args.protocol

  from dslog import Logger
  logger = Logger.of(print).prefix('[OCR PREDICT]')
  cli_logger = logger.prefix('[CLI]')
  cli_logger(f'Running extraction...')
  cli_logger(f'Images path: "{images_path}"')
  cli_logger(f'Input path: "{input_path}"')
  cli_logger(f'Output path: "{output_path}"')
  cli_logger(f'Queues protocol: "{proto}"')

  from .predict import run_predict
  import ramda as R
  params = {
    k: v for k, v in R.pick(['port', 'host', 'endpoint'], args.__dict__).items() # type: ignore
    if v is not None
  } 
  run_predict(input_path, output_path, images_path, protocol=proto, logger=logger, **params)

if __name__ == '__main__':
  main()