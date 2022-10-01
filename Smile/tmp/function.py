import os
import torch

## 네트워크 저장하기
def save(ckpt_dir, model, optim, epoch):
    if not os.path.exists(ckpt_dir):
        os.makedirs(ckpt_dir)
    
    
    torch.save({'model': model.state_dict(), 'optim': optim.state_dict()},
               "%s/model_epoch%d.pkl" % (ckpt_dir, epoch))

## 네트워크 불러오기
def load(ckpt_dir, model, optim):
    if not os.path.exists(ckpt_dir) or len(os.listdir(ckpt_dir)) == 0:
        epoch = 0
        return model, optim, epoch

    ckpt_lst = os.listdir(ckpt_dir)
    ckpt_lst.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    dict_model = torch.load('%s/%s' % (ckpt_dir, ckpt_lst[-1]))

    model.load_state_dict(dict_model['model'])
    optim.load_state_dict(dict_model['optim'])
    epoch = int(ckpt_lst[-1].split('epoch')[1].split('.pkl')[0])

    return model, optim, epoch