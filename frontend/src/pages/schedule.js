import Head from 'next/head';

import { useState, useEffect } from 'react';
import { subDays, subHours } from 'date-fns';
import { MenuItem, Select, Box, Container, Unstable_Grid2 as Grid } from '@mui/material';
import { Layout as DashboardLayout } from 'src/layouts/dashboard/layout';
import { Scheduler } from '@aldabil/react-scheduler';
import { generateColorHex } from 'src/utils/color-generator'
import { Stack, Typography } from '@mui/material';
import { MetricCard } from 'src/components/metric-card';

const Page = () => {
  const mockData = [
    {
      id: 'sub-unit-1',
      name: 'Sub Unit 1'
    },
    {
      id: 'sub-unit-2',
      name: 'Sub Unit 2'
    }
  ];
  const [unit, setUnit] = useState(null);
  useEffect(() => {
    setUnit(mockData[0]);
  }, []);

  return (
    <>
      <Head>
        <title>
          Overview | {process.env.NEXT_PUBLIC_APP_NAME}
        </title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8
        }}
      >
        <Container maxWidth="xl">
          <Stack>
            <Stack direction="row" justifyContent="space-between" alignItems="center">
              <Typography variant="h4">
                Schedule
              </Typography>
              <Select label="Metric" onChange={event => {
                console.log(mockData.find(data => event.target.value === data.id));
                setUnit(mockData.find(data => event.target.value === data.id));
              }
              }>
                {
                  mockData.map(val => (
                    <MenuItem value={val.id}>{val.name}</MenuItem>
                  ))
                }
              </Select>
            </Stack>
            <Scheduler
              view="day"
              customViewer={(event, close) => <MetricCard event={event} close={close} />}
              events={[
                {
                  event_id: 1,
                  title: "Person1 ",
                  start: new Date("2024/2/3 09:30"),
                  end: new Date("2024/2/3 10:30"),
                  color: generateColorHex()
                },
                {
                  event_id: 2,
                  title: "Person 2",
                  start: new Date("2024/2/3 10:00"),
                  end: new Date("2024/2/3 11:00"),
                  color: generateColorHex()
                },
              ]}
            />
          </Stack>
        </Container>
      </Box>
    </>);
};

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;
