import gym
import numpy as np
from gym.spaces import Discrete, Box, Tuple, Dict
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F

# Define the network parameters for the final reward function
input_dim = 4  # number of individual rewards
output_dim = 1  # final reward


stats_file_path_base = 'C:\\Users\\djime\\Documents\\PHD\\THESIS\\CODES\\RL_Routing\\Results_EPyMARL\\stats_over_time'
Eelec = 50e-9  # energy consumption per bit in joules
Eamp = 100e-12  # energy consumption per bit per square meter in joules
info_amount = 3072  # data size in bits
initial_energy = 1  # initial energy of each sensor (in joules)
lower_bound = 0  # lower bound of the sensor positions
upper_bound = 100  # upper bound of the sensor positions
base_station_position = np.array([(upper_bound - lower_bound)/2, (upper_bound - lower_bound)/2]) # position of the base station



# Define the final reward function using an attention mechanism
class Attention(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(Attention, self).__init__()  # Call the initializer of the parent class (nn.Module)
        self.input_dim = input_dim  # Set the input dimension of the network
        self.output_dim = output_dim  # Set the output dimension of the network
        self.linear1 = nn.Linear(input_dim, 64)  # Define the first linear layer. It takes input of size 'input_dim' and outputs size '64'
        self.linear2 = nn.Linear(64, output_dim)  # Define the second linear layer. It takes input of size '64' and outputs size 'output_dim'

    def forward(self, x):
        x = F.relu(self.linear1(x))  # Pass the input through a linear layer and a ReLU activation function
        attention_weights = F.softmax(x, dim=0)  # Apply the softmax function to get the attention weights
        x = attention_weights * x  # Multiply the input by the attention weights
        x = self.linear2(x)  # Pass the result through another linear layer
        return x

# Calculate the reward
net = Attention(input_dim, output_dim)
net = net.double()  # Convert the weights to Double


class WSNRoutingEnv(gym.Env):
    def __init__(self, n_sensors=10, coverage_radius=50):

        time_id = str(datetime.timestamp(datetime.now()))
        self.stats_file_path = stats_file_path_base + '_' + time_id + '.csv' # Set the file path

        # Initialize the CSV file with headers
        with open(self.stats_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Episode_count', 'Std remaining energy',  
                             'Total energy consumption of WSN', 'The number of sensors without energy'])

        self.n_sensors = n_sensors
        self.n_agents = n_sensors
        self.coverage_radius = coverage_radius
        self.episode_count = 0
        self.scale_displacement = 1 # scale of the random displacement of the sensors
        self.epsilon = 1e-10 # small value to avoid division by zero

        self.observation_space = Tuple(tuple([self._get_observation_space()] * self.n_agents))
        self.action_space = Tuple(tuple([Discrete(self.n_sensors + 1)] * self.n_agents))
                
        self.reset()

    def reset(self):

        if self.episode_count > 0:
            # Append the stats to the CSV file
            with open(self.stats_file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([self.episode_count, self.remaining_energy.std(), self.consumption_energy.sum(), 
                                (self.remaining_energy <= 0).sum()])

        self.sensor_positions = np.random.rand(self.n_sensors, 2) * upper_bound
        self.distance_to_base = np.linalg.norm(self.sensor_positions - base_station_position, axis=1)
        # Initialize remaining energy of each sensor to initial_energy joule
        self.remaining_energy = np.ones(self.n_sensors) * initial_energy
        self.consumption_energy = np.zeros(self.n_sensors)
        self.number_of_packets = np.ones(self.n_sensors)  # Number of packets to transmit
        self.episode_count += 1
    
        return self._get_observation()

    def step(self, actions):
        rewards = [0] * self.n_sensors
        dones = [False] * self.n_sensors

        for i, action in enumerate(actions):
            if i >= self.n_sensors:
                continue  # Skip if the number of actions is greater than the number of sensors

            if self.remaining_energy[i] <= 0 or self.number_of_packets[i] == 0:
                continue  # Skip if sensor has no energy left or no packets to transmit

            if action not in range(self.n_sensors + 1):
                raise ValueError("Invalid action!")
            
            if (action == i):
                continue  # Skip if sensor tries to transmit data to itself

            self.distance_to_base[i] = np.linalg.norm(self.sensor_positions[i] - base_station_position)
            transmission_energy_to_base = self.number_of_packets[i] * info_amount * (Eelec + Eamp * self.distance_to_base[i]**2) # energy consumption for transmitting data to the base station
            if action == self.n_sensors and (self.remaining_energy[i] < transmission_energy_to_base or self.distance_to_base[i] > self.coverage_radius):
                continue
            elif action == self.n_sensors:
                rewards[i] = 1.0
                dones[i] = True
                # Calculate the energy consumption for transmitting data to the next hop
                self.consumption_energy[i] += transmission_energy_to_base
                self.remaining_energy[i] -= transmission_energy_to_base
                self.number_of_packets[i] = 0
            else:
                distance_to_action = np.linalg.norm(self.sensor_positions[i] - self.sensor_positions[action])
                transmission_energy_to_action = self.number_of_packets[i] * info_amount * (Eelec + Eamp * distance_to_action**2) # energy consumption for transmitting data to the next hop
                reception_energy =self.number_of_packets[i] * info_amount * Eelec  # energy consumption for receiving data
                if (self.remaining_energy[action] < reception_energy) or (distance_to_action > self.coverage_radius) or (self.remaining_energy[i] < transmission_energy_to_action):
                    continue
                else:
                    distances_to_sensors = np.linalg.norm(self.sensor_positions - self.sensor_positions[i], axis=1)
                    # is_within_coverage = (distances_to_sensors <= self.coverage_radius) & (distances_to_sensors > 0) # exclude i itself
                    # is_within_coverage = (distances_to_sensors <= self.coverage_radius)
                    is_within_coverage = (distances_to_sensors >= 0)
                    variation_remaining_energy_within_coverage_before_action = self.remaining_energy[is_within_coverage].std()
                    total_consumption_energy_within_coverage_before_action = self.consumption_energy[is_within_coverage].sum()
                    # Calculate the energy consumption for transmitting, receiving data to the next hop
                    self.consumption_energy[i] += transmission_energy_to_action
                    self.consumption_energy[action] += reception_energy
                    # Update the remaining energy of the sensors
                    self.remaining_energy[i] -= transmission_energy_to_action
                    self.remaining_energy[action] -= reception_energy
                    # Update the number of packets of the sensors
                    self.number_of_packets[i] = 0
                    self.number_of_packets[action] += self.number_of_packets[i]
                    
                    self.distance_to_base[action] = np.linalg.norm(self.sensor_positions[action] - base_station_position)

                    # Calculate the angle between the current sensor, the next hop, and the base station
                    vector_to_next_hop = self.sensor_positions[action] - self.sensor_positions[i]
                    vector_to_base = base_station_position - self.sensor_positions[i]
                    cosine_angle = np.dot(vector_to_next_hop, vector_to_base) / (np.linalg.norm(vector_to_next_hop) * np.linalg.norm(vector_to_base))
                    angle = np.arccos(np.clip(cosine_angle, -1, 1))  # in radians

                    # Calculate the energy parameters for the final reward function                
                    remaining_energy_within_coverage = self.remaining_energy[is_within_coverage]
                    contrib_action_balance_energy = (self.remaining_energy[action] - remaining_energy_within_coverage.mean())**2
                    balance_energy = ((self.remaining_energy - remaining_energy_within_coverage.mean())**2).sum()
                    consumption_energy_within_coverage = self.consumption_energy[is_within_coverage]
                    variation_remaining_energy_within_coverage_after_action = remaining_energy_within_coverage.std()
                    total_consumption_energy_within_coverage_after_action = self.consumption_energy[is_within_coverage].sum()

                    # Calculate individual rewards
                    reward_angle = 1 - (np.abs(angle) / np.pi)
                    reward_distance = 1 - (distance_to_action / self.coverage_radius)
                    reward_remaining_energy = 1 - contrib_action_balance_energy/(balance_energy + self.epsilon)
                    reward_consumption_energy = 1 - self.consumption_energy[action]/(consumption_energy_within_coverage.sum() + self.epsilon)
                    # if variation_remaining_energy_within_coverage_before_action < variation_remaining_energy_within_coverage_after_action:
                    #     reward_remaining_energy = 0
                    # else:
                    #     reward_remaining_energy = 1
                    # if total_consumption_energy_within_coverage_before_action < total_consumption_energy_within_coverage_after_action:
                    #     reward_consumption_energy = 0
                    # else:
                    #     reward_consumption_energy = 1                            
                    rewards_individual = torch.tensor([reward_angle, reward_distance, reward_remaining_energy, reward_consumption_energy], dtype=torch.double)

                    # Calculate final reward
                    #final_reward = net(rewards_individual)
                    final_reward = reward_angle + reward_distance + reward_remaining_energy + reward_consumption_energy
                    done = (self.remaining_energy[i] <= 0) or (self.number_of_packets[i] == 0) or (self.remaining_energy[action] <= 0) or (self.number_of_packets[action] == 0)
                    rewards[i] = final_reward
                    dones[i] = done

            # Add a small random displacement to each sensor's position
            displacement = np.random.normal(scale=self.scale_displacement, size=2)
            self.sensor_positions[i] += displacement

            # Cancel the displacement if the sensor goes out of bounds
            if not(np.all(self.sensor_positions[i] >= lower_bound) and np.all(self.sensor_positions[i] <= upper_bound)):
                self.sensor_positions[i] -= displacement

        return self._get_observation(), rewards, dones, {}

    def _get_observation(self):
        return [{'remaining_energy': e, 
                 'sensor_positions': p,
                 'number_of_packets': d} for e, p, d in zip(self.remaining_energy, self.sensor_positions, self.number_of_packets)]
    
    def _get_observation_space(self):
        return Dict({
            'remaining_energy': Box(low=0, high=initial_energy, shape=(1,), dtype=np.float64),
            'sensor_positions': Box(low=lower_bound, high=upper_bound, shape=(2,), dtype=np.float64),
            'number_of_packets': Box(low=0, high=np.inf, shape=(1,))
        })