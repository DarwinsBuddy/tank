export interface DepthMeasurement {
    date: string | null;
    depth: number | null;
}

export const initialDepthMeasurement: DepthMeasurement = {
    date: null,
    depth: null
}