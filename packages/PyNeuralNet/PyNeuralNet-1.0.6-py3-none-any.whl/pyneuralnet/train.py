from .models.test import test
from .models.SRCNN import SRCNN
from .dataset_loader import DatasetLoader

import argparse
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import torchvision.utils as vutils
import torch
import torch.nn as nn
import torch.optim as optim

def train(metadata_file, root_dir):

    name = input("what would you like to call your model?: ")
    
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((256, 256)),  # Resize images if necessary
        transforms.ToTensor(),          # Convert images to tensors
    ])

    # Create dataset and dataloader
    dataset = DatasetLoader(metadata_file=metadata_file, root_dir=root_dir, transform=transform) 
    print(f"Dataset length: {len(dataset)}")

    # Load one image to test
    try:
        sample_img = dataset[0]
        print(f"Sample image size: {sample_img.size()}")
    except FileNotFoundError as e:
        print(e)

    # Create DataLoader and Iterate
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    # Iterate over the DataLoader
    for i, batch in enumerate(dataloader):
        print(f"Batch {i+1}, Batch size: {batch.size()}")
        if i == 2:  # Only print first three batches
            break

    # Visualize Sample Images
    # Get a batch of training data
    for i, batch in enumerate(dataloader):
        if i == 0:  # Only visualize the first batch
            images = batch
            break

    # Make a grid from batch
    out = vutils.make_grid(images, padding=2, normalize=True)

    # Plot the grid
    plt.figure(figsize=(12, 12))
    plt.imshow(out.permute(1, 2, 0))
    plt.title('Batch of Images')
    plt.show()

    # Check for GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Initialize the model
    model = SRCNN().to(device)
    print("Initialized the model")

    # Define loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    print("Defined loss and optimizer")

    # Train the Model
    print("Training Started")
    num_epochs = 50

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        
        for batch_idx, inputs in enumerate(dataloader):
            inputs = inputs.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, inputs)  # Since it's an autoencoder, target is input
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            # Print batch progress
            if batch_idx % 10 == 0:
                print(f'Epoch {epoch+1}/{num_epochs}, Batch {batch_idx}/{len(dataloader)}, Loss: {loss.item()}')
        
        # Print epoch progress
        print(f'Epoch {epoch+1}/{num_epochs}, Average Loss: {running_loss/len(dataloader)}')

    # Save the model
    torch.save(model.state_dict(), f'{name}.pnn')
    print("Model saved")
