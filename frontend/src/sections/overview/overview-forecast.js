// Import necessary libraries and components
import React from 'react';
import PropTypes from 'prop-types';
import { Card, CardContent, CardHeader, useTheme } from '@mui/material';
import { Chart } from 'src/components/chart'; // Assuming this is an ApexCharts wrapper

const realData = [0.0, 6.3, 7.6, 10.0, 10.0, 8.5, 9.2];
const forecastedData = [...realData, 8.6, 8.2, 7.4, 6.7];

// Define a hook for the chart options specific to the sleep level line chart
const useSleepChartOptions = () => {
  const theme = useTheme();

  return {
    chart: {
      background: 'transparent',
      toolbar: {
        show: false
      },
      type: 'line'
    },

    stroke: {
      curve: 'smooth',
      width: 3,
      dashArray: [0, 1],
    },
    colors: [theme.palette.primary.main, 'red'],
    xaxis: {
      categories: [], // Empty categories array
      labels: {
        show: false // Hide labels
      },
      axisTicks: {
        show: false // Hide axis ticks
      },
      axisBorder: {
        show: false // Hide the axis border
      }
    },
    yaxis: {

    },
    tooltip: {
      x: {
        format: 'HH:mm'
      }
    },
    grid: {
      borderColor: theme.palette.divider
    },
    legend: {
      show: true
    }
  };
};

// Define the component for the sleep level graph
const Forecast = ({ sx }) => {
  const chartOptions = useSleepChartOptions();

  return (
    <Card sx={sx}>
      <CardHeader title="Forecasted Well-being" />
      <CardContent>
        <Chart
          options={chartOptions}
          series={[{ name: 'Actual', data: realData },
          { name: 'Forecasted', data: forecastedData }]}
          type="line"
          height={350}
        />
      </CardContent>
    </Card>
  );
};

// Prop types for validation
Forecast.propTypes = {
  data: PropTypes.arrayOf(PropTypes.number).isRequired,
  sx: PropTypes.object
};

export default Forecast;
