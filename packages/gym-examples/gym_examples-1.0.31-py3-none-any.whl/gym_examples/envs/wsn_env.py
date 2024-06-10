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

        super(WSNRoutingEnv, self).__init__()

        self.n_sensors = n_sensors
        self.n_agents = n_sensors
        self.coverage_radius = coverage_radius
        self.episode_count = 0
        self.scale_displacement = 1 # scale of the random displacement of the sensors
        self.epsilon = 1e-10 # small value to avoid division by zero

        # Define observation space
        self.observation_space = Tuple(
            tuple([self._get_observation_space() for _ in range(self.n_sensors)])
        )
        self.action_space = Tuple(tuple([Discrete(self.n_sensors + 1)] * self.n_agents))
                
        self.reset()

    def reset(self):

        # Initialize the position of the sensors randomly
        self.sensor_positions = np.random.rand(self.n_sensors, 2) * upper_bound
        self.distance_to_base = np.linalg.norm(self.sensor_positions - base_station_position, axis=1)
        # Initialize remaining energy of each sensor to initial_energy joule
        self.remaining_energy = np.ones(self.n_sensors) * initial_energy
        self.consumption_energy = np.zeros(self.n_sensors)
        self.number_of_packets = np.ones(self.n_sensors)  # Number of packets to transmit
        self.episode_count += 1
    
        return self._get_obs()

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
            transmission_energy_to_base = self.transmission_energy(i, self.distance_to_base[i])
            can_transmit_to_base = (self.remaining_energy[i] >= transmission_energy_to_base) and (self.distance_to_base[i] <= self.coverage_radius)
            if action == self.n_sensors and not can_transmit_to_base:
                continue
            elif action == self.n_sensors:
                rewards[i] = self.compute_individual_rewards(i, self.n_sensors, self.distance_to_base[i], transmission_energy_to_base, 0)
                dones[i] = True
                # Calculate the energy consumption and remaining for transmitting data to the base station
                self.update_sensor_energies(i, transmission_energy_to_base, transmission_energy_to_base)
                self.number_of_packets[i] = 0 # Reset the number of packets of the sensor
            else:
                distance_to_action = np.linalg.norm(self.sensor_positions[i] - self.sensor_positions[action])
                transmission_energy_to_action = self.transmission_energy(i, distance_to_action)
                reception_energy = self.reception_energy(i)
                can_transmit_to_action = (self.remaining_energy[i] >= transmission_energy_to_action) and (distance_to_action <= self.coverage_radius)
                can_receive_from_sensor = self.remaining_energy[action] >= reception_energy
                if not (can_transmit_to_action and can_receive_from_sensor):
                    continue
                else:
                    # Calculate the energy consumption for transmitting, receiving data to the next hop
                    self.consumption_energy[i] += transmission_energy_to_action
                    self.consumption_energy[action] += reception_energy
                    # Update the remaining energy of the sensors
                    self.remaining_energy[i] -= transmission_energy_to_action
                    self.remaining_energy[action] -= reception_energy
                    # Update the number of packets of the sensors
                    self.number_of_packets[i] = 0
                    self.number_of_packets[action] += self.number_of_packets[i]

                    # Compute individual rewards
                    rewards[i] = self.compute_individual_rewards(i, action, distance_to_action, transmission_energy_to_action, reception_energy)

                    self.distance_to_base[action] = np.linalg.norm(self.sensor_positions[action] - base_station_position)

        for i in range(self.n_sensors):
            if (self.remaining_energy[i] <= 0) or (self.number_of_packets[i] <= 0):
                dones[i] = True

            # Calculate the reward based on the variance of the remaining energy
            reward_variation_remaining_energy = self.compute_reward_variation_remaining_energy()
            # Append the reward based on the variance of the remaining energy
            if rewards[i] == 0:
                rewards[i] = [0, 0, 0]                  
            rewards[i].append(reward_variation_remaining_energy)
            # Calculate final reward
            # rewards_individual = torch.tensor(rewards[i], dtype=torch.double)                
            # final_reward = net(rewards_individual)
            final_reward = sum(rewards[i])
            rewards[i] = final_reward

        # Integrate the mobility of the sensors
        #self.integrate_mobility() 

        return self._get_obs(), rewards, dones, {}

    def _get_obs(self):
        return [{'remaining_energy': np.array([e]), 
                 'sensor_positions': p,
                 'consumption_energy': np.array([c]),
                 'number_of_packets': np.array([d])} for e, p, c, d in zip(self.remaining_energy, self.sensor_positions, self.consumption_energy, self.number_of_packets)]

    def _get_observation_space(self):
        return Dict({
            'remaining_energy': Box(low=0, high=initial_energy, shape=(1,), dtype=np.float64),
            'sensor_positions': Box(low=lower_bound, high=upper_bound, shape=(2,), dtype=np.float64),
            'consumption_energy': Box(low=0, high=initial_energy, shape=(1,), dtype=np.float64),
            'number_of_packets': Box(low=0, high=np.inf, shape=(1,))
        })

    def get_state(self):
        return self._get_obs()
    
    def get_avail_actions(self):
        return [list(range(self.n_sensors + 1)) for _ in range(self.n_sensors)]
    
    def update_sensor_energies(self, i, delta_consumption, delta_remaining):
        self.consumption_energy[i] += delta_consumption
        self.remaining_energy[i] -= delta_remaining

    def transmission_energy(self, i, distance):
        # energy consumption for transmitting data on a distance
        return self.number_of_packets[i] * info_amount * (Eelec + Eamp * distance**2)
    
    def reception_energy(self, i):
        # energy consumption for receiving data
        return self.number_of_packets[i] * info_amount * Eelec
    
    def compute_reward_angle(self, i, action):
        '''
        Compute the reward based on the angle between the current sensor, the next hop, and the base station
        '''
        if action == self.n_sensors:
            angle = 0
        else:
            # Calculate the angle between the current sensor, the next hop, and the base station
            vector_to_next_hop = self.sensor_positions[action] - self.sensor_positions[i]
            vector_to_base = base_station_position - self.sensor_positions[i]
            cosine_angle = np.dot(vector_to_next_hop, vector_to_base) / (np.linalg.norm(vector_to_next_hop) * np.linalg.norm(vector_to_base))
            angle = np.arccos(np.clip(cosine_angle, -1, 1))  # in radians

        return 1 - (np.abs(angle) / np.pi)
    
    def compute_reward_consumption_energy(self, i, delta_transmission_energy, delta_reception_energy):
        '''
        Compute the reward based on the energy consumption for transmitting, receiving data to the next hop
        '''
        # Calculate the energy consumption for transmitting, receiving data to the next hop
        total_energy = delta_transmission_energy + delta_reception_energy

        # Normalize the total energy consumption
        total_energy_max = self.transmission_energy(i, self.coverage_radius) + delta_reception_energy
        normalized_total_energy = total_energy / total_energy_max

        return 1 - normalized_total_energy
    
    def compute_reward_variation_remaining_energy(self):
        '''
        Compute the reward based on the variance of the remaining energy
        '''
        variation_remaining_energy = np.std(self.remaining_energy)
        max_variation_remaining_energy = initial_energy / 2  # maximum std of the remaining energy
        normalized_variation_remaining_energy = variation_remaining_energy / max_variation_remaining_energy

        return 1 - normalized_variation_remaining_energy
    
    def integrate_mobility(self):
        '''
        Integrate the mobility of the sensors after each step
        '''
        # Add a small random displacement to each sensor's position
        displacement = np.random.normal(scale=self.scale_displacement, size=(self.n_sensors, 2))
        self.sensor_positions += displacement
        # Cancel the displacement if the sensor goes out of bounds
        for i in range(self.n_sensors):
            if not(np.all(self.sensor_positions[i] >= lower_bound) and np.all(self.sensor_positions[i] <= upper_bound)):
                self.sensor_positions[i] -= displacement[i]

    def compute_individual_rewards(self, i, action, distance_to_next_hop, transmission_energy_to_next_hop, reception_energy):
        '''
        Compute the individual rewards
        '''
        reward_angle = self.compute_reward_angle(i, action)
        reward_distance = 1 - (distance_to_next_hop / self.coverage_radius)
        reward_consumption_energy = self.compute_reward_consumption_energy(i, transmission_energy_to_next_hop, reception_energy)
        return [reward_angle, reward_distance, reward_consumption_energy]

