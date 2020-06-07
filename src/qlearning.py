#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:43:47 2020

@author: camerongordon
"""

from pomdp_simulator import Simulator
import numpy as np 
import random


class QLearning(Simulator): 
    def __init__(self, file,discount_rate = 0.9, learning_rate = 0.01): 
        super().__init__(file) 
        
        self.eps = 1 # set epsilon exploration parameter 
        
        self.discount_rate = discount_rate 
        self.learning_rate = learning_rate 
        
        self.initialise_q_matrix()
        
    def initialise_q_matrix(self): # observation x action pairs 
        # note - should actually be on beliefs??
        # may otherwise go tabular on history?
        
        self.q_matrix = np.zeros([len(self.observation_names),len(self.action_name)])
        
    def greedy_action(self,obs): 
        index = self.get_index(obs)
        return np.argmax(self.q_matrix[index])
    
    def get_action(self, obs): 
        #print('QLearner','get_action')
        action_greedy = self.greedy_action(obs)
        #print('{{{(}}}',action_greedy)
        #print(self.action_name)
        
        #action_random = self.action_name.index(np.random.choice(self.action_name)) 
        
        action_name = list(self.actions.keys())[0] 
        action_taken = random.choice(self.actions[action_name])
        action_random = self.actions[action_name].index(action_taken)
        #print('{{{{}}}}}',action_random)
        
        
        return action_random if np.random.rand() < self.eps else action_greedy 
    
    def train(self, experience): 

        previous_observation, action, observation, reward, done = experience 
        #print(observation)
        debug = False 
        if debug: 
        
            print('QLearner','train')
            print('previous_observation', type(previous_observation), previous_observation)
            print('action', type(action), action) 
            print('observation', type(observation), observation) 
            print('reward', type(reward), reward)
            
        if type(observation) != int: 
            
            
            print('Issue - not int')
        
        ob_value = self.q_matrix[observation]
        ob_value =  np.zeros([len(self.action_name)]) if done else ob_value 
        ob_target = reward + self.discount_rate * np.max(ob_value) 
        
        value_update = ob_target - self.q_matrix[previous_observation,action] 
        
        self.q_matrix[previous_observation,action] += self.learning_rate * value_update
        
        if done: 
            self.eps = self.eps * 0.98 
            print(self.eps)