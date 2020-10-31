import os
import datetime
import numpy as np
import torch
import torchvision

import models.models

def training_loop(n_epochs,
                  model,
                  optimizer,
                  loss_function,
                  train_loader,
                  val_loader):
    print('Training:')
    best_val_loss = 0
    running_loss = []

    for epoch in range(1, n_epochs+1):

        training_loss = 0.0

        # iterate over training batch
        for imgs, _ in train_loader:
            # move tensors to device
            imgs = imgs.to(model.device)

            imgs_out = model(imgs)

            loss = loss_function(imgs_out, imgs)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            training_loss += loss.item()

        running_loss.append(training_loss)
        # print training and validation losses. save if model achieve better accuracy rate.
        if epoch % 10 == 0 or epoch == 1 or epoch == n_epochs:
            # loss = training_loss / len(train_loader)

            validation_loss = 0.0

            for imgs, _ in train_loader:
                # move tensors to device
                imgs = imgs.to(model.device)

                imgs_out = model(imgs)

                loss = loss_function(imgs_out, imgs)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                validation_loss += loss.item()

            print(f'{datetime.datetime.now()} Epoch: {epoch}, Training loss: {training_loss:.3f}')
            # validation_loss /= len(val_loader)
            print(f'{datetime.datetime.now()} Epoch: {epoch}, Validation loss: {validation_loss:.3f}')

            # if validation_loss > best_val_loss:
            #     # save model
            #     print('Saving model!')
            #     model.save_checkpoint()
            #     best_val_loss = validation_loss

    return running_loss


if __name__ == '__main__':

    # Get CIFAR10 dataset.
    data_path = 'C:\\Users\\Kyle\\Documents\\GitHub\\data\\'
    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])

    trainset_cifar = torchvision.datasets.CIFAR10(data_path, transform=transform, train=True, download=True)
    validset_cifar = torchvision.datasets.CIFAR10(data_path, transform=transform, train=False, download=True)
    training_loader = torch.utils.data.DataLoader(trainset_cifar, batch_size=32, shuffle=True)
    validation_loader = torch.utils.data.DataLoader(validset_cifar, batch_size=32, shuffle=False)

    # Create model
    model = models.models.LittmanNet()
    model.cuda()

    # Create optimizer, loss function.
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_function = torch.nn.L1Loss()
    n_epochs = 50

    running_loss = training_loop(n_epochs=n_epochs,
                                model=model,
                                optimizer=optimizer,
                                loss_function=loss_function,
                                train_loader=training_loader,
                                val_loader=validation_loader)


