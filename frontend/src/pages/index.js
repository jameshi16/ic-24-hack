import Head from 'next/head';
import { subDays, subHours } from 'date-fns';
import { Box, Container, Unstable_Grid2 as Grid } from '@mui/material';
import React, { useEffect, useState } from 'react';
import { Layout as DashboardLayout } from 'src/layouts/dashboard/layout';
import { OverviewBudget } from 'src/sections/overview/overview-budget';
import { OverviewLatestOrders } from 'src/sections/overview/overview-latest-orders';
import { OverviewLatestProducts } from 'src/sections/overview/overview-latest-products';
import { OverviewSales } from 'src/sections/overview/overview-stages';
import { OverviewTasksProgress } from 'src/sections/overview/overview-tasks-progress';
import { OverviewTotalCustomers } from 'src/sections/overview/overview-total-customers';
import { OverviewTotalProfit } from 'src/sections/overview/overview-total-profit';
import { OverviewTraffic } from 'src/sections/overview/overview-traffic';
//
import SleepLevelChart from 'src/sections/overview/overview-sleep';

const generateSleepData = () => {
  return Array.from({ length: 24 }, () => Math.floor(Math.random() * 10));
};


const Page = () => {

  const sleepData = generateSleepData();

  return (
    <>
      <Head>
        <title>Overview | Devias Kit</title>
      </Head>
      <Box component="main" sx={{ flexGrow: 1, py: 8 }}>
        <Container maxWidth="xl">
          <Grid container spacing={2}>

            <Grid item xs={12} lg={8}>
              <OverviewSales
                chartSeries={[
                  {
                    name: 'Sleep',
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 9]
                  },
                  {
                    name: 'Activity',
                    data: [0, 0, 0, 6, 2, 9, 9, 10, 11, 12, 13, 13]
                  },
                ]}
                sx={{ height: '100%' }}
              />
            </Grid>

            <Grid item xs={12} lg={4}>
              <SleepLevelChart data={sleepData} sx={{ height: '100%' }} />
            </Grid>
          </Grid>
        </Container>
      </Box>
    </>

  );
};

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;