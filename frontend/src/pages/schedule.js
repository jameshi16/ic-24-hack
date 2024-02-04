import Head from 'next/head';

import { useState, useEffect } from 'react';
import { subDays, subHours } from 'date-fns';
import { MenuItem, Select, Box, Container, Unstable_Grid2 as Grid } from '@mui/material';
import { Layout as DashboardLayout } from 'src/layouts/dashboard/layout';
import { Scheduler } from '@aldabil/react-scheduler';
import { generateColorHex } from 'src/utils/color-generator';
import { Stack, Typography } from '@mui/material';
import { MetricCard } from 'src/components/metric-card';
import { useAppStore, useAppSelector, useAppDispatch } from 'src/hooks/use-store';
import { Button } from '@mui/material';
import { AddTaskButton } from 'src/components/add-task-button';
import { setUnits, store } from 'src/lib/store.js';
import axios from 'axios';

const URL = process.env.NEXT_PUBLIC_API_URL;

const Page = () => {
  const [events, setEvents] = useState([]);

  const [unit, setUnit] = useState(null);

  const translateUnitToBackend = (idx, start_date, data) => {
    return ({
      id: idx,
      name: `Sub Unit ${idx + 1}`,
      events: data.map((val, id) => {
        return ({
          event_id: id + 1,
          title: `Person ${val}`,
          start: new Date(Number(new Date(start_date)) + id * 3600 * 1000),
          end: new Date(Number(new Date(start_date)) + (id + 1) * 3600 * 1000),
          color: generateColorHex(),
        });
      })
    });
  };

  const fetchData = () => {
    axios.get(URL + '/tasks').then(res => {
      setEvents(res.data.map((val, idx) =>
        translateUnitToBackend(idx, val.times.start, val.ids)));
    }).catch(e => {
      console.log(e);
      alert('tasks error. is API on?');
    });
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (events.length > 0) {
      setUnit(events[events.length - 1]);
    }
  }, [events]);

  useEffect(() => {
    console.log(unit);
  }, [unit]);

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
                <AddTaskButton taskUpdatedCallback={fetchData} />
                <Select label="Metric" onChange={event => {
                  setUnit(events.find(data => event.target.value === data.id));
                }} value={unit ? unit.id : null}>
                  {
                    events.map(val => (
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
              editor={false}
              props={{
                startHour: 8,
                endHour: 17,
              }}
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
