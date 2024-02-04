import { configureStore, createSlice } from '@reduxjs/toolkit';
import { generateColorHex } from 'src/utils/color-generator';

const initialUnit = [
  {
    id: 'sub-unit-1',
    name: 'Sub Unit 1',
    events: [
      {
        event_id: 1,
        title: "Person 1",
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
    ],
  },
  {
    id: 'sub-unit-2',
    name: 'Sub Unit 2',
    events: [
      {
        event_id: 1,
        title: "Person 1",
        start: new Date("2024/2/3 11:30"),
        end: new Date("2024/2/3 12:30"),
        color: generateColorHex()
      },
      {
        event_id: 2,
        title: "Person 2",
        start: new Date("2024/2/3 12:30"),
        end: new Date("2024/2/3 13:30"),
        color: generateColorHex()
      },
    ],
  }
];

const unitsSlice = createSlice({
  name: 'units',
  initialState: [],
  reducers: {
    addUnit(state, action) {
      state.units.push({
        id: action.payload.id,
        name: action.payload.name
      });
    },
    removeUnit(state, action) {
      state.units = state.filter(unit => unit.id !== action.payload.id);
    },
    setUnits(state, action) {
      state = action.payload;
    }
  }
});

export const { addUnit, removeUnit, setUnits } = unitsSlice.actions;

export const store = configureStore({
  reducer: {
    units: unitsSlice.reducer
  }
});
