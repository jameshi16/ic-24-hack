import Head from 'next/head';

import { useState, useEffect } from 'react';
import { subDays, subHours } from 'date-fns';
import { MenuItem, Select, Box, Container, Unstable_Grid2 as Grid } from '@mui/material';
import { Layout as DashboardLayout } from 'src/layouts/dashboard/layout';
import { Scheduler } from '@aldabil/react-scheduler';
import { generateColorHex } from 'src/utils/color-generator';
import { Stack, Typography } from '@mui/material';
import { MetricCard } from 'src/components/metric-card';
import { useAppStore, useAppSelector } from 'src/hooks/use-store';
import { Button } from '@mui/material';
import { AddTaskButton } from 'src/components/add-task-button';

const Page = () => {
  const units = useAppSelector(state => state.units);

  const [unit, setUnit] = useState(null);
  useEffect(() => {
    if (units.length > 0) {
      setUnit(units[0]);
    }
  }, [units]);

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
              <Stack direction="row" alignItems="center" spacing={2}>
                <AddTaskButton />
                <Select label="Metric" onChange={event => {
                  setUnit(units.find(data => event.target.value === data.id));
                }} value={unit ? unit.id : null}>
                  {
                    units.map(val => (
                      <MenuItem value={val.id}>{val.name}</MenuItem>
                    ))
                  }
                </Select>
              </Stack>
            </Stack>
            <Scheduler
              view="day"
              customViewer={(event, close) => <MetricCard event={event} close={close} />}
              events={unit ? unit.events.map(x => x) : []}
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
