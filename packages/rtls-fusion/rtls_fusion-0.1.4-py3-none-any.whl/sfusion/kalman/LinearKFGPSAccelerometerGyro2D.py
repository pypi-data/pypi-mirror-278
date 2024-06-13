# sfusion/kalman/LinearKFGPSAccelerometerGyro2D.py

import numpy as np
import math

class LinearKFGPSAccelerometerGyro2D:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise):
        """
        Initialize the Linear Kalman Filter for 2D GPS with accelerometer and gyroscope input.

        :param initial_state: Initial state vector [x_position, y_position, x_velocity, y_velocity, orientation].
        :param initial_covariance: Initial covariance matrix.
        :param process_noise: Process noise covariance matrix.
        :param measurement_noise: Measurement noise covariance matrix.
        """
        self.state = np.array(initial_state)  # State vector [x_position, y_position, x_velocity, y_velocity, orientation]
        self.covariance = np.array(initial_covariance)  # Covariance matrix
        self.process_noise = np.array(process_noise)  # Process noise covariance matrix
        self.measurement_noise = np.array(measurement_noise)  # Measurement noise covariance matrix

    def predict(self, dt, control_input):
        """
        Predict the next state and covariance.
        
        :param dt: Time step.
        :param control_input: Control input (acceleration and angular velocity) [x_acceleration, y_acceleration, angular_velocity].
        """
        # State transition matrix
        F = np.array([[1, 0, dt, 0, 0],
                      [0, 1, 0, dt, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 1]])

        # Control input matrix
        B = np.array([[0.5 * dt**2, 0, 0],
                      [0, 0.5 * dt**2, 0],
                      [dt, 0, 0],
                      [0, dt, 0],
                      [0, 0, dt]])

        # Predicted state
        self.state = F @ self.state + B @ np.array(control_input)

        # Predicted covariance
        self.covariance = F @ self.covariance @ F.T + self.process_noise

    def update(self, measurement):
        """
        Update the state and covariance with the new measurement.
        
        :param measurement: New measurement for [x_position, y_position].
        """

        # Measurement matrix
        H = np.array([[1, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0]])

        # Measurement residual
        Z = np.array(measurement)
        y = Z - H @ self.state

        # Residual covariance
        S = H @ self.covariance @ H.T + self.measurement_noise

        # Kalman gain
        K = self.covariance @ H.T @ np.linalg.inv(S)

        # Updated state
        self.state = self.state + K @ y

        # Updated covariance
        self.covariance = (np.eye(5) - K @ H) @ self.covariance
