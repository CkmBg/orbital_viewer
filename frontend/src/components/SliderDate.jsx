import { useState } from "react";
import { PLANETS_POINTS } from "../utils/constant";

export default function DateSlider({ handleIndexTransition }) {
  // Dates de début et de fin
  const startDate = new Date("2025-11-03").getTime();
  const endDate = new Date("2055-11-03").getTime();

  // Valeur initiale
  const [dateValue, setDateValue] = useState(startDate);

  // Fonction pour formater la date en dd/mm/yyyy
  const formatDate = (ms) => {
    const d = new Date(ms);
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
  };

  // Handler du slider
  const handleChange = (e) => {
    setDateValue(parseInt(e.target.value));
  };

  return (
    <div style={{ padding: "20px", color: "#fff" }}>
      <label>
        Date: {formatDate(dateValue)}
        <input
          type="range"
          min={startDate}
          max={endDate}
          step={24 * 60 * 60 * 1000} // 1 jour en millisecondes
          value={dateValue}
          onChange={handleChange}
          style={{ width: "100%", marginTop: "10px" }}
          //   onDragEnd={() => console.log("Date sélectionnée :", new Date(dateValue).toISOString())}
          onTouchEnd={() => {
            handleIndexTransition(
              PLANETS_POINTS?.bodies[0]?.samples?.findIndex((elm) => {
                const d1 = new Date(elm.datetime_utc);
                const d2 = new Date(dateValue);

                return (
                  d1.getFullYear() === d2.getFullYear() &&
                  d1.getMonth() === d2.getMonth() &&
                  d1.getDate() === d2.getDate()
                );
              })
            );
            console.log(
              "Date sélectionnée :",
              new Date(dateValue).toISOString()
            );
            console.log(
              "Index - ",
              PLANETS_POINTS?.bodies[0]?.samples?.findIndex((elm) => {
                const d1 = new Date(elm.datetime_utc);
                const d2 = new Date(dateValue);

                return (
                  d1.getFullYear() === d2.getFullYear() &&
                  d1.getMonth() === d2.getMonth() &&
                  d1.getDate() === d2.getDate()
                );
              })
            );
          }}
        />
      </label>
    </div>
  );
}
