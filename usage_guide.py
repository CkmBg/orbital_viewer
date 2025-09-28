"""
Example usage of Python Elliptical Orbit Simulator
Shows step-by-step how to create 3D orbital visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
from orbital_mechanics import OrbitalMechanics, OrbitVisualizer, WebExporter

def step_by_step_3d_orbit():
    """
    Step-by-step guide to creating 3D orbital visualizations
    """
    print("STEP-BY-STEP: Creating 3D Orbital Visualizations")
    print("=" * 60)
    
    # STEP 1: Initialize the orbital mechanics system
    print("\nSTEP 1: Initialize Classes")
    om = OrbitalMechanics()
    visualizer = OrbitVisualizer(om)
    print("✓ OrbitalMechanics and OrbitVisualizer initialized")
    
    # STEP 2: Define orbital parameters
    print("\nSTEP 2: Define Orbital Parameters")
    a = 2.5          # Semi-major axis (AU for asteroids)
    e = 0.4          # Eccentricity (0=circle, <1=ellipse)
    inclination = np.radians(15)  # Orbital inclination (15 degrees)
    omega = np.radians(45)        # Longitude of ascending node (45 degrees)
    raan = np.radians(30)         # Right ascension of ascending node (30 degrees)
    
    print(f"  Semi-major axis (a): {a} AU")
    print(f"  Eccentricity (e): {e}")
    print(f"  Inclination: {np.degrees(inclination):.1f}°")
    print(f"  Longitude of ascending node (ω): {np.degrees(omega):.1f}°")
    print(f"  Right ascension of ascending node (Ω): {np.degrees(raan):.1f}°")
    
    # STEP 3: Generate 2D ellipse in orbital plane
    print("\nSTEP 3: Generate 2D Ellipse")
    x_2d, y_2d, z_2d = om.generate_ellipse_2d(a, e, num_points=100)
    print(f"✓ Generated {len(x_2d)} points for 2D ellipse")
    
    # STEP 4: Apply 3D transformations
    print("\nSTEP 4: Apply Keplerian Rotations")
    x_3d, y_3d, z_3d = om.apply_keplerian_rotations(
        x_2d, y_2d, z_2d, inclination, omega, raan
    )
    print("✓ Applied inclination, longitude of ascending node, and RAAN rotations")
    
    # STEP 5: Create 3D visualization
    print("\nSTEP 5: Create 3D Visualization")
    fig, ax = visualizer.plot_orbit_3d(a, e, inclination, omega, raan)
    print("✓ 3D plot created and displayed")
    
    return fig, (x_3d, y_3d, z_3d)

def create_multiple_asteroid_orbits():
    """
    Create a solar system view with multiple asteroid orbits
    """
    print("\n" + "=" * 60)
    print("CREATING MULTIPLE ASTEROID ORBITS")
    print("=" * 60)
    
    om = OrbitalMechanics()
    
    # Define multiple asteroids with realistic parameters
    asteroids = {
        "Ceres": {"a": 2.77, "e": 0.079, "i": 10.6, "ω": 73.6, "Ω": 80.3, "color": "blue"},
        "Vesta": {"a": 2.36, "e": 0.089, "i": 7.1, "ω": 151.2, "Ω": 103.9, "color": "green"},
        "Pallas": {"a": 2.77, "e": 0.231, "i": 34.8, "ω": 310.0, "Ω": 173.1, "color": "red"},
        "Juno": {"a": 2.67, "e": 0.257, "i": 13.0, "ω": 248.1, "Ω": 169.9, "color": "orange"}
    }
    
    # Create figure
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    print("\nGenerating orbits for asteroids:")
    
    for name, params in asteroids.items():
        # Convert angles to radians
        inclination = np.radians(params["i"])
        omega = np.radians(params["ω"])
        raan = np.radians(params["Ω"])
        
        # Generate orbit
        x_2d, y_2d, z_2d = om.generate_ellipse_2d(params["a"], params["e"])
        x_3d, y_3d, z_3d = om.apply_keplerian_rotations(
            x_2d, y_2d, z_2d, inclination, omega, raan
        )
        
        # Plot orbit
        ax.plot(x_3d, y_3d, z_3d, color=params["color"], linewidth=2, 
                label=f'{name} (a={params["a"]:.2f} AU)')
        
        print(f"  ✓ {name}: a={params['a']:.2f} AU, e={params['e']:.3f}")
    
    # Add Sun at center
    ax.scatter([0], [0], [0], c='yellow', s=300, marker='o', 
               label='Sun', edgecolors='orange', linewidth=2)
    
    # Add planetary orbits for reference
    earth_orbit = np.linspace(0, 2*np.pi, 100)
    earth_x = np.cos(earth_orbit)
    earth_y = np.sin(earth_orbit)
    earth_z = np.zeros_like(earth_x)
    ax.plot(earth_x, earth_y, earth_z, 'b--', alpha=0.5, label='Earth orbit (1 AU)')
    
    mars_orbit = np.linspace(0, 2*np.pi, 100)
    mars_x = 1.52 * np.cos(mars_orbit)
    mars_y = 1.52 * np.sin(mars_orbit)
    mars_z = np.zeros_like(mars_x)
    ax.plot(mars_x, mars_y, mars_z, 'r--', alpha=0.5, label='Mars orbit (1.52 AU)')
    
    # Set equal aspect ratio and limits
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_zlim(-2, 2)
    
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.set_title('Main Belt Asteroids in 3D')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    print("\n✓ Multi-asteroid 3D visualization created")
    
    return fig, ax

def create_animated_orbit():
    """
    Create an animated orbit showing object movement over time
    """
    print("\n" + "=" * 60)
    print("CREATING ANIMATED ORBIT")
    print("=" * 60)
    
    om = OrbitalMechanics()
    visualizer = OrbitVisualizer(om)
    
    # Orbital parameters for animation
    a = 2.0
    e = 0.3
    T = 100.0  # Period in time units
    inclination = np.radians(20)
    omega = np.radians(60)
    raan = np.radians(45)
    
    print(f"Animating orbit with:")
    print(f"  Period: {T} time units")
    print(f"  Semi-major axis: {a} AU")
    print(f"  Eccentricity: {e}")
    
    # Create animation
    fig, anim = visualizer.animate_orbit(
        a=a, e=e, T=T, 
        inclination=inclination, omega=omega, raan=raan,
        num_frames=50, duration=10.0
    )
    
    print("✓ Animated orbit created")
    print("  - Shows object moving along elliptical path")
    print("  - Demonstrates Kepler's law of equal areas in equal time")
    
    return fig, anim

def export_for_web_visualization():
    """
    Export orbit data for Three.js web visualization
    """
    print("\n" + "=" * 60)
    print("EXPORTING FOR WEB VISUALIZATION")
    print("=" * 60)
    
    om = OrbitalMechanics()
    exporter = WebExporter(om)
    
    # Multiple asteroids for web export
    asteroids_for_web = {
        "asteroid_1": {"a": 2.2, "e": 0.15, "i": 5, "ω": 30, "Ω": 45},
        "asteroid_2": {"a": 2.8, "e": 0.25, "i": 12, "ω": 120, "Ω": 75},
        "asteroid_3": {"a": 1.8, "e": 0.35, "i": 8, "ω": 200, "Ω": 150}
    }
    
    web_data = {"asteroids": {}}
    
    for name, params in asteroids_for_web.items():
        # Convert to radians
        inclination = np.radians(params["i"])
        omega = np.radians(params["ω"])
        raan = np.radians(params["Ω"])
        
        # Export orbit data
        orbit_data = exporter.export_orbit_json(
            params["a"], params["e"], inclination, omega, raan
        )
        
        web_data["asteroids"][name] = orbit_data
        print(f"✓ Exported {name}: {len(orbit_data['orbit_path']['coordinates'])} points")
    
    # Save to JSON file
    import json
    with open('/home/mikymax/workspace/orbital_viewer/asteroids_web_data.json', 'w') as f:
        json.dump(web_data, f, indent=2)
    
    print(f"\n✓ Web data exported to asteroids_web_data.json")
    print("  - Ready for Three.js integration")
    print("  - Contains 3D coordinates for all asteroid orbits")
    
    return web_data

def demonstrate_kepler_propagation():
    """
    Demonstrate orbital position calculation at different times
    """
    print("\n" + "=" * 60)
    print("KEPLER EQUATION ORBITAL PROPAGATION")
    print("=" * 60)
    
    om = OrbitalMechanics()
    
    # Orbital parameters
    a = 2.5
    e = 0.4
    T = 120.0  # Orbital period
    inclination = np.radians(10)
    omega = np.radians(30)
    raan = np.radians(45)
    
    print(f"Computing orbital positions over time:")
    print(f"  Semi-major axis: {a} AU")
    print(f"  Eccentricity: {e}")
    print(f"  Period: {T} time units")
    
    # Calculate positions at different times
    times = [0, T/8, T/4, 3*T/8, T/2, 5*T/8, 3*T/4, 7*T/8]
    positions = []
    
    print(f"\nTime (fraction of period) -> Position (x, y, z)")
    print("-" * 50)
    
    for t in times:
        x, y, z = om.propagate_orbit(t, a, e, T, inclination, omega, raan)
        positions.append((x, y, z))
        fraction = t / T
        print(f"t = {fraction:.3f}T -> ({x:6.3f}, {y:6.3f}, {z:6.3f})")
    
    # Create visualization of positions over time
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot complete orbit
    x_2d, y_2d, z_2d = om.generate_ellipse_2d(a, e, 200)
    x_orbit, y_orbit, z_orbit = om.apply_keplerian_rotations(
        x_2d, y_2d, z_2d, inclination, omega, raan
    )
    ax.plot(x_orbit, y_orbit, z_orbit, 'k-', alpha=0.3, label='Orbit path')
    
    # Plot positions at different times
    pos_x, pos_y, pos_z = zip(*positions)
    ax.scatter(pos_x, pos_y, pos_z, c=range(len(positions)), 
               s=100, cmap='viridis', label='Time positions')
    
    # Add Sun
    ax.scatter([0], [0], [0], c='yellow', s=200, marker='o', label='Sun')
    
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.set_title('Orbital Positions Over Time')
    ax.legend()
    
    print("\n✓ Time-based position visualization created")
    
    return fig


if __name__ == "__main__":
    print("PYTHON 3D ORBITAL VISUALIZATION GUIDE")
    print("Based on NASA's elliptical orbit simulator")
    print("=" * 60)
    
    # Show matplotlib backend
    import matplotlib
    print(f"Using matplotlib backend: {matplotlib.get_backend()}")
    
    # Run demonstrations
    try:
        # Step-by-step orbit creation
        fig1, coords = step_by_step_3d_orbit()
        
        # Multiple asteroids
        fig2, ax2 = create_multiple_asteroid_orbits()
        
        # Animated orbit
        fig3, anim = create_animated_orbit()
        
        # Export for web
        web_data = export_for_web_visualization()
        
        # Kepler propagation
        fig4 = demonstrate_kepler_propagation()
        
        # Show all plots
        plt.show()
        
        print("\n" + "=" * 60)
        print("ALL VISUALIZATIONS COMPLETED!")
        print("=" * 60)
        print("Files generated:")
        print("  - asteroids_web_data.json (for Three.js)")
        print("\nNext steps:")
        print("  1. Use the JSON data in a Three.js web application")
        print("  2. Customize orbital parameters for your specific asteroids")
        print("  3. Add real asteroid data from NASA APIs")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure matplotlib is installed: pip install matplotlib")