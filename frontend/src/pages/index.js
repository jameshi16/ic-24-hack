import Head from 'next/head';
import { subDays, subHours } from 'date-fns';
import { Box, Container, Unstable_Grid2 as Grid } from '@mui/material';
import { Layout as DashboardLayout } from 'src/layouts/dashboard/layout';
import { Scheduler } from '@aldabil/react-scheduler';
import { generateColorHex } from 'src/utils/color-generator'
import { Stack, Typography } from '@mui/material';
import { MetricCard } from 'src/components/metric-card';

const now = new Date();

const Page = () => (
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
          <Typography variant="h4">
            Schedule
          </Typography>
          <Scheduler
            view="day"
            customViewer={(event, close) => <MetricCard event={event} close={close} data={{
            }} />}
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
  </>
);

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;
