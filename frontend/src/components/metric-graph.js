import { Chart } from 'src/components/chart';
import { Typography } from '@mui/material';
import { Box } from '@mui/material';

export const MetricGraph = ({ times, tensor }) => {
  const data = {
    options: {
      chart: {
        id: "basic-bar"
      },
      xaxis: {
        categories: times,
        tickAmount: 12
      }
    },
    series: [
      ...tensor.map((vector, idx) => ({
        name: `series-${idx}`,
        data: vector
      }))
    ]
  };

  return (
    <Box sx={{ p: 2 }}>
      <Chart
        options={data.options}
        series={data.series}
        type="line"
        width="400"
      />
    </Box>
  );
};
