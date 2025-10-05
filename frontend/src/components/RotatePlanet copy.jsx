export function RotatePlanet(planet, points, rendere, camera, controls, prevIdxRef, i){
    const duration = 2000; // Durée de la transition en ms
    const start = performance.now();

    function animate(now) {
        if(planet?.position === points[points.length -1]) {
            prevIdxRef.current = i;
            return;
        }; // stop if at last point  
        const elapsed = now - start;
        const t = Math.min(1, elapsed / duration);
        points?.map((elm) => planet.position.set(elm.r[0], elm.r[1], elm.r[2]));
        controls.update();
        rendere.render(planet, camera);
        if (t < 1) {
            requestAnimationFrame(animate);
        }
    }
    requestAnimationFrame(animate);
}