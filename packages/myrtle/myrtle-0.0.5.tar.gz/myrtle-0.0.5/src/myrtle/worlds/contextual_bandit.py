import numpy as np
from myrtle.worlds.base_world import BaseWorld
from pacemaker.pacemaker import Pacemaker


class ContextualBandit(BaseWorld):
    """
    A multi-armed bandit, except that at each time step the order of the
    bandits is shuffled. The shuffled order is sensed.

    This world tests an agent's ability to use sensor information to determine
    which action to take.
    """

    def __init__(
        self,
        sensor_q=None,
        action_q=None,
        report_q=None,
        n_time_steps=1000,
        n_episodes=1,
        log_name=None,
        log_dir=".",
        logging_level="info",
    ):
        # Initialize constants
        self.n_sensors = 4
        self.n_actions = 4
        self.n_rewards = 4
        self.steps_per_second = 1000

        # Number of time steps to run in a single episode
        self.n_time_steps = n_time_steps
        self.n_episodes = n_episodes

        self.name = "Contextual bandit"

        # This gets incremented to 0 with the first reset(), before the run starts.
        self.i_episode = -1

        self.sensor_q = sensor_q
        self.action_q = action_q
        self.report_q = report_q

        self.pm = Pacemaker(self.steps_per_second)
        self.initialize_log(log_name, log_dir, logging_level)

        # The highest paying bandit is 2 with average payout of .4 * 280 = 112.
        # Others are 50 or less.
        self.bandit_payouts = [150, 200, 280, 320]
        self.bandit_hit_rates = [0.3, 0.25, 0.4, 0.15]

    def reset(self):
        # This block will probably be needed in the reset() of every world.
        ####
        self.i_step = 0
        if self.i_episode > 0:
            self.sensor_q.put({"truncated": True})
        ####

        self.bandit_order = np.arange(self.n_actions)
        self.sensors = self.bandit_order.copy()
        self.actions = np.zeros(self.n_actions)
        self.rewards = [0] * self.n_rewards

    def step(self):
        # print(
        #     f"step {self.i_step}, episode {self.i_episode}              ",
        #     end="\r",
        # )

        # Calculate the reward based on the shuffled order of the previous time step.
        self.rewards = [0] * self.n_actions
        for i in range(self.n_actions):
            if (
                np.random.sample()
                < self.bandit_hit_rates[self.bandit_order[i]]
            ):
                self.rewards[i] = (
                    self.actions[i] * self.bandit_payouts[self.bandit_order[i]]
                )

        # Shuffle and sense the order of the bandits.
        self.bandit_order = np.arange(self.n_actions)
        np.random.shuffle(self.bandit_order)
        self.sensors = self.bandit_order.copy()
