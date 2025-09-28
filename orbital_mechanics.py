"""
Python Elliptical Orbit Simulator
Based on NASA's R implementation for mission visualization
Implements Keplerian orbital mechanics and 3D transformations
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
from typing import Tuple, List, Dict, Any


class OrbitalMechanics:
    """
    Core orbital mechanics calculations for elliptical orbits
    Implements the same methodology as NASA's R-based simulator
    """
    
    def __init__(self):
        self.tolerance = 1.0e-14  # Convergence tolerance for Kepler solver
        
    def generate_ellipse_2d(self, a: float, e: float, num_points: int = 80) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate a 2D ellipse in the orbital plane
        
        Args:
            a: semi-major axis
            e: eccentricity (0 = circle, approaching 1 = line)
            num_points: number of points to generate
            
        Returns:
            Tuple of (x, y, z) coordinate arrays
        """
        # Calculate orbital parameters
        b = a * np.sqrt(1 - e**2)  # semi-minor axis
        c = e * a  # distance from center to focus
        
        # Generate parametric angle sequence
        u = np.linspace(-np.pi, np.pi, num_points)
        
        # Generate ellipse coordinates (focus at origin)
        x = a * np.cos(u) - c
        y = b * np.sin(u)
        z = np.zeros(num_points)
        
        return x, y, z
    
    def rotation_matrix_x(self, angle: float) -> np.ndarray:
        """Rotation matrix around X-axis (Roll/RAAN)"""
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([
            [1, 0, 0],
            [0, cos_a, -sin_a],
            [0, sin_a, cos_a]
        ])
    
    def rotation_matrix_y(self, angle: float) -> np.ndarray:
        """Rotation matrix around Y-axis (Pitch/Inclination)"""
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([
            [cos_a, 0, sin_a],
            [0, 1, 0],
            [-sin_a, 0, cos_a]
        ])
    
    def rotation_matrix_z(self, angle: float) -> np.ndarray:
        """Rotation matrix around Z-axis (Yaw/Longitude of ascending node)"""
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ])
    
    def apply_keplerian_rotations(self, x: np.ndarray, y: np.ndarray, z: np.ndarray,
                                inclination: float, omega: float, raan: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Apply Keplerian orbital element rotations to transform 2D ellipse to 3D orbit
        
        Args:
            x, y, z: 2D ellipse coordinates
            inclination: orbital inclination (pitch)
            omega: longitude of ascending node (yaw)  
            raan: right ascension of ascending node (roll)
            
        Returns:
            Transformed 3D coordinates
        """
        # Stack coordinates for matrix operations
        coords = np.vstack([x, y, z])
        
        # Apply rotations in sequence: inclination -> omega -> RAAN
        # 1. Pitch (inclination) - rotation around Y axis
        coords = self.rotation_matrix_y(inclination) @ coords
        
        # 2. Yaw (omega) - rotation around Z axis  
        coords = self.rotation_matrix_z(omega) @ coords
        
        # 3. Roll (RAAN) - rotation around X axis
        coords = self.rotation_matrix_x(raan) @ coords
        
        return coords[0], coords[1], coords[2]
    
    def kepler_start3(self, e: float, M: float) -> float:
        """
        Marc Murison's initial guess for Kepler equation solver
        Uses Taylor series expansion to third order
        """
        t34 = e**2
        t35 = e * t34
        t33 = np.cos(M)
        
        result = M + (-0.5*t35 + e + (t34 + 1.5 * t33*t35)*t33) * np.sin(M)
        return result
    
    def eps3(self, e: float, M: float, x: float) -> float:
        """
        Third-order correction term for Kepler equation solver
        """
        t1 = np.cos(x)
        t2 = -1 + e * t1
        t3 = np.sin(x)
        t4 = e * t3
        t5 = -x + t4 + M
        t6 = t5 / (0.5 * t5 * t4/t2 + t2)
        result = t5 / ((0.5 * t3 - t1 * t6/6) * e * t6 + t2)
        return result
    
    def solve_kepler_equation(self, e: float, M: float) -> float:
        """
        Solve Kepler's equation: E - e*sin(E) = M
        Uses Marc Murison's iterative method with Taylor series
        
        Args:
            e: eccentricity
            M: mean anomaly
            
        Returns:
            E: eccentric anomaly
        """
        # Normalize mean anomaly to [0, 2π]
        M_norm = M % (2 * np.pi)
        
        # Initial guess
        E0 = self.kepler_start3(e, M_norm)
        dE = self.tolerance + 1
        count = 0
        
        # Iterative solution
        while dE > self.tolerance and count < 100:
            E = E0 - self.eps3(e, M_norm, E0)
            dE = abs(E - E0)
            E0 = E
            count += 1
            
        if count >= 100:
            print("Warning: Kepler equation solver failed to converge!")
            
        return E0
    
    def propagate_orbit(self, t: float, a: float, e: float, T: float, 
                       inclination: float, omega: float, raan: float, 
                       tau: float = 0) -> Tuple[float, float, float]:
        """
        Calculate orbital position at time t using Keplerian propagation
        
        Args:
            t: time
            a: semi-major axis
            e: eccentricity
            T: orbital period
            inclination: orbital inclination
            omega: longitude of ascending node
            raan: right ascension of ascending node
            tau: time of periapsis passage
            
        Returns:
            3D position coordinates (x, y, z)
        """
        # Mean motion
        n = 2 * np.pi / T
        
        # Mean anomaly
        M = n * (t - tau)
        
        # Solve for eccentric anomaly
        E = self.solve_kepler_equation(e, M)
        
        cos_E = np.cos(E)
        
        # Calculate distance and position in orbital plane
        r = a * (1 - e * cos_E)
        
        # Position in orbital plane
        x_orb = r * ((cos_E - e) / (1 - e * cos_E))
        y_orb = r * ((np.sqrt(1 - e**2) * np.sin(E)) / (1 - e * cos_E))
        z_orb = 0
        
        # Apply Keplerian rotations
        x_3d, y_3d, z_3d = self.apply_keplerian_rotations(
            np.array([x_orb]), np.array([y_orb]), np.array([z_orb]),
            inclination, omega, raan
        )
        
        return float(x_3d[0]), float(y_3d[0]), float(z_3d[0])


class OrbitVisualizer:
    """
    3D orbit visualization using matplotlib
    """
    
    def __init__(self, orbital_mechanics: OrbitalMechanics):
        self.om = orbital_mechanics
        
    def plot_orbit_3d(self, a: float, e: float, inclination: float = 0, 
                     omega: float = 0, raan: float = 0, num_points: int = 80):
        """
        Create interactive 3D plot of orbital path
        """
        # Generate 2D ellipse
        x_2d, y_2d, z_2d = self.om.generate_ellipse_2d(a, e, num_points)
        
        # Transform to 3D orbit
        x_3d, y_3d, z_3d = self.om.apply_keplerian_rotations(
            x_2d, y_2d, z_2d, inclination, omega, raan
        )
        
        # Create 3D plot
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot orbit
        ax.plot(x_3d, y_3d, z_3d, 'r-', linewidth=2, label='Orbit')
        
        # Add central body (Sun)
        ax.scatter([0], [0], [0], c='yellow', s=200, marker='o', label='Sun')
        
        # Add focus point
        c = e * a
        focus_x, focus_y, focus_z = self.om.apply_keplerian_rotations(
            np.array([-c]), np.array([0]), np.array([0]),
            inclination, omega, raan
        )
        ax.scatter(focus_x, focus_y, focus_z, c='red', s=50, marker='o', label='Focus')
        
        # Set equal aspect ratio
        max_range = np.array([x_3d.max()-x_3d.min(), 
                             y_3d.max()-y_3d.min(),
                             z_3d.max()-z_3d.min()]).max() / 2.0
        mid_x = (x_3d.max()+x_3d.min()) * 0.5
        mid_y = (y_3d.max()+y_3d.min()) * 0.5
        mid_z = (z_3d.max()+z_3d.min()) * 0.5
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'3D Elliptical Orbit (a={a}, e={e:.3f})')
        ax.legend()
        
        plt.tight_layout()
        return fig, ax
    
    def animate_orbit(self, a: float, e: float, T: float, 
                     inclination: float = 0, omega: float = 0, raan: float = 0,
                     num_frames: int = 100, duration: float = 10.0):
        """
        Create animated orbit with propagating object
        """
        from matplotlib.animation import FuncAnimation
        
        # Generate orbit path
        x_2d, y_2d, z_2d = self.om.generate_ellipse_2d(a, e, 200)
        x_orbit, y_orbit, z_orbit = self.om.apply_keplerian_rotations(
            x_2d, y_2d, z_2d, inclination, omega, raan
        )
        
        # Create figure
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot static elements
        ax.plot(x_orbit, y_orbit, z_orbit, 'k-', alpha=0.3, linewidth=1, label='Orbit')
        ax.scatter([0], [0], [0], c='yellow', s=200, marker='o', label='Sun')
        
        # Animated object
        object_point, = ax.plot([], [], [], 'ro', markersize=8, label='Object')
        
        # Calculate time steps
        time_steps = np.linspace(0, T, num_frames)
        
        def animate(frame):
            t = time_steps[frame]
            x, y, z = self.om.propagate_orbit(t, a, e, T, inclination, omega, raan)
            object_point.set_data([x], [y])
            object_point.set_3d_properties([z])
            ax.set_title(f'Orbit Animation (t={t:.1f}s)')
            return object_point,
        
        # Set plot limits
        max_range = max(x_orbit.max() - x_orbit.min(),
                       y_orbit.max() - y_orbit.min(),
                       z_orbit.max() - z_orbit.min()) / 2.0
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_zlim(-max_range, max_range)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y') 
        ax.set_zlabel('Z')
        ax.legend()
        
        # Create animation
        anim = FuncAnimation(fig, animate, frames=num_frames, 
                           interval=duration*1000/num_frames, blit=False, repeat=True)
        
        return fig, anim


class WebExporter:
    """
    Export orbital data for Three.js web visualization
    """
    
    def __init__(self, orbital_mechanics: OrbitalMechanics):
        self.om = orbital_mechanics
    
    def export_orbit_json(self, a: float, e: float, inclination: float = 0,
                         omega: float = 0, raan: float = 0, num_points: int = 200) -> Dict[str, Any]:
        """
        Export orbit data as JSON for Three.js consumption
        """
        # Generate orbit coordinates
        x_2d, y_2d, z_2d = self.om.generate_ellipse_2d(a, e, num_points)
        x_3d, y_3d, z_3d = self.om.apply_keplerian_rotations(
            x_2d, y_2d, z_2d, inclination, omega, raan
        )
        
        # Create orbit data structure
        orbit_data = {
            "orbital_elements": {
                "semi_major_axis": float(a),
                "eccentricity": float(e),
                "inclination": float(inclination),
                "longitude_ascending_node": float(omega),
                "right_ascension_ascending_node": float(raan)
            },
            "orbit_path": {
                "coordinates": [
                    [float(x_3d[i]), float(y_3d[i]), float(z_3d[i])]
                    for i in range(len(x_3d))
                ]
            },
            "central_body": {
                "position": [0.0, 0.0, 0.0],
                "radius": 0.1
            }
        }
        
        return orbit_data
    
    def export_propagation_data(self, a: float, e: float, T: float,
                               inclination: float = 0, omega: float = 0, raan: float = 0,
                               num_steps: int = 100) -> Dict[str, Any]:
        """
        Export time-propagated orbital positions for animation
        """
        time_steps = np.linspace(0, T, num_steps)
        positions = []
        
        for t in time_steps:
            x, y, z = self.om.propagate_orbit(t, a, e, T, inclination, omega, raan)
            positions.append({
                "time": float(t),
                "position": [float(x), float(y), float(z)]
            })
        
        return {
            "orbital_elements": {
                "semi_major_axis": float(a),
                "eccentricity": float(e),
                "period": float(T),
                "inclination": float(inclination),
                "longitude_ascending_node": float(omega),
                "right_ascension_ascending_node": float(raan)
            },
            "propagation_data": positions
        }