import PropTypes from 'prop-types';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents'; // High morale
import SentimentSatisfiedIcon from '@mui/icons-material/SentimentSatisfied'; // Average morale
import SentimentDissatisfiedIcon from '@mui/icons-material/SentimentDissatisfied'; // Low morale
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Stack,
  SvgIcon,
  Typography,
  useTheme
} from '@mui/material';
import { Chart } from 'src/components/chart';

const useChartOptions = (labels) => {
  const theme = useTheme();

  // Adjust the colors to be more appropriate for morale categories
  const colors = [
    theme.palette.success.main, // High morale
    theme.palette.info.main,    // Average morale
    theme.palette.error.main    // Low morale
  ];

  return {
    chart: {
      background: 'transparent'
    },
    colors: [
      theme.palette.primary.main,
      theme.palette.success.main,
      theme.palette.warning.main
    ],
    dataLabels: {
      enabled: false
    },
    labels,
    legend: {
      show: false
    },
    plotOptions: {
      pie: {
        expandOnClick: false
      }
    },
    states: {
      active: {
        filter: {
          type: 'none'
        }
      },
      hover: {
        filter: {
          type: 'none'
        }
      }
    },
    stroke: {
      width: 0
    },
    theme: {
      mode: theme.palette.mode
    },
    tooltip: {
      fillSeriesColor: false
    }
  };
};

const iconMap = {
  'High Morale': (
    <SvgIcon color="success">
      <EmojiEventsIcon />
    </SvgIcon>
  ),
  'Average Morale': (
    <SvgIcon color="info">
      <SentimentSatisfiedIcon />
    </SvgIcon>
  ),
  'Low Morale': (
    <SvgIcon color="error">
      <SentimentDissatisfiedIcon />
    </SvgIcon>
  )
};

export const OverviewTraffic = (props) => {
  const { chartSeries, labels, sx } = props;
  const chartOptions = useChartOptions(labels);

  return (
    <Card sx={sx}>
      <CardHeader title="Soldier Morale" />
      <CardContent>
        <Chart
          height={300}
          options={chartOptions}
          series={chartSeries}
          type="donut"
          width="100%"
        />
        <Stack
          alignItems="center"
          direction="row"
          justifyContent="center"
          spacing={2}
          sx={{ mt: 2 }}
        >
          {labels.map((label, index) => {
            const value = chartSeries[index];

            return (
              <Box
                key={label}
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center'
                }}
              >
                {iconMap[label]}
                <Typography
                  sx={{ my: 1 }}
                  variant="h6"
                >
                  {label}
                </Typography>
                <Typography
                  color="text.secondary"
                  variant="subtitle2"
                >
                  {value}% 
                </Typography>
              </Box>
            );
          })}
        </Stack>
      </CardContent>
    </Card>
  );
};

OverviewTraffic.propTypes = {
  chartSeries: PropTypes.arrayOf(PropTypes.number).isRequired,
  labels: PropTypes.arrayOf(PropTypes.string).isRequired,
  sx: PropTypes.object
};
