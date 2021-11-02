"""
Run the already created model
"""

from bin.nn.textgenrnn.textgenrnn import textgenrnn
from datetime import datetime

base_path = 'bin/nn/textgenrnn/'
base_model_path = f'{base_path}models/'

model_name = 'model_2_11_2021_a'

# temperature = [1.0, 0.5, 0.2, 0.2]
temperature = [0.5]
prefix = None  # if you want each generated text to start with a given seed text

n = 40
max_gen_length = 40

textgen = textgenrnn(weights_path=f'{base_model_path}{model_name}_weights.hdf5',
                     vocab_path=f'{base_model_path}{model_name}_vocab.json',
                     config_path=f'{base_model_path}{model_name}_config.json')

time_name = datetime.now().strftime('%Y%m%d_%H%M%S')
file_name = f'bin/nn/textgenrnn/output/textgenrnn_texts_{time_name}.txt'

# textgen.generate_samples(max_gen_length=max_gen_length)
textgen.generate_to_file(file_name,
                         prefix=prefix,
                         temperature=temperature,
                         n=n,
                         max_gen_length=max_gen_length)