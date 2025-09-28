# Python 3D Asteroid Orbit Visualizer

This Python implementation recreates NASA's R-based elliptical orbit simulator using modern Python libraries and provides web export capabilities for Three.js integration.

## How to Use the Python Logic for 3D Views

### 1. Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the usage guide
python usage_guide.py
```

### 2. Basic Usage - Step by Step

#### Step 1: Import the Classes
```python
from orbital_mechanics import OrbitalMechanics, OrbitVisualizer, WebExporter
import numpy as np

# Initialize
om = OrbitalMechanics()
visualizer = OrbitVisualizer(om)
```

#### Step 2: Define Orbital Parameters
```python
# Orbital elements
a = 2.5          # Semi-major axis (AU)
e = 0.4          # Eccentricity (0=circle, <1=ellipse)
inclination = np.radians(15)  # Inclination in radians
omega = np.radians(45)        # Longitude of ascending node
raan = np.radians(30)         # Right ascension of ascending node
```

#### Step 3: Create 3D Visualization
```python
# Generate and plot 3D orbit
fig, ax = visualizer.plot_orbit_3d(a, e, inclination, omega, raan)
plt.show()
```

### 3. Advanced Features

#### Multiple Asteroid System
```python
# Define multiple asteroids
asteroids = {
    "Ceres": {"a": 2.77, "e": 0.079, "i": 10.6},
    "Vesta": {"a": 2.36, "e": 0.089, "i": 7.1},
    "Pallas": {"a": 2.77, "e": 0.231, "i": 34.8}
}

# Plot all orbits in one 3D view
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

for name, params in asteroids.items():
    # Convert degrees to radians
    inclination = np.radians(params["i"])
    
    # Generate orbit
    x_2d, y_2d, z_2d = om.generate_ellipse_2d(params["a"], params["e"])
    x_3d, y_3d, z_3d = om.apply_keplerian_rotations(
        x_2d, y_2d, z_2d, inclination, 0, 0
    )
    
    # Plot
    ax.plot(x_3d, y_3d, z_3d, linewidth=2, label=name)

plt.show()
```

#### Animated Orbit
```python
# Create animated orbit showing object movement
fig, anim = visualizer.animate_orbit(
    a=2.0, e=0.3, T=100.0,  # T = orbital period
    inclination=np.radians(20),
    num_frames=60, duration=10.0
)
plt.show()
```

#### Export for Web (Three.js)
```python
# Export orbit data for web visualization
exporter = WebExporter(om)

orbit_data = exporter.export_orbit_json(
    a=2.5, e=0.4, 
    inclination=np.radians(15),
    omega=np.radians(45),
    raan=np.radians(30)
)

# Save to JSON file
import json
with open('asteroid_orbit.json', 'w') as f:
    json.dump(orbit_data, f, indent=2)
```

### 4. Key Mathematical Concepts

#### Keplerian Orbital Elements
- **Semi-major axis (a)**: Size of the orbit
- **Eccentricity (e)**: Shape of the orbit (0=circle, <1=ellipse)
- **Inclination (i)**: Tilt of orbital plane
- **Longitude of ascending node (ω)**: Orientation in orbital plane
- **Right ascension of ascending node (Ω)**: Orientation of orbital plane

#### 3D Transformations
The system applies three sequential rotations to transform a 2D ellipse into a 3D orbit:

1. **Inclination** (Y-axis rotation): Tilts the orbital plane
2. **Longitude of ascending node** (Z-axis rotation): Rotates within the plane
3. **RAAN** (X-axis rotation): Final orientation adjustment

#### Kepler Equation Solver
For orbital propagation (object position over time):
```
E - e*sin(E) = M(t)
```
Where:
- E = Eccentric anomaly
- e = Eccentricity  
- M(t) = Mean anomaly at time t

### 5. File Structure

```
orbital_viewer/
├── orbital_mechanics.py    # Core orbital mechanics classes
├── usage_guide.py         # Step-by-step examples
├── web_visualizer.html    # Three.js web interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### 6. Web Integration

The system exports JSON data that can be used directly in Three.js:

```javascript
// Load the exported JSON data
fetch('asteroid_orbit.json')
  .then(response => response.json())
  .then(data => {
    // Create Three.js orbit visualization
    const coordinates = data.orbit_path.coordinates;
    // ... Three.js code to render the orbit
  });
```

### 7. Real Asteroid Data Integration

To use real asteroid data from NASA APIs:

```python
# Example: Connect to NASA JPL Small-Body Database
import requests

def get_asteroid_elements(asteroid_name):
    # NASA JPL API call (simplified)
    url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={asteroid_name}"
    response = requests.get(url)
    data = response.json()
    
    # Extract orbital elements from response
    # ... parse API response
    
    return {
        'a': semi_major_axis,
        'e': eccentricity,
        'i': inclination
        # ... other elements
    }

# Use real data
ceres_elements = get_asteroid_elements('Ceres')
fig, ax = visualizer.plot_orbit_3d(**ceres_elements)
```

### 8. Performance Tips

- Use fewer points (50-100) for interactive visualization
- Use more points (200-500) for high-quality static plots
- For web export, 200 points provide good balance of quality and file size
- Cache orbital calculations for repeated visualizations

### 9. Extending the System

The modular design allows easy extension:

- Add planetary perturbations
- Include asteroid physical properties
- Implement n-body simulations
- Add collision detection
- Create VR/AR visualizations

## Files Generated

Running the examples will create:
- `asteroids_web_data.json`: Three.js-ready orbit data
- Various matplotlib 3D plots and animations

## Next Steps

1. Run `python usage_guide.py` to see all examples
2. Open `web_visualizer.html` in a browser for interactive 3D view
3. Integrate with NASA APIs for real asteroid data
4. Customize for your specific visualization needs