import PropTypes from 'prop-types';
import { Card, CardContent, CardHeader, Typography } from '@mui/material';

export const OverviewTrainingHours = ({ hours, sx }) => (
    <Card sx={sx}>
        <CardHeader title="Daily Training Hours" />
        <CardContent>
            <Typography variant="h4">{hours} Hours</Typography>
            <Typography color="text.secondary">Average per soldier</Typography>
        </CardContent>
    </Card>
);

OverviewTrainingHours.propTypes = {
    hours: PropTypes.number.isRequired,
    sx: PropTypes.object,
};

