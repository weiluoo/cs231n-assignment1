import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_class = W.shape[1]
  for i in range(num_train):
    f = X[i].dot(W)
    f -= np.max(f)
    p = np.exp(f[y[i]]) / np.sum(np.exp(f))
    loss += - np.log(p)

    dW[:, y[i]] -= (1 - np.exp(f[y[i]]) / np.sum(np.exp(f))) * X[i]
    for j in range(num_class):
      if j == y[i]:
        continue
      dW[:, j] += np.exp(f[j]) / np.sum(np.exp(f)) * X[i]

  loss /= num_train
  dW /= num_train
  loss += reg * np.sum(W * W)
  dW += 2 * reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  f = X.dot(W)
  f -= np.max(f, axis=1).reshape(num_train, 1)
  f_exp = np.exp(f)
  loss = np.sum(-np.log(f_exp[range(num_train), y] / np.sum(f_exp, axis=1)))
  loss /= num_train
  loss += reg * np.sum(W * W)

  corr_mask = np.zeros(f.shape)
  corr_mask[range(num_train), y] = 1 - f_exp[range(num_train), y] / np.sum(f_exp, axis=1)
  loss_mask = f_exp / np.sum(f_exp, axis=1).reshape(num_train, 1)
  loss_mask[range(num_train), y] = 0
  dW = X.T.dot(loss_mask) - X.T.dot(corr_mask)
  dW /= num_train
  dW += 2 * reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

