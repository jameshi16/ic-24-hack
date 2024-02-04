import {
    Box,
    Card,
    CardContent,
    CardHeader,
    Stack, Typography
} from '@mui/material';
import { Chart } from 'src/components/chart';
import { useChartOptions, iconMap } from './overview-traffic';


export const OverviewTraffic = (props) => {
    const { chartSeries, labels, sx } = props;
    const chartOptions = useChartOptions(labels);

    // Determine the icon for the percentage value
    const getIconForValue = (value) => {
        if (value >= 75) return iconMap['High Morale']; // Assuming 75% and above is high morale
        if (value >= 50) return iconMap['Average Morale']; // Assuming between 50% and 74% is average morale
        return iconMap['Average Morale']; // Assuming below 50% is low morale
    };

    return (
        <Card sx={sx}>
            <CardHeader title="Soldier Morale" />
            <CardContent>
                <Chart
                    height={300}
                    options={chartOptions}
                    series={chartSeries}
                    type="donut"
                    width="100%" />
                <Stack
                    alignItems="center"
                    direction="row"
                    justifyContent="center"
                    spacing={3}
                    sx={{ mt: 2 }}
                >
                    {labels.map((label, index) => {
                        const value = chartSeries[index];
                        // const IconComponent = getIconForValue(value); // Use a function to determine the icon
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
                                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                    {IconComponent}
                                </Box>
                            </Box>
                        );
                    })}
                </Stack>
            </CardContent>
        </Card>
    );
};
