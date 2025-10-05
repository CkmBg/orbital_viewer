import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import IMPACT from "../../impact asteroides/impact-data.json";
import PLANETS_POINTS from "../../planets/Planet_heliocentric_position_velocity.json";

export default function OrbitVisualizer({ trajectory, transition, reset, indexTransition }) {
  const [prevIndexTransition, setPrevIndexTransition] = useState(indexTransition);
  const mountRef = useRef(null);
  const impactTimelinePoints = IMPACT.map((imp) =>
    imp?.timeline?.slice(0, 732)?.map((el) => el.heliocentric?.r_au)
  );
  const planetsPoints = PLANETS_POINTS?.bodies;
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

    camera.position.set(0, 0, 5);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.physicallyCorrectLights = true;
    renderer.setSize(
      mountRef.current.clientWidth,
      mountRef.current.clientHeight
    );
    mountRef.current.appendChild(renderer.domElement);

    // Add OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Smooth controls
    controls.dampingFactor = 0.05;

    // Orbit line
    const points = trajectory.map((p) => new THREE.Vector3(p.x, p.y, p.z));
    // const geometry = new THREE.BufferGeometry().setFromPoints(points);
    // const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
    // const orbitLine = new THREE.Line(geometry, material);
    // scene.add(orbitLine);
    console.log({ points });
    console.log({ planetsPoints });

    const planetsTJ = planetsPoints?.map((pp) =>
      pp?.samples?.map((p) => new THREE.Vector3(p.r[0], p.r[1], p.r[2]))
    );
    // const planetColors = [
    //   0x00ff88, // vert vif
    //   0x0088ff, // bleu clair et lumineux
    //   0xffee00, // jaune éclatant
    //   0xff6600, // orange vif
    //   0xcc00ff, // violet électrique
    //   0xff0099, // rose fuchsia
    //   0x00ffff, // cyan brillant
    //   0xff0000, // rouge pur
    // ]; // Example colors for planets
    const planetColors = [
      "#00FF88", // vert vif
      "#0088FF", // bleu clair et lumineux
      "#FFEE00", // jaune éclatant
      "#FF6600", // orange vif
      "#CC00FF", // violet électrique
      "#FF0099", // rose fuchsia
      "#00FFFF", // cyan brillant
      "#FF0000", // rouge pur
    ];
    planetsTJ?.forEach((planetPoints, index) => {
      console.log({ planetPoints });
      const planetGeometry = new THREE.BufferGeometry().setFromPoints(
        planetPoints
      );
      const planetMaterial = new THREE.LineBasicMaterial({
        color: planetColors[index % planetColors.length],
      });
      const planetLine = new THREE.Line(planetGeometry, planetMaterial);
      scene.add(planetLine);
    });

    planetsPoints?.map((elm, idx) => {
      const uiContainer = document.createElement("div");
      uiContainer.style.position = "absolute";
      uiContainer.style.top = `${10 * idx * 2.3}px`;
      uiContainer.style.right = `30px`;
      uiContainer.style.color = planetColors[idx % planetColors.length];
      document.body.appendChild(uiContainer);

      uiContainer.innerHTML = `
      <p>${elm.name} ${elm?.samples?.length}</p>
      `;
    });

    // Asteroid mesh
    const asteroid = new THREE.Mesh(
      new THREE.SphereGeometry(0.05, 16, 16),
      new THREE.MeshPhongMaterial({ color: 0xd3d3d3 })
    );
    scene.add(asteroid);

    const planets = planetsPoints?.map(
      (pp, idx) =>
        new THREE.Mesh(
          new THREE.SphereGeometry(0.05 * idx, 16, 16),
          new THREE.MeshPhongMaterial({
            color: planetColors[idx % planetColors.length],
          })
        )
    );
    planets?.forEach((planet, idx) => {
      scene.add(planet);
      planet?.position?.set(
        planetsTJ[idx][0].x,
        planetsTJ[idx][0].y,
        planetsTJ[idx][0].z
      );
    });

    // Sun mesh
    const sun = new THREE.Mesh(
      new THREE.SphereGeometry(0.1, 32, 32),
      new THREE.MeshBasicMaterial({ color: 0xffff00 })
    );
    scene.add(sun);

    // Light
    const light = new THREE.PointLight(0xffffff, 10000, 100);
    light.position.set(2, 2, 2);
    scene.add(light);

    // Animate asteroid along trajectory
    let i = 0;
    const animate = () => {
      requestAnimationFrame(animate);
      // asteroid.position.copy(points[i % points.length]);
      // i++;
      controls.update(); // Update controls
      renderer.render(scene, camera);
    };
    animate();

    

    // function moveToIndex(index) {
    //   if (indexTransition < prevIndexTransition) {
    //     console.log("Backward");
    //     let i = 0;
    //     planetsTJ[0]?.planetPoints?.
    //     planetsTJ?.forEach((planetPoints, index) => {
    //       planets[index].position.copy(planetPoints[i % points.length]);
    //       console.log({ planetPoints, index, indexTransition, prevIndexTransition });
          
    //     });
    //   }else{
    //     console.log("Forward");
    //   };

    // }
    // if(indexTransition != prevIndexTransition){
    //   moveToIndex(indexTransition);
    //   setPrevIndexTransition(indexTransition);
    // }

    // Handle resize
    const handleResize = () => {
      if (!mountRef.current) return;
      camera.aspect =
        mountRef.current.clientWidth / mountRef.current.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(
        mountRef.current.clientWidth,
        mountRef.current.clientHeight
      );
    };
    window.addEventListener("resize", handleResize);

    // Cleanup on unmount
    return () => {
      window.removeEventListener("resize", handleResize);
      if (mountRef.current) {
        mountRef.current.removeChild(renderer.domElement);
      }
    };
  }, [trajectory, reset, indexTransition]);

  return (
    <div
      ref={mountRef}
      style={{ width: "100%", height: "100%", display: "flex", flex: 1 }}
    />
  );
}
