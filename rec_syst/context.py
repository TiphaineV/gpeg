{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Text classification with Pytorch"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The goal of this TP is double: an introduction to using Pytorch for treating textual data, and implementing neural classification models that we can apply to IMDB data - and then compare to models implemented in the previous TPs. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import torch\n",
    "import torch.nn as nn"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### A (very small) introduction to pytorch"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Pytorch Tensors are very similar to Numpy arrays, with the added benefit of being usable on GPU. For a short tutorial on various methods to create tensors of particular types, see [this link](https://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html#sphx-glr-beginner-blitz-tensor-tutorial-py).\n",
    "The important things to note are that Tensors can be created empty, from lists, and it is very easy to convert a numpy array into a pytorch tensor, and inversely."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "a = torch.LongTensor(5)\n",
    "b = torch.LongTensor([5])\n",
    "\n",
    "print(a)\n",
    "print(b)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "a = torch.FloatTensor([2])\n",
    "b = torch.FloatTensor([3])\n",
    "\n",
    "print(a + b)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The main interest in us using Pytorch is the ```autograd``` package. ```torch.Tensor```objects have an attribute ```.requires_grad```; if set as True, it starts to track all operations on it. When you finish your computation, can call ```.backward()``` and all the gradients are computed automatically (and stored in the ```.grad``` attribute).\n",
    "\n",
    "One way to easily cut a tensor from the computational once it is not needed anymore is to use ```.detach()```.\n",
    "More info on automatic differentiation in pytorch on [this link](https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html#sphx-glr-beginner-blitz-autograd-tutorial-py)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "x = torch.tensor(1., requires_grad=True)\n",
    "w = torch.tensor(2., requires_grad=True)\n",
    "b = torch.tensor(3., requires_grad=True)\n",
    "\n",
    "# Build a computational graph.\n",
    "y = w * x + b    # y = 2 * x + 3\n",
    "\n",
    "# Compute gradients.\n",
    "y.backward()\n",
    "\n",
    "# Print out the gradients.\n",
    "print(x.grad)    # x.grad = 2 \n",
    "print(w.grad)    # w.grad = 1 \n",
    "print(b.grad)    # b.grad = 1 "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "x = torch.randn(10, 3)\n",
    "y = torch.randn(10, 2)\n",
    "\n",
    "# Build a fully connected layer.\n",
    "linear = nn.Linear(3, 2)\n",
    "for name, p in linear.named_parameters():\n",
    "    print(name)\n",
    "    print(p)\n",
    "\n",
    "# Build loss function - Mean Square Error\n",
    "criterion = nn.MSELoss()\n",
    "\n",
    "# Forward pass.\n",
    "pred = linear(x)\n",
    "\n",
    "# Compute loss.\n",
    "loss = criterion(pred, y)\n",
    "print('Initial loss: ', loss.item())\n",
    "\n",
    "# Backward pass.\n",
    "loss.backward()\n",
    "\n",
    "# Print out the gradients.\n",
    "print ('dL/dw: ', linear.weight.grad) \n",
    "print ('dL/db: ', linear.bias.grad)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# You can perform gradient descent manually, with an in-place update ...\n",
    "linear.weight.data.sub_(0.01 * linear.weight.grad.data)\n",
    "linear.bias.data.sub_(0.01 * linear.bias.grad.data)\n",
    "\n",
    "# Print out the loss after 1-step gradient descent.\n",
    "pred = linear(x)\n",
    "loss = criterion(pred, y)\n",
    "print('Loss after one update: ', loss.item())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use the optim package to define an Optimizer that will update the weights of the model.\n",
    "optimizer = torch.optim.SGD(linear.parameters(), lr=0.01)\n",
    "\n",
    "# By default, gradients are accumulated in buffers( i.e, not overwritten) whenever .backward()\n",
    "# is called. Before the backward pass, we need to use the optimizer object to zero all of the\n",
    "# gradients.\n",
    "optimizer.zero_grad()\n",
    "loss.backward()\n",
    "\n",
    "# Calling the step function on an Optimizer makes an update to its parameters\n",
    "optimizer.step()\n",
    "\n",
    "# Print out the loss after the second step of gradient descent.\n",
    "pred = linear(x)\n",
    "loss = criterion(pred, y)\n",
    "print('Loss after two updates: ', loss.item())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Tools for data processing "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "```torch.utils.data.Dataset``` is an abstract class representing a dataset. Your custom dataset should inherit ```Dataset``` and override the following methods:\n",
    "- ```__len__``` so that ```len(dataset)``` returns the size of the dataset.\n",
    "- ```__getitem__``` to support the indexing such that ```dataset[i]``` can be used to get the i-th sample\n",
    "\n",
    "Here is a toy example: "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "toy_corpus = ['I walked down down the boulevard',\n",
    "              'I walked down the avenue',\n",
    "              'I ran down the boulevard',\n",
    "              'I walk down the city',\n",
    "              'I walk down the the avenue']\n",
    "\n",
    "toy_categories = [0, 0, 1, 0, 0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from torch.utils.data import Dataset, DataLoader\n",
    "\n",
    "class CustomDataset(Dataset):\n",
    "    # A pytorch dataset class for holding data for a text classification task.\n",
    "    def __init__(self, data, categories):\n",
    "        # Upon creating the Dataset object, store the data in an attribute\n",
    "        # Split the text data and labels from each other\n",
    "        self.X, self.Y = [], []\n",
    "        for x, y in zip(data, categories):\n",
    "            # We will propably need to preprocess the data - have it done in a separate method\n",
    "            # We do it here because we might need corpus-wide info to do the preprocessing \n",
    "            # For example, cutting all examples to the same length\n",
    "            self.X.append(self.preprocess(x))\n",
    "            self.Y.append(y)\n",
    "                \n",
    "    # Method allowing you to preprocess data                      \n",
    "    def preprocess(self, text):\n",
    "        text_pp = text.lower().strip()\n",
    "        return text_pp\n",
    "    \n",
    "    # Overriding the method __len__ so that len(CustomDatasetName) returns the number of data samples                     \n",
    "    def __len__(self):\n",
    "        return len(self.Y)\n",
    "   \n",
    "    # Overriding the method __getitem__ so that CustomDatasetName[i] returns the i-th sample of the dataset                      \n",
    "    def __getitem__(self, idx):\n",
    "           return self.X[idx], self.Y[idx]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "toy_dataset = CustomDataset(toy_corpus, toy_categories)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(len(toy_dataset))\n",
    "for i in range(len(toy_dataset)):\n",
    "    print(toy_dataset[i])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "```torch.utils.data.DataLoader``` is what we call an iterator, which provides very useful features:\n",
    "- Batching the data\n",
    "- Shuffling the data\n",
    "- Load the data in parallel using multiprocessing workers.\n",
    "and can be created very simply from a ```Dataset```. Continuing on our simple example: "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "toy_dataloader = DataLoader(toy_dataset, batch_size = 2, shuffle = True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "for e in range(3):\n",
    "    print(\"Epoch:\" + str(e))\n",
    "    for x, y in toy_dataloader:\n",
    "        print(\"Batch: \" + str(x) + \"; labels: \" + str(y))  "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Data processing of a text dataset\n",
    "\n",
    "Now, we would like to apply what we saw to our case, and **create a specific class** ```TextClassificationDataset``` **inheriting** ```Dataset``` that will:\n",
    "- Create a vocabulary from the data (use what we saw in the previous TP)\n",
    "- Preprocess the data using this vocabulary, adding whatever we need for our pytorch model\n",
    "- Have a ```__getitem__``` method that allows us to use the class with a ```Dataloader``` to easily build batches."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import sys\n",
    "from torch.nn import functional as F\n",
    "import numpy as np\n",
    "import random\n",
    "\n",
    "from nltk import word_tokenize\n",
    "from torch.nn.utils.rnn import pad_sequence"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "First, we get the filenames and the corresponding categories: "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from glob import glob\n",
    "filenames_neg = sorted(glob(os.path.join('.', 'data', 'imdb1', 'neg', '*.txt')))\n",
    "filenames_pos = sorted(glob(os.path.join('.', 'data', 'imdb1', 'pos', '*.txt')))\n",
    "filenames = filenames_neg + filenames_pos\n",
    "\n",
    "# The first half of the elements of the list are string of negative reviews, and the second half positive ones\n",
    "# We create the labels, as an array of [1,len(texts)], filled with 1, and change the first half to 0\n",
    "categories = np.ones(len(filenames), dtype=np.int)\n",
    "categories[:len(filenames_neg)] = 0.\n",
    "\n",
    "print(\"%d documents\" % len(filenames))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We will need to create a ```TextClassificationDataset``` and a ```Dataloader``` for the training data, the validation data, and the testing data. We need to implement a function that will help us split the data in three, according to proportions we give in input."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a function allowing you to simply shuffle then split the filenames and categories into the desired\n",
    "# proportions for a training, validation and testing set. \n",
    "def get_splits(x, y, splits):\n",
    "    \"\"\"\n",
    "    The idea is to use an index list as reference:\n",
    "    Indexes = [0 1 2 3 4 5 6 7 8 9]\n",
    "    To shuffle it randomly:\n",
    "    Indexes = [7 1 5 0 2 9 8 6 4 3]\n",
    "    We need 'splits' to contain 2 values. Assuming those are = (0.8, 0.1), we'll have:\n",
    "    Train_indexes = [7 1 5 0 2 9 8 6]\n",
    "    Valid_indexes = [4]\n",
    "    Test_indexes = [3]\n",
    "    \"\"\"\n",
    "    # Create an index list and shuffle it - use the function random.shuffle\n",
    "    # -- A compléter --\n",
    "    \n",
    "    # Find the two indexes we'll use to cut the lists from the splits\n",
    "    # -- A compléter -- \n",
    "    \n",
    "    # Do the cutting (careful: you can't use a list as index for a list - this only works with tensors)\n",
    "    # (you need to use list comprehensions - or go through numpy)\n",
    "    train_x, train_y = # A compléter\n",
    "    valid_x, valid_y = # A compléter\n",
    "    test_x, test_y = # A compléter\n",
    "    return (train_x, train_y), (valid_x, valid_y), (test_x, test_y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Choose the training, validation, testing splits\n",
    "splits = (0.8, 0.1)\n",
    "(train_f, train_c), (valid_f, valid_c), (test_f, test_c) = get_splits(filenames, categories, splits)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We can now implement our ```TextClassificationDataset``` class, that we will build from:\n",
    "- A list of path to the IMDB files in the training set: ```path_to_file```\n",
    "- A list of the corresponding categories: ```categories```\n",
    "We will add three optional arguments:\n",
    "- First, a way to input a vocabulary (so that we can re-use the training vocabulary on the validation and training ```TextClassificationDataset```). By default, the value of the argument is ```None```.\n",
    "- In order to work with batches, we will need to have sequences of the same size. That can be done via **padding** but we will still need to limit the size of documents (to avoid having batches of huge sequences that are mostly empty because of one very long documents) to a ```max_length```. Let's put it to 100 by default.\n",
    "- Lastly, a ```min_freq``` that indicates how many times a word must appear to be taken in the vocabulary. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The idea behind **padding** is to transform a list of pytorch tensors (of maybe different length) into a two dimensional tensor - which we can see as a batch. The size of the first dimension is the one of the longest tensor - and other are **padded** with a chosen symbol: here, we choose 0. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "tensor_1 = torch.LongTensor([1, 4, 5])\n",
    "tensor_2 = torch.LongTensor([2])\n",
    "tensor_3 = torch.LongTensor([6, 7])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "tensor_padded = pad_sequence([tensor_1, tensor_2, tensor_3], batch_first=True, padding_value = 0)\n",
    "print(tensor_padded)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class TextClassificationDataset(Dataset):\n",
    "    def __init__(self, paths_to_files, categories, vocab = None, max_length = 100, min_freq = 5):\n",
    "        # Read all files and put the data in a list of strings\n",
    "        self.data = # A compléter\n",
    "        \n",
    "        # Set the maximum length we will keep for the sequences\n",
    "        self.max_length = max_length\n",
    "        \n",
    "        # Allow to import a vocabulary (for valid/test datasets, that will use the training vocabulary)\n",
    "        if vocab is not None:\n",
    "            self.word2idx, self.idx2word = vocab\n",
    "        else:\n",
    "            # If no vocabulary imported, build it (and reverse)\n",
    "            self.word2idx, self.idx2word = self.build_vocab(self.data, min_freq)\n",
    "        \n",
    "        # We then need to tokenize the data .. \n",
    "        tokenized_data = # A compléter\n",
    "        # Transform words into lists of indexes ... (use the .get() method to redirect unknown words to the UNK token)\n",
    "        indexed_data = # A compléter\n",
    "        # And transform this list of lists into a list of Pytorch LongTensors\n",
    "        tensor_data = # A compléter\n",
    "        # And the categories into a FloatTensor\n",
    "        tensor_y =\n",
    "        # To finally cut it when it's above the maximum length\n",
    "        cut_tensor_data = # A compléter\n",
    "        \n",
    "        # Now, we need to use the pad_sequence function to have the whole dataset represented as one tensor,\n",
    "        # containing sequences of the same length. We choose the padding_value to be 0, the we want the\n",
    "        # batch dimension to be the first dimension \n",
    "        self.tensor_data = # A compléter\n",
    "        self.tensor_y = tensor_y\n",
    "        \n",
    "    def __len__(self):\n",
    "        return len(self.data)\n",
    "\n",
    "    def __getitem__(self, idx):\n",
    "        # The iterator just gets one particular example with its category\n",
    "        # The dataloader will take care of the shuffling and batching\n",
    "        if torch.is_tensor(idx):\n",
    "            idx = idx.tolist()\n",
    "        return self.tensor_data[idx], self.tensor_y[idx] \n",
    "    \n",
    "    def build_vocab(self, corpus, count_threshold):\n",
    "        \"\"\"\n",
    "        Same as in the previous TP: we want to output word_index, a dictionary containing words \n",
    "        and their corresponding indexes as {word : indexes} \n",
    "        But we also want the reverse, which is a dictionary {indexes: word}\n",
    "        Don't forget to add a UNK token that we need when encountering unknown words\n",
    "        We also choose '0' to represent the padding index, so begin the vocabulary index at 1 ! \n",
    "        \"\"\"\n",
    "        # A compléter\n",
    "        return word_index, idx_word\n",
    "    \n",
    "    def get_vocab(self):\n",
    "        # A simple way to get the training vocab when building the valid/test \n",
    "        return self.word2idx, self.idx2word"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "training_dataset = TextClassificationDataset(train_f, train_c)\n",
    "training_word2idx, training_idx2word = training_dataset.get_vocab()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "valid_dataset = TextClassificationDataset(valid_f, valid_c, (training_word2idx, training_idx2word))\n",
    "test_dataset = TextClassificationDataset(test_f, test_c, (training_word2idx, training_idx2word))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "training_dataloader = DataLoader(training_dataset, batch_size = 200, shuffle=True)\n",
    "valid_dataloader = DataLoader(valid_dataset, batch_size = 25)\n",
    "test_dataloader = DataLoader(test_dataset, batch_size = 25)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(training_dataset[0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "example_batch = next(iter(training_dataloader))\n",
    "print(example_batch[0].size())\n",
    "print(example_batch[1].size())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### A simple averaging model\n",
    "\n",
    "Now, we will implement in Pytorch what we did in the previous TP: a simple averaging model. For each model we will implement, we need to create a class which inherits from ```nn.Module``` and redifine the ```__init__``` method as well as the ```forward``` method."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Models are usually implemented as custom nn.Module subclass\n",
    "# We need to redefine the __init__ method, which creates the object\n",
    "# We also need to redefine the forward method, which transform the input into outputs\n",
    "\n",
    "class AveragingModel(nn.Module):    \n",
    "    def __init__(self, embedding_dim, vocabulary_size):\n",
    "        super().__init__()\n",
    "        # Create an embedding object. Be careful to padding - you need to increase the vocabulary size by one !\n",
    "        # Look into the arguments of the nn.Embedding class\n",
    "        self.embeddings = # A compléter\n",
    "        # Create a linear layer that will transform the mean of the embeddings into a classification score\n",
    "        self.linear = # A compléter\n",
    "        \n",
    "        # No need for sigmoid, it will be into the criterion ! \n",
    "        \n",
    "    def forward(self, inputs):\n",
    "        # Remember: the inpts are written as Batch_size * seq_length * embedding_dim\n",
    "        # First, take the mean of the embeddings of the document\n",
    "        x = # A compléter\n",
    "        # Then make it go through the linear layer and remove the extra dimension with the method .squeeze()\n",
    "        o = # A compléter\n",
    "        return o"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import torch.optim as optim"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "model = AveragingModel(300, len(training_word2idx))\n",
    "# Create an optimizer\n",
    "opt = optim.Adam(model.parameters(), lr=0.0025, betas=(0.9, 0.999))\n",
    "# The criterion is a binary cross entropy loss based on logits - meaning that the sigmoid is integrated into the criterion\n",
    "criterion = nn.BCEWithLogitsLoss()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Implement a training function, which will train the model with the corresponding optimizer and criterion,\n",
    "# with the appropriate dataloader, for one epoch.\n",
    "\n",
    "def train_epoch(model, opt, criterion, dataloader):\n",
    "    model.train()\n",
    "    losses = []\n",
    "    for i, (x, y) in enumerate(dataloader):\n",
    "        opt.zero_grad()\n",
    "        # (1) Forward\n",
    "        pred = # A compléter\n",
    "        # (2) Compute the loss \n",
    "        loss = # A compléter\n",
    "        # (3) Compute gradients with the criterion\n",
    "        # A compléter\n",
    "        # (4) Update weights with the optimizer\n",
    "        # A compléter       \n",
    "        losses.append(loss.item())\n",
    "        # Count the number of correct predictions in the batch - here, you'll need to use the sigmoid\n",
    "        num_corrects = # A compléter\n",
    "        acc = 100.0 * num_corrects/len(y)\n",
    "        \n",
    "        if (i%20 == 0):\n",
    "            print(\"Batch \" + str(i) + \" : training loss = \" + str(loss.item()) + \"; training acc = \" + str(acc.item()))\n",
    "    return losses"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Same for the evaluation ! We don't need the optimizer here. \n",
    "def eval_model(model, criterion, evalloader):\n",
    "    model.eval()\n",
    "    total_epoch_loss = 0\n",
    "    total_epoch_acc = 0\n",
    "    with torch.no_grad():\n",
    "        for i, (x, y) in enumerate(evalloader):\n",
    "            pred = # A compléter\n",
    "            loss = # A compléter\n",
    "            num_corrects = # A compléter\n",
    "            acc = 100.0 * num_corrects/len(y)\n",
    "            total_epoch_loss += loss.item()\n",
    "            total_epoch_acc += acc.item()\n",
    "\n",
    "    return total_epoch_loss/(i+1), total_epoch_acc/(i+1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# A function which will help you execute experiments rapidly - with a early_stopping option when necessary. \n",
    "def experiment(model, opt, criterion, num_epochs = 5, early_stopping = True):\n",
    "    train_losses = []\n",
    "    if early_stopping: \n",
    "        best_valid_loss = 10. \n",
    "    print(\"Beginning training...\")\n",
    "    for e in range(num_epochs):\n",
    "        print(\"Epoch \" + str(e+1) + \":\")\n",
    "        train_losses += train_epoch(model, opt, criterion, training_dataloader)\n",
    "        valid_loss, valid_acc = eval_model(model, criterion, valid_dataloader)\n",
    "        print(\"Epoch \" + str(e+1) + \" : Validation loss = \" + str(valid_loss) + \"; Validation acc = \" + str(valid_acc))\n",
    "        if early_stopping:\n",
    "            if valid_loss < best_valid_loss:\n",
    "                best_valid_loss = valid_loss\n",
    "            else:\n",
    "                print(\"Early stopping.\")\n",
    "                break  \n",
    "    test_loss, test_acc = eval_model(model, criterion, test_dataloader)\n",
    "    print(\"Epoch \" + str(e+1) + \" : Test loss = \" + str(test_loss) + \"; Test acc = \" + str(test_acc))\n",
    "    return train_losses"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "train_losses = experiment(model, opt, criterion)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### With Glove embeddings: \n",
    "\n",
    "Now, we would like to integrate pre-trained word embeddings into our model ! Let's use again the functions that we used in the previous TP:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import gensim.downloader as api\n",
    "loaded_glove_model = api.load(\"glove-wiki-gigaword-300\")\n",
    "loaded_glove_embeddings = loaded_glove_model.vectors"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_glove_adapted_embeddings(glove_model, input_voc):\n",
    "    keys = {i: glove_model.vocab.get(w, None) for w, i in input_voc.items()}\n",
    "    index_dict = {i: key.index for i, key in keys.items() if key is not None}\n",
    "    embeddings = np.zeros((len(input_voc)+1,glove_model.vectors.shape[1]))\n",
    "    for i, ind in index_dict.items():\n",
    "        embeddings[i] = glove_model.vectors[ind]\n",
    "    return embeddings\n",
    "\n",
    "GloveEmbeddings = get_glove_adapted_embeddings(loaded_glove_model, training_word2idx)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(GloveEmbeddings.shape)\n",
    "# We should check that the \"padding\" vector is at zero\n",
    "print(GloveEmbeddings[0])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Here, implement a ```PretrainedAveragingModel``` very similar to the previous model, using the ```nn.Embedding``` method ```from_pretrained()``` to initialize the embeddings from a numpy array. Use the ```requires_grad_``` method to specify if the model must fine-tune the embeddings or not ! "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class PretrainedAveragingModel(nn.Module):\n",
    "    # A compléter"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Questions: \n",
    "- What are the results **with and without fine-tuning of embeddings imported from GloVe** ?\n",
    "- Make hypothesis based on your intuition and the class on how\n",
    "    - the number of documents (take only a portion of the 25.000 documents !)\n",
    "    - the size of the vocabulary (change the minimum frequency of words to be taken in the vocabulary ! )\n",
    "  will impact results, in the three cases (No pre-training, pre-training without fine-tuning, pretraining with fine-tuning).\n",
    "- Verify your hypothesis with experiments and analyze your results !"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### LSTM Cells in pytorch"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create a toy example of LSTM: \n",
    "lstm = nn.LSTM(3, 3)  # Input dim is 3, output dim is 3\n",
    "inputs = [torch.randn(1, 3) for _ in range(5)]  # make a sequence of length 5\n",
    "\n",
    "# LSTMs expect inputs having 3 dimensions:\n",
    "# - The first dimension is the temporal dimension, along which we (in our case) have the different words\n",
    "# - The second dimension is the batch dimension, along which we stack the independant batches\n",
    "# - The third dimension is the feature dimension, along which are the features of the vector representing the words\n",
    "\n",
    "# In our toy case, we have inputs and outputs containing 3 features (third dimension !)\n",
    "# We created a sequence of 5 different inputs (first dimension !)\n",
    "# We don't use batch (the second dimension will have one lement)\n",
    "\n",
    "# We need an initial hidden state, of the right sizes for dimension 2/3, but with only one temporal element:\n",
    "# Here, it is:\n",
    "hidden = (torch.randn(1, 1, 3),\n",
    "          torch.randn(1, 1, 3))\n",
    "# Why do we create a tuple of two tensors ? Because we use LSTMs: remember that they use two sets of weights,\n",
    "# and two hidden states (Hidden state, and Cell state).\n",
    "# If you don't remember, read: https://colah.github.io/posts/2015-08-Understanding-LSTMs/\n",
    "# If we used a classic RNN, we would simply have:\n",
    "# hidden = torch.randn(1, 1, 3)\n",
    "\n",
    "# The naive way of applying a lstm to inputs is to apply it one step at a time, and loop through the sequence\n",
    "for i in inputs:\n",
    "    # After each step, hidden contains the hidden states (remember, it's a tuple of two states).\n",
    "    out, hidden = lstm(i.view(1, 1, -1), hidden)\n",
    "    \n",
    "# Alternatively, we can do the entire sequence all at once.\n",
    "# The first value returned by LSTM is all of the Hidden states throughout the sequence.\n",
    "# The second is just the most recent Hidden state and Cell state (you can compare the values)\n",
    "# The reason for this is that:\n",
    "# \"out\" will give you access to all hidden states in the sequence, for each temporal step\n",
    "# \"hidden\" will allow you to continue the sequence and backpropagate later, with another sequence\n",
    "inputs = torch.cat(inputs).view(len(inputs), 1, -1)\n",
    "hidden = (torch.randn(1, 1, 3), torch.randn(1, 1, 3))  # Re-initialize\n",
    "out, hidden = lstm(inputs, hidden)\n",
    "print(out)\n",
    "print(hidden)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Creating our own LSTM Model\n",
    "\n",
    "We'll implement now a LSTM model, taking the same inputs and also outputing a score for the sentence."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class LSTMModel(nn.Module):\n",
    "    def __init__(self, embedding_dim, vocabulary_size, hidden_dim, embeddings=None, fine_tuning=False):\n",
    "        # A compléter      \n",
    "\n",
    "    def forward(self, inputs):\n",
    "        # A compléter  "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### And with a CNN ? "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class CNNModel(nn.Module):\n",
    "    def __init__(self, embedding_dim, vocabulary_size, window_size: int = 16, filter_multiplier = 64):\n",
    "        # A compléter\n",
    "        \n",
    "    def forward(self, inputs): \n",
    "        # A compléter"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Questions: \n",
    "- What do you see with a simple application of LSTMs and CNNs models ? \n",
    "- Similarly, make hypothesis based on your intuition and the class on how\n",
    "    - the number of documents \n",
    "    - the size of the vocabulary \n",
    "  will impact results, in the three cases (No pre-training, pre-training without fine-tuning, pretraining with fine-tuning) for the LSTM **or** CNN (and the CNN should be quite faster !) and verify your hypothesis with experiments and analyze your results !\n",
    "- Present your results in a clear and synthetic way (table, figures) and be careful to experimental methodology. Notably, you should fix hyperparameters before making comparisons (you should use maximum length of sentences and batch sizes to accelerate training - similarly, using a SGD optimizer will be faster than Adam) ! "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}