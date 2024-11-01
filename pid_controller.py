# pid_controller.py

class PIDController:
    def __init__(self, kp, ki, kd, integral_limit=None):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0
        self.integral_limit = integral_limit  # Added integral limit

    def calculate(self, error, dt):
        # Proportional term
        proportional = self.kp * error
        
        # Integral term
        self.integral += error * dt
        if self.integral_limit is not None:
            self.integral = max(min(self.integral, self.integral_limit), -self.integral_limit)  # Clamping integral term
        integral = self.ki * self.integral
        
        # Derivative term
        derivative = self.kd * (error - self.previous_error) / dt
        self.previous_error = error
        
        # PID output
        return proportional + integral + derivative

def update_steering(right_lane_distance, left_lane_distance, pid_controller, dt):
    # Calculate error
    error = right_lane_distance - left_lane_distance
    
    # Compute steering adjustment using PID controller
    steering_adjustment = pid_controller.calculate(error, dt)
    
    # Return the computed steering adjustment for visualization or application
    return steering_adjustment
