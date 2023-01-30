import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { getDays } from "../Utils";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export function BallkidParamsChart({ offset, improvement }) {
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Ballkid Parameters",
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Time (days)",
        },
      },
      y: {
        title: {
          display: true,
          text: "Calibrated Rating (stars)",
        },
      },
    },
  };

  const days = getDays();
  const labels = days.map((day) => day.toDateString());

  const data = {
    labels,
    datasets: [
      {
        label: "Ballkid",
        data: days.map((day, index) => improvement * index + offset),
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  };

  return <Line options={options} data={data} />;
}
