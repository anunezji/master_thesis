# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 18:41:59 2019

@author: iA
"""
from mesa.time import StagedActivation

class StagedActivation_random(StagedActivation):
    """ A scheduler which allows agent activation to be divided into several
    stages instead of a single `step` method. All agents execute one stage
    before moving on to the next.

    Agents must have all the stage methods implemented. Stage methods take a
    model object as their only argument.

    This schedule tracks steps and time separately. Time advances in fractional
    increments of 1 / (# of stages), meaning that 1 step = 1 unit of time.

    """
    def __init__(self, model, stage_list=None, shuffle=True,
                 shuffle_between_stages=True,seed = 1):
        """ Create an empty Staged Activation schedule.

        Args:
            model: Model object associated with the schedule.
            stage_list: List of strings of names of stages to run, in the
                         order to run them in.
            shuffle: If True, shuffle the order of agents each step.
            shuffle_between_stages: If True, shuffle the agents after each
                                    stage; otherwise, only shuffle at the start
                                    of each step.

        """
        super().__init__(model)
        self.stage_list = ["step"] if not stage_list else stage_list
        self.shuffle = shuffle
        self.shuffle_between_stages = shuffle_between_stages
        self.stage_time = 1 / len(self.stage_list)
        self.seed = seed
        print("Randomseed: ",self.seed)

    def step(self):
        """ Executes all the stages for all agents. """
        
        agent_keys = list(self._agents.keys())
        if self.shuffle:
            self.model.random.seed(self.seed)
            self.model.random.shuffle(agent_keys)
        for stage in self.stage_list:
            for agent_key in agent_keys:
                getattr(self._agents[agent_key], stage)()  # Run stage
            if self.shuffle_between_stages:
                #seed(2)
                #self.model.random.seed(self.seed)
                self.model.random.shuffle(agent_keys)
            self.time += self.stage_time

        self.steps += 1
