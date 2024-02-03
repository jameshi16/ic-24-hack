// Sleep, Alertness, Physical
import { useState, useEffect } from 'react';
import { Box, Typography, Select, MenuItem } from '@mui/material';
import { MetricGraph } from 'src/components/metric-graph';
import { getFormattedDateTime } from 'src/utils/date-util';

export const MetricCard = ({ event, close }) => {
  const [selectedMetric, setSelectedMetric] = useState(0);
  const data = [
    { // TODO: Probably want the metric ID here as well
      times: ["2024-02-03T18:00", "2024-02-03T19:00"],
      tensor: [[10, 10]]
    },
    { // TODO: Probably want the metric ID here as well
      times: ["2024-02-03T18:00", "2024-02-03T19:00"],
      tensor: [[10, 20]]
    },
    { // TODO: Probably want the metric ID here as well
      times: ["2024-02-03T18:00", "2024-02-03T19:00"],
      tensor: [[30, 80]]
    }
  ];

  const transformData = datapoint => ({
    times: datapoint.times.map(val => getFormattedDateTime(val)),
    tensor: datapoint.tensor,
  });

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4">
        Data
      </Typography>
      <Select label="Metric" value={selectedMetric} onChange={
        event => setSelectedMetric(event.target.value)}>
        <MenuItem value={0}>Metric 1</MenuItem>
        <MenuItem value={1}>Metric 2</MenuItem>
        <MenuItem value={2}>Metric 3</MenuItem>
      </Select>
      <MetricGraph
        times={transformData(data[selectedMetric]).times}
        tensor={data[selectedMetric].tensor}
      />
    </Box>
  );
};
