import copy
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
        self.scale_displacement = 0.01 * (upper_bound - lower_bound) # scale of the random displacement of the sensors
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
            
            if action not in range(self.n_sensors + 1):
                raise ValueError("Invalid action!")
            
            if i >= self.n_sensors:
                continue  # Skip if the number of actions is greater than the number of sensors

            if self.remaining_energy[i] <= 0 or self.number_of_packets[i] == 0:
                continue  # Skip if sensor has no energy left or no packets to transmit
            
            if (action == i):
                continue  # Skip if sensor tries to transmit data to itself

            neighbors_i = self.eligible_receivers(i)
            keys_neighbors_i = list(neighbors_i.keys())
            if len(neighbors_i) == 0:
                continue
            if action not in keys_neighbors_i:
                continue

            remaining_energy_before = copy.deepcopy(self.remaining_energy)
            self.number_of_packets[i] = 0 # Reset the number of packets of the sensor i
            if action == self.n_sensors:
                rewards[i] = self.compute_individual_rewards(i, action, neighbors_i, remaining_energy_before)
                dones[i] = True
                # Calculate the energy consumption and remaining for transmitting data to the base station
                self.update_sensor_energies(i, neighbors_i[action]['transmission_energy'])                
            else:
                self.update_sensor_energies(i, neighbors_i[action]['transmission_energy'])  
                self.update_sensor_energies(action, neighbors_i[action]['reception_energy'])              
                # Update the number of packets of the sensor action
                self.number_of_packets[action] += self.number_of_packets[i]
                
                self.distance_to_base[action] = np.linalg.norm(self.sensor_positions[action] - base_station_position)
                
                # Compute individual rewards
                rewards[i] = self.compute_individual_rewards(i, action, neighbors_i, remaining_energy_before)

            # Calculate final reward
            # rewards_individual = torch.tensor(rewards[i], dtype=torch.double)                
            # final_reward = net(rewards_individual)
            final_reward = sum(rewards[i])
            rewards[i] = final_reward

        for i in range(self.n_sensors):
            if (self.remaining_energy[i] <= 0) or (self.number_of_packets[i] <= 0):
                dones[i] = True

        # Integrate the mobility of the sensors
        self.integrate_mobility() 

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
    
    def update_sensor_energies(self, i, delta_energy):
        self.consumption_energy[i] += delta_energy
        self.remaining_energy[i] -= delta_energy

    def transmission_energy(self, i, distance):
        # energy consumption for transmitting data on a distance        
        return self.number_of_packets[i] * info_amount * (Eelec + Eamp * distance**2)
    
    def reception_energy(self, i):
        # energy consumption for receiving data
        return self.number_of_packets[i] * info_amount * Eelec
    
    def compute_angle_vectors(self, i, action):
        '''
        Compute the angle in radians between the vectors formed by (i, action) and (i, base station)
        '''
        if action == self.n_sensors:
            return 0
        else:
            vector_to_next_hop = self.sensor_positions[action] - self.sensor_positions[i]
            vector_to_base = base_station_position - self.sensor_positions[i]
            cosine_angle = np.dot(vector_to_next_hop, vector_to_base) / (np.linalg.norm(vector_to_next_hop) * np.linalg.norm(vector_to_base))
            
            return np.arccos(np.clip(cosine_angle, -1, 1))

    def compute_reward_angle(self, i, action, neighbors_i):
        '''
        Compute the reward based on the angle between the vectors formed by (i, action) and (i, base station)
        '''
        if len(neighbors_i) == 1:
            return 1
        else:
            # Calculate the angle in radians between the vectors formed by (i, action) and (i, base station)
            angle = self.compute_angle_vectors(i, action)
            # Normalize the angle
            total_angles_without_direction = np.sum([abs(self.compute_angle_vectors(i, x)) for x in neighbors_i])
            normalized_angle = abs(angle) / total_angles_without_direction

            return 1 - normalized_angle
    
    def compute_reward_distance(self, action, neighbors_i):
        '''
        Compute the reward based on the distance to the next hop
        '''
        if len(neighbors_i) == 1:
            return 1
        else:
            total_distances = np.sum([neighbors_i[x]['distance'] for x in neighbors_i]) 
            # Normalize the distance to the next hop
            normalized_distance_to_next_hop = neighbors_i[action]['distance'] / total_distances

            return 1 - normalized_distance_to_next_hop

    def compute_reward_consumption_energy(self, action, neighbor_i):
        '''
        Compute the reward based on the total energy consumption (transmission, reception)
        '''
        if len(neighbor_i) == 1:
            return 1
        else:
            # Calculate the total energy consumption (transmission, reception)
            total_energy = neighbor_i[action]['transmission_energy'] + neighbor_i[action]['reception_energy']

            # Normalize the total energy consumption
            total_transmission_energies = np.sum([neighbor_i[x]['transmission_energy'] for x in neighbor_i])
            total_reception_energies = np.sum([neighbor_i[x]['reception_energy'] for x in neighbor_i])
            total_energies = total_transmission_energies + total_reception_energies
            normalized_total_energy = total_energy / total_energies

            return 1 - normalized_total_energy
    
    def compute_dispersion_remaining_energy(self, i, action, neighbor_i, remaining_energy_before):
        '''
        Compute the variation of sensors remaining energy after transmission and reception
        '''
        temporary_remaining_energy = copy.deepcopy(remaining_energy_before)
        temporary_remaining_energy[i] -= neighbor_i[action]['transmission_energy']
        if action != self.n_sensors:
            temporary_remaining_energy[action] -= neighbor_i[action]['reception_energy']
        dispersion_remaining_energy = np.std(temporary_remaining_energy)

        return dispersion_remaining_energy

    def compute_reward_dispersion_remaining_energy(self, i, action, neighbor_i, remaining_energy_before):
        '''
        Compute the reward based on the standard deviation of the remaining energy
        '''
        if len(neighbor_i) == 1:
            return 1
        else:
            dispersion_remaining_energy = self.compute_dispersion_remaining_energy(i, action, neighbor_i, remaining_energy_before)
            # Normalize the standard deviation of the remaining energy
            total_dispersion_remaining_energy = np.sum([self.compute_dispersion_remaining_energy(i, x, neighbor_i, remaining_energy_before) for x in neighbor_i])
            normalized_dispersion_remaining_energy = dispersion_remaining_energy / total_dispersion_remaining_energy

            return 1 - normalized_dispersion_remaining_energy
    
    def compute_individual_rewards(self, i, action, neighbors_i, remaining_energy_before):
        '''
        Compute the individual rewards
        '''
        reward_angle = self.compute_reward_angle(i, action, neighbors_i)
        reward_distance = self.compute_reward_distance(action, neighbors_i)
        reward_consumption_energy = self.compute_reward_consumption_energy(action, neighbors_i)
        reward_dispersion_remaining_energy = self.compute_reward_dispersion_remaining_energy(i, action, neighbors_i, remaining_energy_before)

        return [reward_angle, reward_distance, reward_consumption_energy, reward_dispersion_remaining_energy]
    
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

    def eligible_receivers(self, i):
        '''
        Get the list of eligible receivers for the current sensor
        '''
        eligible_receivers = {}
        # eligibility for sensors apart the base station
        for j in range(self.n_sensors):
            if i != j:
                distance = np.linalg.norm(self.sensor_positions[i] - self.sensor_positions[j])
                transmission_energy = self.transmission_energy(i, distance)
                reception_energy = self.reception_energy(j)
                condition_i = (self.remaining_energy[i] >= transmission_energy) and (distance <= self.coverage_radius)
                condition_j = (self.remaining_energy[j] >= reception_energy) and (distance <= self.coverage_radius)
                if condition_i and condition_j:
                    eligible_receivers[j] = {
                        'distance': distance,
                        'transmission_energy': transmission_energy,
                        'reception_energy': reception_energy
                    }
        
        # eligibility for the base station
        distance = np.linalg.norm(self.sensor_positions[i] - base_station_position)
        transmission_energy = self.transmission_energy(i, distance)
        condition_i = (self.remaining_energy[i] >= transmission_energy) and (distance <= self.coverage_radius)
        if condition_i:
            eligible_receivers[self.n_sensors] = {
                'distance': distance,
                'transmission_energy': transmission_energy,
                'reception_energy': 0
            }

        return eligible_receivers
