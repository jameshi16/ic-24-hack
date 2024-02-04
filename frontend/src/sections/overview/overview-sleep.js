// Import necessary libraries and components
import React from 'react';
import PropTypes from 'prop-types';
import { Card, CardContent, CardHeader, useTheme } from '@mui/material';
import { Chart } from 'src/components/chart'; // Assuming this is an ApexCharts wrapper

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
            width: 2
        },
        colors: [theme.palette.primary.main],
        xaxis: {
            type: 'category',
            categories: Array.from({ length: 24 }, (_, i) => `${i}:00`),
            tickPlacement: 'on'
        },
        yaxis: {
            labels: {
                formatter: (value) => `${value} lvl`,
            }
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
const SleepLevelChart = ({ data, sx }) => {
    const chartOptions = useSleepChartOptions();

    return (
        <Card sx={sx}>
            <CardHeader title="Sleep Level Over 24 Hours" />
            <CardContent>
                <Chart
                    options={chartOptions}
                    series={[{ name: 'Sleep Level', data }]}
                    type="line"
                    height={350}
                />
            </CardContent>
        </Card>
    );
};

// Prop types for validation
SleepLevelChart.propTypes = {
    data: PropTypes.arrayOf(PropTypes.number).isRequired,
    sx: PropTypes.object
};

export default SleepLevelChart;
