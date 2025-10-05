import * as THREE from "three";
import { PLANETS_POINTS } from "../utils/constant";

export default function MoveToIndex({
  planets,
  indexTransition,
  prevIndexTransitionRef,
}) {
  console.log(
    indexTransition,
    "< - >",
    prevIndexTransitionRef.current,
    " | ",
    indexTransition == prevIndexTransitionRef.current
  );
  if (indexTransition != prevIndexTransitionRef.current ) {
    const planetsXYZ = PLANETS_POINTS?.bodies?.map((pp) =>
      pp?.samples
        ?.map((p) => new THREE.Vector3(p.r[0], p.r[1], p.r[2]))
        ?.slice(
          indexTransition < prevIndexTransitionRef.current
            ? indexTransition
            : prevIndexTransitionRef.current,
          indexTransition > prevIndexTransitionRef.current
            ? indexTransition + 1
            : prevIndexTransitionRef.current + 1
        )
    );

    planetsXYZ?.forEach((point, index) => {
      console.log({x : point[0].x, point, index, planets});
      planets[index].position.lerp(point[indexTransition], indexTransition);
    })

    console.log(
      planetsXYZ,
      indexTransition < prevIndexTransitionRef.current
        ? indexTransition
        : prevIndexTransitionRef.current,
      indexTransition > prevIndexTransitionRef.current
        ? indexTransition + 1
        : prevIndexTransitionRef.current + 1
    );

    console.log(
      indexTransition,
      "< - >",
      prevIndexTransitionRef.current,
      " | ",
      indexTransition == prevIndexTransitionRef.current
    );
    prevIndexTransitionRef.current = indexTransition;
  }
  
  return null;
}
