import { configureStore, createSlice } from '@reduxjs/toolkit';

const initialUnit = [
  {
    id: 'sub-unit-1',
    name: 'Sub Unit 1'
  },
  {
    id: 'sub-unit-2',
    name: 'Sub Unit 2'
  }
];

const unitsSlice = createSlice({
  name: 'units',
  initialState: initialUnit,
  reducers: {
    addUnit(state, action) {
      state.units.push({
        id: action.payload.id,
        name: action.payload.name
      });
    },
    removeUnit(state, action) {
      state.units = state.units.filter(unit => unit.id !== action.payload.id);
    }
  }
});

export const store = configureStore({
  reducer: {
    units: unitsSlice.reducer
  }
});
