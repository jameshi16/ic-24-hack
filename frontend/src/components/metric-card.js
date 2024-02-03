// Sleep, Alertness, Physical
import { Chart } from 'src/components/chart';
import { Typography } from '@mui/material';
import { Box } from '@mui/material';

export const MetricCard = ({ event, close, _data }) => {
  const data = {
    options: {
      chart: {
        id: "basic-bar"
      },
      xaxis: {
        categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
      }
    },
    series: [
      {
        name: "series-1",
        data: [30, 40, 45, 50, 49, 60, 70, 91]
      }
    ]
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4">
        Data
      </Typography>
      <Chart
        options={data.options}
        series={data.series}
        type="line"
        width="500"
      />
    </Box>
  );
};
