from globals import *

#Variables
N_STATES = 6
ACTIONS = []

#Hyper factors
GREEDINESS = 0.9 #Greediness factor. How much randomness is introduced in the action selection. In fancy math version of update algorithm, this is Epsilon.
LEARNING_RATE = 0.2 #Learning rate. In fancy math version of update algorithm, this is Alpha.
REWARD_DECAY = 0.9 #Reward decay. As far as I understand it, after every step, the final reward is multiplied by the reward decay.
#The AI will strive to maximize it's reward, so because of the reward decay, it will strive to get to the reward as fast as possible.
#In fancy math version of update algorithm, this is Gamma.
MAX_EPISODES = 13 #Maximum amount of episodes
FRESH_TIME = 0.3 #Fresh time for 1 move. NOTE: will probably remove this, and simply request a new action once the previous one has completed

#q table: used for selecting the action. all decision making is based on this
#q table with 4 states and 2 actions:
#           action 1    action 2
#state 0    0           0
#state 1    0           0
#state 2    0           0
#state 3    0           0
#0 is the reward here

def observation_to_state(observation) :
    #The AI has zero frame of reference, so it does not matter how we encode our observation data, as long as it's processable by the "brain".
    return str(observation) #For now, we can just take the data and make it a string.

class RL_Brain() :
    def __init__(self, actions) :
        self.actions = actions
        self.GREEDINESS = 0.9
        self.LEARNING_RATE = 0.1
        self.REWARD_DECAY = 0.9

        self.episode = 1
        self.steps = 0
        self.max_steps = 2000

        self._build_q_table()

    def _build_q_table(self) :
        self.q_table = pd.DataFrame(
            np.zeros((1, len(self.actions))), #Initial q_table values
            columns = self.actions #Action's names
        )

    def _append_q_table(self, state) :
        self.q_table = self.q_table.append(
            pd.Series(
                [0]*len(self.actions),
                index=self.q_table.columns,
                name=state
            )
        )

    def choose_action(self, state) :
        state_actions = self.q_table.loc[state, :]
        if (np.random.uniform() > self.GREEDINESS) or (state_actions.all() == 0) : #Select a random action, either because this state has not been handled yet, or because of random chance based on greediness
            action_name = np.random.choice(self.actions)
        else :
            action_name = state_actions.argmax()
        return action_name

    def step(self, observation) :
        state = observation_to_state(observation)
        self.check_state_exists(state)
        self.steps += 1
        return self.choose_action(state)

    def check_state_exists(self, state) :
        if state not in self.q_table.index :
            self._append_q_table(state)

    #reward is the reward for reaching next_state
    def learn(self, cur_observation, cur_action, reward, next_observation) :
        cur_state = observation_to_state(cur_observation)
        next_state = observation_to_state(next_observation)
        self.check_state_exists(next_state) #Check if the next state exists. If not, append the next state to our q table

        q_predict = self.q_table.ix[cur_state, cur_action] #ix just indexes with integer position fallback
        if next_state != "terminal" :
            q_target = reward + self.REWARD_DECAY * self.q_table.ix[next_state, :].max()
            #With q_table.ix[next_state, :].max() we find the next possible actions and select the one with the highest reward
        else :
            q_target = reward #Next state is "terminal", which mean we have reached our target
        self.q_table.ix[cur_state, cur_action] += self.LEARNING_RATE * (q_target - q_predict) #Update our current q table.

        # print("Weights have been adjusted!")

    def save(self, filename) :
        self.q_table.to_csv(path_or_buf = filename)
