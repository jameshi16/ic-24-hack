import Head from 'next/head';
import { subDays, subHours } from 'date-fns';
import { Card, CardContent } from '@mui/material';
import { Paper, Box, Container, Unstable_Grid2 as Grid } from '@mui/material';
import { Layout as DashboardLayout } from 'src/layouts/dashboard/layout';
import { Scheduler } from '@aldabil/react-scheduler';
import { generateColorHex } from 'src/utils/color-generator'
import { Stack, Typography } from '@mui/material';
import { MetricCard } from 'src/components/metric-card';
import Forecast from 'src/sections/overview/overview-forecast';

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
      <Paper maxWidth="xl" scrollable>
        <Paper>
          <Forecast sx={{ height: '100%' }} />
          <Card sx={{ py: 2 }}>
            <CardContent sx={{ p: 3 }}>
              <Typography align="center" variant="h5" color="#cf7b09" >
                Low Readiness
              </Typography>
              <Typography variant="body" component="p" sx={{ p: 3 }}>
                A state of low readiness may indicate challenges in training, equipment maintenance, or other factors that impact the military's ability to respond swiftly and effectively to potential threats.

              </Typography>


              <Typography align="left" variant="h6" sx={{ px: 3, pb: 1 }} >
                Possible Cause
              </Typography>

              <Typography align="left" variant="body1" color="red" sx={{ px: 3, py: 2 }} >
                Reduced Sleep Quality
              </Typography>

              <Typography variant="body" component="p" sx={{ px: 3 }}>
                Total sleep time has decreased by 1.5H in the last week (see dashboard)
              </Typography>

              <Typography align="left" variant="h6" sx={{ px: 3, pt: 2 }} >
                Negative Effects
              </Typography>

              <Typography align="left" variant="body2" >
                <ul>
                  <li>Reduced physical endurance</li>
                  <li>Increased stress, anxiety</li>
                  <li>Diminishing effectiveness of communication</li>
                </ul>
              </Typography>

            </CardContent>
          </Card>
        </Paper>
      </Paper>
    </Box>
  </>
);

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;
