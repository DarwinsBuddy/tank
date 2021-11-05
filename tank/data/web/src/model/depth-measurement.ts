import { currently } from "../routes/home/style";

export interface MeasurementState {
    last: DepthMeasurement | null;
    current: DepthMeasurement | null;
    diff: number;
}

export interface DepthMeasurement {
    date: string | null;
    depth: number | null;
}

export const initialDepthMeasurement: DepthMeasurement = {
    date: null,
    depth: null
}

export const initialMeasurements: MeasurementState = {
    last: null,
    current: null,
    diff: 0
}