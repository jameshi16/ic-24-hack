import { useState } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField, Skeleton, Stack } from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import AddIcon from '@mui/icons-material/Add';
import axios from 'axios';

const URL = process.env.NEXT_PUBLIC_API_URL;

export const AddTaskButton = ({ taskUpdatedCallback }) => {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [taskName, setTaskName] = useState('');
  const [startTime, setStartTime] = useState(new Date());
  const [endTime, setEndTime] = useState(new Date());
  const [people, setPeople] = useState(1);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleAddTask = () => {
    if (!open || !taskName || !startTime || !endTime || !people) {
      alert("At least one of the fields are empty");
      return;
    }

    setIsLoading(true);
    axios.post(URL + '/set-task', {
      start_dt: startTime,
      end_dt: endTime,
      number: people,
    }).catch(() => {
      console.log('uh oh, set task deadge');
    }).finally(() => {
      handleClose();
      setIsLoading(false);
      if (taskUpdatedCallback) {
        taskUpdatedCallback();
      }
    });
  };

  const handleSetStartTime = (date) => {
    date.setMilliseconds(0);
    date.setSeconds(0);
    date.setMinutes(0);
    if (date > endTime) {
      alert('end time > start time smh my head');
      return;
    }
    setStartTime(date);
  };

  const handleSetEndTime = (date) => {
    date.setMilliseconds(0);
    date.setSeconds(0);
    date.setMinutes(0);
    if (date < startTime) {
      alert('end time < start time smh my head');
      return;
    }
    setEndTime(date);
  };

  const handleSetPeople = (val) => {
    if (val <= 0) {
      alert('people <= 0 smh my head');
      return;
    }

    const regex = /^[0-9]+$/;
    if (regex.test(val)) {
      setPeople(val);
    }
  };

  return (
    <>
      <Button onClick={handleClickOpen}>
        <AddIcon /> Add Task
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Add New Task</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please enter the task name:
          </DialogContentText>
          <Stack gap={2}>
            <TextField
              autoFocus
              margin="dense"
              id="taskName"
              label="Task Name"
              type="text"
              fullWidth
              value={taskName}
              onChange={event => setTaskName(event.target.value)}
            />

            <Stack direction="row" justifyContent="space-between" gap={2}>
              <DateTimePicker fullWidth label="Start Time"
                views={['year', 'month', 'day', 'hours']}
                value={startTime} onChange={handleSetStartTime} />
              <DateTimePicker fullWidth label="End Time"
                views={['year', 'month', 'day', 'hours']}
                value={endTime} onChange={handleSetEndTime} />
            </Stack>

            <TextField
              margin="dense"
              id="people"
              label="People"
              type="number"
              fullWidth
              value={people}
              onChange={event => handleSetPeople(event.target.value)}
            />
          </Stack>
        </DialogContent>
        {isLoading ? <Skeleton width={100} /> :
          <DialogActions>
            <Button onClick={handleClose} color="secondary">
              Cancel
            </Button>
            <Button onClick={handleAddTask} color="primary">
              Add Task
            </Button>
          </DialogActions>}
      </Dialog>
    </>
  );
};
