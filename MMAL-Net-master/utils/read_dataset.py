import torch
import os
from datasets import dataset

def read_dataset(input_size, batch_size, root, set, status):
    if set == 'CUB':
        print('Loading CUB trainset')
        trainset = dataset.CUB(input_size=input_size, root=root, is_train=True)
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                                  shuffle=True, num_workers=8, drop_last=False)
        print('Loading CUB testset')
        testset = dataset.CUB(input_size=input_size, root=root, is_train=False)
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                                 shuffle=False, num_workers=8, drop_last=False)
    elif set == 'CAR':
        print('Loading car trainset')
        trainset = dataset.STANFORD_CAR(input_size=input_size, root=root, is_train=True)
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                                  shuffle=True, num_workers=8, drop_last=False)
        print('Loading car testset')
        testset = dataset.STANFORD_CAR(input_size=input_size, root=root, is_train=False)
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                                 shuffle=False, num_workers=8, drop_last=False)
    
    elif set == 'CompCars':
        print('Loading CompCars trainset')
        trainset = dataset.CompCars(input_size=input_size, root=root, is_train=True, is_val=False)
        print(f'Size of trainset: {len(trainset)}')
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                                  shuffle=True, num_workers=8, drop_last=False)
        if status == 'train':
            print('Loading CompCars valset') # NOTE: for train.py, this is the validation set, for consistency of code we leave the variable name as test
            testset = dataset.CompCars(input_size=input_size, root=root, is_train=False, is_val=True)
            print(f'Size of valset: {len(testset)}')
        elif status == 'test':
            print('Loading CompCars testset') # NOTE: now test.py is run, load the actual test set
            testset = dataset.CompCars(input_size=input_size, root=root, is_train=False, is_val=False)
            print(f'Size of testset: {len(testset)}')
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                                 shuffle=False, num_workers=8, drop_last=False)

    elif set == 'Aircraft':
        print('Loading Aircraft trainset')
        trainset = dataset.FGVC_aircraft(input_size=input_size, root=root, is_train=True)
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                                  shuffle=True, num_workers=8, drop_last=False)
        print('Loading Aircraft testset')
        testset = dataset.FGVC_aircraft(input_size=input_size, root=root, is_train=False)
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                                 shuffle=False, num_workers=8, drop_last=False)
    else:
        print('Please choose supported dataset')
        os._exit()

    return trainloader, testloader