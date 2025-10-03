import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

export default function OrbitVisualizer({ trajectory }) {
  const mountRef = useRef(null);

  useEffect(() => {
    if (!trajectory || trajectory.length === 0 || !mountRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    const camera = new THREE.PerspectiveCamera(
      75,
      mountRef.current.clientWidth / mountRef.current.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 2, 5);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.physicallyCorrectLights = true;
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    mountRef.current.appendChild(renderer.domElement);

    // Add OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Smooth controls
    controls.dampingFactor = 0.05;

    // Orbit line
    const points = trajectory.map(p => new THREE.Vector3(p.x, p.y, p.z));
    const geometry = new THREE.BufferGeometry().setFromPoints(points);
    const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
    const orbitLine = new THREE.Line(geometry, material);
    scene.add(orbitLine);

    // Asteroid mesh
    const asteroid = new THREE.Mesh(
      new THREE.SphereGeometry(0.05, 16, 16),
      new THREE.MeshPhongMaterial({ color: 0xd3d3d3 })
    );
    scene.add(asteroid);

    // Sun mesh
    const sun = new THREE.Mesh(
      new THREE.SphereGeometry(0.1, 32, 32),
      new THREE.MeshBasicMaterial({ color: 0xffff00 })
    );
    scene.add(sun);

    // Light
    const light = new THREE.PointLight(0xffffff, 10, 100);
    light.position.set(2, 2, 2);
    scene.add(light);

    // Animate asteroid along trajectory
    let i = 0;
    const animate = () => {
      requestAnimationFrame(animate);
      asteroid.position.copy(points[i % points.length]);
      i++;
      controls.update(); // Update controls
      renderer.render(scene, camera);
    };
    animate();

    // Handle resize
    const handleResize = () => {
      if (!mountRef.current) return;
      camera.aspect = mountRef.current.clientWidth / mountRef.current.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    };
    window.addEventListener("resize", handleResize);

    // Cleanup on unmount
    return () => {
      window.removeEventListener("resize", handleResize);
      if (mountRef.current) {
        mountRef.current.removeChild(renderer.domElement);
      }
    };
  }, [trajectory]);

  return <div ref={mountRef} style={{ width: "100%", height: "100%", display: "flex", flex: 1 }} />;
}