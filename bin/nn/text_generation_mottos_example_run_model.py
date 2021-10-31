from bin.nn.textgenrnn.textgenrnn import textgenrnn
from datetime import datetime

base_path = 'bin/nn/textgenrnn/'
base_model_path = f'{base_path}models/'

temperature = [1.0, 0.5, 0.2, 0.2]
prefix = None  # if you want each generated text to start with a given seed text

n = 1000
max_gen_length = 60

textgen = textgenrnn(weights_path=f'{base_model_path}colaboratory_weights.hdf5',
                     vocab_path=f'{base_model_path}colaboratory_vocab.json',
                     config_path=f'{base_model_path}colaboratory_config.json')

time_name = datetime.now().strftime('%Y%m%d_%H%M%S')
file_name = f'bin/nn/textgenrnn/output/textgenrnn_texts_{time_name}.txt'

textgen.generate_samples(max_gen_length=1000)
textgen.generate_to_file(file_name,
                         prefix=prefix,
                         temperature=temperature,
                         n=n,
                         max_gen_length=max_gen_length)
