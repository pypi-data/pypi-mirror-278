from main import YakutMorph
from mappers import CoNLLU
import json


path = '/Users/nicolascortegosovissio/PycharmProjects/yakut/annotate/littleprince/little_prince_dataset.json'
with open(path, 'r') as f:
    sentences = [(sentence['sah'], sentence['ru']) for sentence in json.load(f)]

morphology = YakutMorph()

with open('little_prince.conllu', 'w') as f:
    for i, sentence in enumerate(sentences, start=1):
        sah = sentence[0]
        ru = sentence[1]
        # We provide a header for the treebanks
        print(sah)
        header = [
            f'# sent_id = {i}',
            f'# text_sah = {sah}',
            f'# text_rus = {ru}'
        ]
        parse = CoNLLU(morphology.parse(sah), header)
        f.write(f'{parse}\n\n')
