import re
import spacy
import multiprocessing
import argparse

"""
A spacy tokeninzer wrapper.
by: xiaodl
"""
def space_extend(matchobj):
    return ' ' + matchobj.group(0) + ' '

def reform_text(text):
    text = re.sub(u'-|¢|¥|€|£|\u2010|\u2011|\u2012|\u2013|\u2014|\u2015|%|\[|\]|:|\(|\)|/', space_extend, text)
    text = text.strip(' \n')
    text = re.sub('\s+', ' ', text)
    return text

class SpacyWrapper(object):
    def __init__(self, lang, batch_size, thread):
        self.lang = lang
        self.batch_size = batch_size
        self.thread = thread
        self.nlp = spacy.load(lang)

    def tokenize(self, docs):
        """
        Args:
            :param docs: an iter object of text
        """
        tokened_docs = self.nlp.pipe(docs, batch_size=self.batch_size, n_threads=self.thread)
        data = []
        for doc in tokened_docs:
            tokens = [w.text for w in doc if len(w.text) > 0]
            data.append(tokens)
        return data

def main(args):
    fin = args.fin
    fout = args.fout
    tokenizer = SpacyWrapper(args.lang, batch_size=args.bs, thread=args.thread)
    with open(fin, 'r', encoding=args.in_encode) as reader:
        data = [reform_text(line.strip()) for line in reader]
        tokened = tokenizer.tokenize(data)
        assert tokened is not None and len(tokened) > 0
        with open(fout, 'w', encoding=args.out_encode) as writer:
            for line in tokened:
                writer.write('{}\n'.format(' '.join(line)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spacy tokenize wrapper')
    parser.add_argument('--lang', type=str, default='en', help='langauge marker:en/de/fr')
    parser.add_argument('--thread', type=int, default=64)
    parser.add_argument('--bs', type=int, default=1024)
    parser.add_argument('--fin', type=str, required=True, help='input file path')
    parser.add_argument('--fout', type=str, required=True, help='output file path')
    parser.add_argument('--in_encode', type=str, required=True, help='input file encoding')
    parser.add_argument('--out_encode', type=str, required=True, help='output file encoding')
    args = parser.parse_args()
    main(args)
