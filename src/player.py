import numpy as np
from agent import Agent
from viewer import Viewer
from board import Board
import copy

class player:
    def __init__(self):
        self.agents = [Agent(), Agent()]
        self.viewer = Viewer()
        self.board = Board()
        self.episodes = 200
        win_draw_loss = {"wins": 0, "draws":0, "losses":0}
        red_and_yellow = {"red": copy.deepcopy(win_draw_loss),
                        "yellow": copy.deepcopy(win_draw_loss)}
        self.resultData = [copy.deepcopy(red_and_yellow),
                            copy.deepcopy(red_and_yellow)]

    def updateResults(self, result, last_team):
        other_team = -1*last_team + 1
        if result == 0:
            for i in range(2):
                self.resultData[i]["red"]["draws"] += 0.5
                self.resultData[i]["yellow"]["draws"] += 0.5
        elif result == 1:
            self.resultData[last_team]["yellow"]["wins"] += 1
            self.resultData[other_team]["red"]["losses"] += 1
        else:
            self.resultData[last_team]["red"]["wins"] += 1
            self.resultData[other_team]["yellow"]["losses"] += 1

    def printResults(self):
        agent_score = [0,0]
        for i in range(2):
            agent_score[i] = self.resultData[i]["red"]["wins"] \
                            + self.resultData[i]["yellow"]["wins"] \
                            + 0.5* (self.resultData[i]["red"]["draws"] \
                                    + self.resultData[i]["yellow"]["draws"])
        print("Score: {:.1f} : {:.1f}".format(
                        agent_score[0], agent_score[1]))

    def competeRandomAction(self):
        done = False
        team = np.random.choice([0,1])
        self.viewer.displayBoard(self.board.board, pause = -1)
        while not done:
            action = self.agents[team].randomAction(self.board.validActions())
            board, result, done = self.board.step(action)
            if done:
                if result != 0:
                    print("Team {} won!".format(
                            self.viewer.getColourOfTeam(result)))
                else:
                    print("Draw".format(result))
            self.viewer.displayBoard(self.board.board, pause = 200)
            team = -1*team + 1
        self.viewer.displayBoard(self.board.board, pause = 0)

    def trainAgents(self, view = False):
        for step in range(self.episodes):
            done = False
            self.board.resetBoard()
            team = np.random.choice([0,1])
            state = self.agents[team].reshapeState(self.board.board)
            result = 0
            if view:
                self.viewer.displayBoard(self.board.board, pause = -1)
            while not done:
                action = self.agents[team].takeAction(self.board.validActions(), state)
                next_state, result, done = self.board.step(action)
                next_state = self.agents[team].reshapeState(next_state)
                self.agents[team].update(state, action, abs(result),
                                        next_state, done)
                if view:
                    self.viewer.displayBoard(self.board.board, pause = 200)
                team = -1*team + 1
                state = next_state

            if view:
                self.viewer.displayBoard(self.board.board, pause = 400)
            last_team = -1*team + 1
            self.updateResults(result, last_team)
            self.printResults()
            for i in range(2):
                self.agents[i].updateStepModel()
        for i in range(2):
            self.agents[i].save(i)

    def trainAgentsVsRandom(self, view = False):
        for step in range(self.episodes):
            done = False
            self.board.resetBoard()
            team = np.random.choice([0,1])
            state = self.agents[team].reshapeState(self.board.board)
            result = 0
            action = 0
            if view:
                self.viewer.displayBoard(self.board.board, pause = -1)
            while not done:
                if team == 1:
                    action = self.agents[team].randomAction(self.board.validActions())
                action = self.agents[team].takeAction(self.board.validActions(), state)
                next_state, result, done = self.board.step(action)
                next_state = self.agents[team].reshapeState(next_state)
                if team == 0:
                    self.agents[team].update(state, action, abs(result),
                                        next_state, done)
                if view:
                    self.viewer.displayBoard(self.board.board, pause = 200)
                team = -1*team + 1
                state = next_state
            if view:
                self.viewer.displayBoard(self.board.board, pause = 400)
            last_team = -1*team + 1
            self.updateResults(result, last_team)
            self.printResults()
            self.agents[0].updateStepModel()
        print("Epsilon: {}".format(self.agents[0].epsilon))
        self.agents[0].save(0)


    def playVsHuman(self, first = ''):
        agent = self.agents[0]
        agent.load()
        whos_turn = np.random.choice(['agent','human'])
        if first == 'agent':
            whos_turn = 'agent'
        elif first == 'human':
            whos_turn = 'human'
        self.board.resetBoard()
        board = self.board.board
        done = False
        action = 0
        while not done:
            available_actions = self.board.validActions()
            if whos_turn == 'human':
                print("Your turn!")
                action = self.viewer.getHumanAction(self.board.board)
            else:
                state = agent.reshapeState(board)
                action = agent.bestAction(available_actions, state)
            board, result, done = self.board.step(action)
            self.viewer.displayBoard(self.board.board, pause = 20)
            if done:
                if result != 0:
                    print("{} won with {} won!".format(whos_turn,
                            self.viewer.getColourOfTeam(result)))
                else:
                    print("Draw".format(result))
            if whos_turn == 'human':
                whos_turn = 'agent'
            else:
                whos_turn = 'human'


    def humanVsHuman(self):
        self.board.resetBoard()
        done = False
        action = 0
        while not done:
            available_actions = self.board.validActions()
            action = self.viewer.getHumanAction(self.board.board)
            while action not in available_actions:
                print("Action {} not an option, please try one of {}".format(
                    action, available_actions))
                action = self.viewer.getHumanAction(self.board.board)
            next_board, result, done = self.board.step(action)
            if done:
                if result != 0:
                    print("Team {} won!".format(
                            self.viewer.getColourOfTeam(result)))
                else:
                    print("Draw".format(result))

if __name__ == "__main__":
    p = player()
    # p.trainAgentsVsRandom()
    p.playVsHuman()
    # p.trainAgents()
    # p.humanVsHuman()
