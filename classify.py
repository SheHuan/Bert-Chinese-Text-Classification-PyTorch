import torch
from importlib import import_module

key = {
    0: 'finance',
    1: 'realty',
    2: 'stocks',
    3: 'education',
    4: 'science',
    5: 'society',
    6: 'politics',
    7: 'sports',
    8: 'game',
    9: 'entertainment'
}

x = import_module('models.' + 'Bert')
config = x.Config('THUCNews')
model = x.Model(config).to(config.device)
model.load_state_dict(torch.load(config.save_path, map_location='cpu'))


def build_predict_text(text):
    token = config.tokenizer.tokenize(text)
    token = ['[CLS]'] + token
    seq_len = len(token)
    mask = []
    token_ids = config.tokenizer.convert_tokens_to_ids(token)
    pad_size = config.pad_size
    if pad_size:
        if len(token) < pad_size:
            mask = [1] * len(token_ids) + ([0] * (pad_size - len(token)))
            token_ids += ([0] * (pad_size - len(token)))
        else:
            mask = [1] * pad_size
            token_ids = token_ids[:pad_size]
            seq_len = pad_size
    ids = torch.LongTensor([token_ids])
    seq_len = torch.LongTensor([seq_len])
    mask = torch.LongTensor([mask])
    return ids, seq_len, mask


def do_predict(text):
    """
    单个文本预测
    :param text:
    :return:
    """
    data = build_predict_text(text)
    with torch.no_grad():
        outputs = model(data)
        num = torch.argmax(outputs)
    return key[int(num)]


if __name__ == '__main__':
    print(do_predict("备考2012高考作文必读美文50篇(一)"))
