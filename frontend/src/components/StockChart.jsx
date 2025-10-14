import React, { useEffect, useRef } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

function StockChart({ data }) {
  const chartRef = useRef(null);

  // Detect if it's an Indian stock (NSE or BSE)
  const isIndianStock = data.symbol && (data.symbol.includes('.NS') || data.symbol.includes('.BO'));
  const currencySymbol = isIndianStock ? '₹' : '$';

  // Combine historical and prediction data
  const allDates = [...data.historical.dates, data.prediction.date];
  const allPrices = [...data.historical.prices, data.prediction.price];
  
  // Create prediction line (only last 2 points)
  const predictionLine = new Array(data.historical.prices.length - 1).fill(null);
  predictionLine.push(data.historical.prices[data.historical.prices.length - 1]);
  predictionLine.push(data.prediction.price);

  const chartData = {
    labels: allDates,
    datasets: [
      {
        label: 'Historical Price',
        data: data.historical.prices,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 2,
        pointRadius: 1,
        pointHoverRadius: 5,
        tension: 0.1,
        fill: true,
      },
      {
        label: 'Forecast',
        data: predictionLine,
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        borderWidth: 3,
        borderDash: [10, 5],
        pointRadius: 4,
        pointHoverRadius: 7,
        pointBackgroundColor: 'rgb(34, 197, 94)',
        tension: 0.1,
      }
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 15,
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleFont: {
          size: 14,
        },
        bodyFont: {
          size: 13,
        },
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += currencySymbol + context.parsed.y.toFixed(2);
            }
            return label;
          }
        }
      },
    },
    scales: {
      x: {
        display: true,
        grid: {
          display: false,
        },
        ticks: {
          maxTicksLimit: 10,
          font: {
            size: 11,
          },
        },
      },
      y: {
        display: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
        ticks: {
          callback: function(value) {
            return currencySymbol + value.toFixed(2);
          },
          font: {
            size: 11,
          },
        },
      },
    },
  };

  return (
    <div className="w-full" style={{ height: '400px' }}>
      <Line ref={chartRef} data={chartData} options={options} />
    </div>
  );
}

export default StockChart;
