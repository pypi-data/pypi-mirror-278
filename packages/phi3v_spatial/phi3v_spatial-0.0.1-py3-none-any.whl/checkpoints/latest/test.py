import torch
from transformers import AutoModelForImageSequenceClassification, AutoTokenizer

# Define the checkpoint path
checkpoint_path = "path/to/checkpoint"

# Load the model from the checkpoint
model = AutoModelForImageSequenceClassification.from_pretrained(checkpoint_path)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)

# Get the input from the command line
text_input = input("Enter the text: ")
# Get the image path from the command line
image_path = input("Enter the image path: ")

# Define your image(s)
images = [image_path]  # Replace [...] with your image(s)

# Tokenize the text and images
inputs = tokenizer(text_input, images, padding=True, truncation=True, return_tensors="pt")

# Forward pass through the model
outputs = model(**inputs)

# Get the predicted labels
predicted_labels = torch.argmax(outputs.logits, dim=1)

# Print the predicted labels
print(predicted_labels)
# Perform one inference
with torch.no_grad():
  # Get the sequence embeddings
  sequence_embeddings = model.get_sequence_embeddings(**inputs)

# Process the sequence embeddings
# ...

# Perform your desired operations on the sequence embeddings
# ...

# Print the processed sequence embeddings
print(sequence_embeddings)