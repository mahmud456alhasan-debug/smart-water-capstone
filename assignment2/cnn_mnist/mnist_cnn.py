import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from model import DigitCNN
import argparse
import numpy as np
import matplotlib.pyplot as plt
import random

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# Define transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Load MNIST dataset
train_dataset = torchvision.datasets.MNIST(root='./data/MNIST', train=True,
                                           download=True, transform=transform)
test_dataset = torchvision.datasets.MNIST(root='./data/MNIST', train=False,
                                          download=True, transform=transform)

def train():
    # Create data loaders
    batch_size = 64
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size,
                                               shuffle=True)
    
    # Initialize model, loss function, and optimizer
    model = DigitCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Train the model
    num_epochs = 5
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')
    
    # Save the trained model
    torch.save(model.state_dict(), 'mnist_cnn_model.pth')
    print('Model saved to mnist_cnn_model.pth')

def evaluate():
    # Create data loader for test set
    batch_size = 64
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=batch_size,
                                              shuffle=False)
    
    # Load the trained model
    model = DigitCNN().to(device)
    model.load_state_dict(torch.load('mnist_cnn_model.pth'))
    model.eval()
    
    # Evaluate the model
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Calculate accuracy
    accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
    print(f'Test accuracy: {accuracy:.4f}')
    
    # Print classification report
    from sklearn.metrics import classification_report, confusion_matrix
    print('Classification report:')
    print(classification_report(all_labels, all_preds))
    
    # Compute confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.get_cmap('Blues'))
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(10)
    plt.xticks(tick_marks, [str(i) for i in range(10)])
    plt.yticks(tick_marks, [str(i) for i in range(10)])
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    print('Confusion matrix saved as confusion_matrix.png')
    plt.close()

def predict(index):
    # Load the trained model
    model = DigitCNN().to(device)
    model.load_state_dict(torch.load('mnist_cnn_model.pth'))
    model.eval()
    
    # Get the specified test image
    image, label = test_dataset[index]
    image = image.unsqueeze(0).to(device)  # Add batch dimension
    
    # Make prediction
    with torch.no_grad():
        output = model(image)
        probabilities = torch.nn.functional.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    true_label = label
    predicted_label = predicted.item()
    confidence_score = confidence.item()
    
    print(f'True label: {true_label}')
    print(f'Predicted label: {predicted_label}')
    print(f'Confidence score: {confidence_score:.4f}')

def demo():
    # Load the trained model
    model = DigitCNN().to(device)
    model.load_state_dict(torch.load('mnist_cnn_model.pth'))
    model.eval()
    
    # Randomly select 10 indices from the test dataset
    indices = random.sample(range(len(test_dataset)), 10)
    
    # Create a figure with subplots
    fig, axes = plt.subplots(2, 5, figsize=(12, 6))
    axes = axes.flatten()
    
    for i, idx in enumerate(indices):
        # Get the image and label
        image, label = test_dataset[idx]
        image_tensor = image.unsqueeze(0).to(device)  # Add batch dimension
        
        # Make prediction
        with torch.no_grad():
            output = model(image_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        true_label = label
        predicted_label = predicted.item()
        confidence_score = confidence.item()
        
        # Plot the image
        axes[i].imshow(image.squeeze(), cmap='gray')
        axes[i].set_title(f'True: {true_label}, Pred: {predicted_label}\nConf: {confidence_score:.2f}')
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.savefig('demo_results.png')
    print('Demo results saved as demo_results.png')
    plt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MNIST CNN Training/Evaluation/Prediction/Demo')
    parser.add_argument('--mode', type=str, required=True, choices=['train', 'eval', 'predict', 'demo'],
                        help='Mode: train, eval, predict, or demo')
    parser.add_argument('--index', type=int, default=0,
                        help='Index of test image for predict mode (default: 0)')
    
    args = parser.parse_args()
    
    if args.mode == 'train':
        train()
    elif args.mode == 'eval':
        evaluate()
    elif args.mode == 'predict':
        predict(args.index)
    elif args.mode == 'demo':
        demo()