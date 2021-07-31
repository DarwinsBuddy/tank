import { DepthMeasurement } from "../../model/depth-measurement";

export type Series = {
    label: string | null;
    data: SeriesPoint[];
}

export type SeriesPoint = {
    date: string;
    depth: number;
}

export function utcStringToLocalString(locale: string, date: string ): string {
    const d = new Date(date);
    return `${d.toLocaleDateString(locale)} ${d.toLocaleTimeString(locale, {hour12: false})}`;
}

export function toSeriesPoint(measurement: DepthMeasurement, locale: string, maxValue: number): SeriesPoint {
    
    return {
        date: utcStringToLocalString(locale, measurement.date),
        depth: maxValue - measurement.depth
    }
}