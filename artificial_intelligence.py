from globals import *

#Variables
N_STATES = 6
ACTIONS = []

#Hyper factors
GREEDINESS = 0.9 #Greediness factor. how much randomness is introduced in the action selection. In fancy math version of update algorithm, this is Epsilon.
LEARNING_RATE = 0.1 #Learning rate. In fancy math version of update algorithm, this is Alpha.
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

#Construct a q table
'''
def build_q_table(states, actions) :
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))), #Initial q_table values
        columns = actions, #Action's names
    )
    return table
'''

#this looks at the rewards for each possible action for the selected state
#if in state 1, action 1 gives a reward of 0.5, but action 2 gives a reward of 0.8, then it will select action 2
'''
def choose_action(state, q_table) :
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > GREEDINESS) or (state_actions.all() == 0) : #act non-greedy or state-act???
        action_name = np.random.choice(ACTIONS)
'''

#Based on the current state and action, determine the next state and reward. See episode 3?
'''
def get_env_feedback(state, action) :
    return
'''

#Comment here contains "code" very similar to the tutorial code, but with small changes and comments so I can understand it better
'''
def learn(self, cur_state, cur_action, reward, next_state) :
    check_state_exists(next_state) #Check if the next state exists. If not, append the next state to our q table

    q_predict = q_table.ix[cur_state, cur_action] #ix just indexes with integer position fallback
    if next_state != "terminal" :
        q_target = r + REWARD_DECAY * q_table.ix[next_state, :].max()
        #With q_table.ix[next_state, :].max() we find the next possible actions and select the one with the highest reward
    else :
        q_target = r #Next state is "terminal"
    q_table.ix[cur_state, cur_action] += LEARNING_RATE * (q_target - q_predict) #Update our current q table.
'''
class RL_Brain() :
    def __init__(self, actions) :
        self.actions = actions

    def _build_q_table(self) :
        self.table = pd.DataFrame(
            np.zeros((self.n_states, len(self.actions))), #Initial q_table values
            columns = self.actions, #Action's names
        )

    def choose_action(self, state) :
        state_actions = q_table.iloc[state, :]
        if (np.random.uniform() > self.greediness) or (state_actions.all() == 0) : #Select a random action, either because this state has not been handled yet, or because of random chance based on greediness
            action_name = np.random.choice(actions)
        else :
            action_name = state_actions.argmax()
        return action_name

    def step(self, observation) :
        pass
