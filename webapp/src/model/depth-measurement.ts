export interface DepthMeasurement {
    date: string;
    depth: number;
}

export const initialDepthMeasurement: DepthMeasurement = {
    date: 'n/a',
    depth: new Date().getUTCDate()
}