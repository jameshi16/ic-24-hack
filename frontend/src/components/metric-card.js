// Sleep, Alertness, Physical
import { useState, useEffect } from 'react';
import { Box, Typography, Select, MenuItem, Skeleton } from '@mui/material';
import { MetricGraph } from 'src/components/metric-graph';
import { getFormattedDateTime } from 'src/utils/date-util';
import axios from 'axios';

const URL = process.env.NEXT_PUBLIC_API_URL;

export const MetricCard = ({ event, close }) => {
  const [selectedMetric, setSelectedMetric] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState({});
  const [xAxis, setXAxis] = useState([]);
  const userId = event.title;

  useEffect(() => {
    setIsLoading(true);
    axios.get(URL + `/get_user/${userId}`)
      .then(response => {
        setData(response.data.scores);
        const startTime = new Date(response.data.startTime);

        // NOTE: ugly hack to generate 100 hours. I'm dumb
        let arr = [];
        for (let i = 0; i < response.data.length; i++) {
          arr.push(startTime + i * 1000 * 3600);
        }
        setXAxis(arr);
        setSelectedMetric(Object.keys(response.data.scores)[0]);
        setIsLoading(false);
      }).catch(error => {
        console.log(error);
        alert("oh noes");
      });
  }, []);

  const transformData = datApoint => ({
    times: datapoint.times.map(val => getFormattedDateTime(val)),
    tensor: datapoint.tensor,
  });

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4">
        Data
      </Typography>


      {isLoading ?
        <Skeleton variant="rectangular" /> :
        <Select label="Metric" value={selectedMetric} onChange={
          event => setSelectedMetric(event.target.value)}>
          {
            Object.keys(data).map((datum, index) => {
              return <MenuItem value={datum}>{datum}</MenuItem>;
            })
          }
        </Select>}
      {isLoading ? <Skeleton variant="rectangular" width={500} height={200} /> :
        <MetricGraph
          times={xAxis}
          tensor={[data[selectedMetric]]}
        />
      }
    </Box>
  );
};
