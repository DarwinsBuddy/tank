import { DepthMeasurement } from "../../model/depth-measurement";

export type Series = {
    label: string | null;
    data: SeriesPoint[];
}

export type SeriesPoint = {
    date: string;
    depth: number;
}

export function utcStringToLocalString(locale: string, date: string | null ): string | null {
    if (date !== null) {
        const d = new Date(date+"Z");
        return `${d.toLocaleDateString(locale, {})} ${d.toLocaleTimeString(locale, {hour12: false})}`;
    }
    return null;
}

export function toSeriesPoint(measurement: DepthMeasurement, locale: string, maxValue: number): SeriesPoint {
    return {
        date: utcStringToLocalString(locale, measurement.date) || '',
        depth: measurement.depth != null ? maxValue - measurement.depth : maxValue
    }
}