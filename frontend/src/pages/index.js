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
          Put content here
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
