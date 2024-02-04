import PropTypes from 'prop-types';
import ArrowPathIcon from '@heroicons/react/24/solid/ArrowPathIcon';
import ArrowRightIcon from '@heroicons/react/24/solid/ArrowRightIcon';
import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Divider,
  SvgIcon
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Chart } from 'src/components/chart';

const useChartOptions = () => {
  const theme = useTheme();

  // Define a color for each sleep stage
  const stageColors = {
    deep: '#3f51b5',
    light: '#2196f3',
    rem: '#f50057',
    awake: '#ffeb3b'
  };

  return {
    chart: {
      background: 'transparent',
      stacked: true,
      toolbar: {
        show: false
      }
    },
    colors: Object.values(stageColors), // Use the colors for the stages
    plotOptions: {
      bar: {
        horizontal: false,
      }
    },
    fill: {
      opacity: 1,
      type: 'solid'
    },
    grid: {
      borderColor: theme.palette.divider,
      strokeDashArray: 2,
      xaxis: {
        lines: {
          show: false
        }
      },
      yaxis: {
        lines: {
          show: true
        }
      }
    },
    legend: {
      show: false
    },
    plotOptions: {
      bar: {
        columnWidth: '40px'
      }
    },
    stroke: {
      colors: ['transparent'],
      show: true,
      width: 2
    },
    theme: {
      mode: theme.palette.mode
    },
    xaxis: {
      axisBorder: {
        color: theme.palette.divider,
        show: true
      },
      axisTicks: {
        color: theme.palette.divider,
        show: true
      },
      categories: [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'
      ],
      labels: {
        offsetY: 5,
        style: {
          colors: theme.palette.text.secondary
        }
      }
    },
    yaxis: {
      labels: {
        formatter: (value) => (value > 0 ? `${value}H` : `${value}`),
        offsetX: -10,
        style: {
          colors: theme.palette.text.secondary
        }
      }
    }
  };
};

export const OverviewSales = ({ sleepStages, sx }) => {
  const chartOptions = useChartOptions();

  const chartSeries = [
    {
      name: 'Deep',
      data: sleepStages.deep
    },
    {
      name: 'Light',
      data: sleepStages.light
    },
    {
      name: 'REM',
      data: sleepStages.rem
    },
    {
      name: 'Awake',
      data: sleepStages.awake
    }
  ];

  return (
    <Card sx={sx}>
      <CardHeader
        action={(
          <Button
            color="inherit"
            size="small"
            startIcon={(
              <SvgIcon fontSize="small">
                <ArrowPathIcon />
              </SvgIcon>
            )}
          >
            Sync
          </Button>
        )}
        title="Sleep Stages"
      />
      <CardContent>
        <Chart
          height={350}
          options={chartOptions}
          series={chartSeries}
          type="bar"
          width="100%"
        />
      </CardContent>
      <Divider />
      <CardActions sx={{ justifyContent: 'flex-end' }}>
        <Button
          color="inherit"
          endIcon={(
            <SvgIcon fontSize="small">
              <ArrowRightIcon />
            </SvgIcon>
          )}
          size="small"
        >
          Overview
        </Button>
      </CardActions>
    </Card>
  );
};


OverviewSales.propTypes = {
  sleepStages: PropTypes.shape({
    deep: PropTypes.arrayOf(PropTypes.number).isRequired,
    light: PropTypes.arrayOf(PropTypes.number).isRequired,
    rem: PropTypes.arrayOf(PropTypes.number).isRequired,
    awake: PropTypes.arrayOf(PropTypes.number).isRequired
  }).isRequired,
  sx: PropTypes.object
};