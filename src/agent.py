import numpy as np
from board import Board
import cv2 as cv
from collections import deque
import random
import keras

class Agent:
    def __init__(self):
        self.board = Board()
        self.to_save = True
        self.model_folder = 'models/'
        self.model_name = "vs_random_num_0_connect4_agent"
        self.model_suffix = '.h5'
        self.setHyperParameters()
        self.model_continuous = self.buildNN()
        self.model_step = self.buildNN()

    def setHyperParameters(self):
        self.state_size = self.board.BOARD_WIDTH * self.board.BOARD_HEIGHT
        self.action_size = self.board.BOARD_WIDTH
        self.test_episodes = 10

        self.gamma = 0.95 # discount rate
        self.epsilon = 1.0
        self.min_epsilon = 0.001
        self.epsilon_decay_rate = 0.997

        self.batch_size = 32
        self.memory = deque(maxlen=2000)
        self.train_start = 100


    def buildNN(self):
        model = keras.models.Sequential()
        model.add(keras.layers.Input(shape = self.state_size))
        model.add(keras.layers.Dense(32, activation='relu'))
        model.add(keras.layers.Dense(16, activation='relu'))
        model.add(keras.layers.Dense(8,  activation='relu'))
        model.add(keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss ='mse', optimizer = 'adam')
        return model

    def trainNN(self):
        # Sample from memory either the eniter memory or batch_size
        minibatch_size = min(len(self.memory), self.batch_size)
        minibatch = random.sample(self.memory, minibatch_size)
        state = np.zeros((minibatch_size, self.state_size))
        next_state = np.zeros((minibatch_size, self.state_size))
        action = [0]*minibatch_size
        reward = [0]*minibatch_size
        done = [False]*minibatch_size

        for i in range(minibatch_size):
            state[i] = minibatch[i][0]
            action[i] = minibatch[i][1]
            reward[i] = minibatch[i][2]
            next_state[i] = minibatch[i][3]
            done[i] = minibatch[i][4]

        # Should these be model_continuous or model_step
        target = self.model_step.predict(state, verbose = 0)
        target_next = self.model_step.predict(next_state, verbose = 0)
        for i in range(minibatch_size):
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                target[i][action[i]] = reward[i] + self.gamma * np.amax(target_next[i])
        self.model_continuous.fit(state, target, batch_size=minibatch_size, verbose = 0)

    def updateEpsilon(self):
        if len(self.memory) > self.train_start:
            self.epsilon = max(self.epsilon*self.epsilon_decay_rate,
                                self.min_epsilon)
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state,action,reward,next_state,done))

    def save(self, agent_number):
        if self.to_save:
            self.model_continuous.save(
                    self.model_folder + self.model_name \
                    + str(agent_number) + self.model_suffix)

    def load(self, agent_number = 0):
        name_to_load = self.model_folder + self.model_name \
                        + str(agent_number) + self.model_suffix
        self.model_continuous = keras.models.load_model(name_to_load)
        self.model_step = keras.models.load_model(name_to_load)

    def reshapeState(self, state):
        return np.reshape(state.flatten(),[1,self.state_size])

    def randomAction(self, actions):
        return np.random.choice(actions)

    # Get model that is updated periodically and use it to predict action
    # from state, which is using keras so convert to numpy
    # only consider viable actions
    # get argmax
    # convert back to all actions
    def bestAction(self, actions, state):
        return actions[np.argmax(self.model_step(state).numpy()[0][actions])]

    def takeAction(self, actions, state):
        if np.random.random() < self.epsilon:
             return self.randomAction(actions)
        return self.bestAction(actions, state)

    def update(self, state, action, reward, next_state, done):
        self.remember(state, action, reward, next_state, done)
        self.trainNN()
        self.updateEpsilon()

    def updateStepModel(self):
        self.model_step.set_weights(self.model_continuous.get_weights())

if __name__ == "__main__":
    np.random.seed(2)
    a = Agent()
    a.buildNN()
    brd = np.array([[1., -1., 1., -1., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0.]])
    state = a.reshapeState(brd)
    results = a.model_step(state).numpy()[0]
    print(results.shape)
    print(results)
    print(np.argmax(results))
    actions = [0,2,4,6]
    print(actions[np.argmax(results[actions])])
