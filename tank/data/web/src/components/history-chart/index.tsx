/** @jsx jsx */
import { useContext, useEffect, useState } from 'preact/hooks';
import { CartesianGrid, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis, Text } from 'recharts';
import { DepthMeasurement, initialDepthMeasurement } from '../../model/depth-measurement';
import { Config, ConfigContext, SocketContext } from '../context/global-context';
import { Series, SeriesPoint, toSeriesPoint } from './model';
import { jsx } from '@emotion/react';
import { centered, chart, chartContainer } from './style';
import { FunctionalComponent, h } from 'preact';
import { Socket } from 'socket.io-client';

interface HistoryChartProperties {
    showChart?: boolean;
}

const DEPTH_SERIES_LABEL = 'Depth (m)';

const HistoryChart: FunctionalComponent<HistoryChartProperties> = (props: HistoryChartProperties) => {
    const socket = useContext<Socket>(SocketContext);
    const config = useContext<Config>(ConfigContext);
    const [history, setHistory] = useState([initialDepthMeasurement]);    
    const [chartData, setChartData] = useState<Series>(
        {
            label: null,
            data: [toSeriesPoint(initialDepthMeasurement, config.LOCALE, config.MAX_HEIGHT)]
        }
    );

    function renderHistoryEvents(history: DepthMeasurement[]): JSX.Element[] {
        const events = [];
        for(const ev of history) {
            events.push(
            <div>
                <div>{ev.depth}m</div>
                <div>{ev.date}</div>
            </div>);
        }
        return events;
    }

    function renderChart(series: Series) {
   
        return (
            <div css={chartContainer}>
                <div css={chart}>
                    <ResponsiveContainer width="90%" height="80%">
                        <LineChart data={series.data} margin={{ top: 5, right: 0, bottom: 150, left: 0 }}>
                            <Line type="monotone" dataKey="depth" stroke="#8884d8" dot={{r: 1}} animationDuration={50} />
                            <ReferenceLine y={config.MAX_HEIGHT} label="Full" stroke="red" strokeDasharray="4 3" />
                            <ReferenceLine y={config.MIN_HEIGHT} label="Empty" stroke="green" strokeDasharray="4 3" />
                            <CartesianGrid stroke="#ccc" strokeDasharray="1 1" />
                            <XAxis dataKey="date" textAnchor="end" angle={-45} />
                            <YAxis dataKey="depth" textAnchor="end" domain={[0, config.MAX_HEIGHT+0.2]} label={(<Text x={0} y={0} dx={20}dy={150} offset={0} angle={-90}>Water level (m)</Text>)} />
                            <Tooltip />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
        );
    }

    useEffect(() => {
        fetch(`${config.backend()}/history?limit=${config.HISTORY_LIMIT}`)
        .then((response: Response) => {
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            return response.json();
        })
        .then((response: {history: DepthMeasurement[]}) => {
            setHistory(response.history);
            setChartData({
                label: DEPTH_SERIES_LABEL,
                data: response.history.map(m => toSeriesPoint(m, config.LOCALE, config.MAX_HEIGHT))
            });
            console.log(`Got ${response.history.length} entries`);
        });
    },[config]);

    useEffect(() => {
        function onDismount(): void {
            // before the component is destroyed
            // unbind all event handlers used in this component
            socket.off("depth", (depth: DepthMeasurement) => console.log(`OFF: ${depth}`));
        }
        // subscribe to socket events
        socket.on("depth", (measurement: DepthMeasurement) => {
            const currentMeasurement = toSeriesPoint(measurement, config.LOCALE, config.MAX_HEIGHT);
            setChartData({
                label: DEPTH_SERIES_LABEL,
                data: [...chartData.data, currentMeasurement]
            })
        }); 
        return onDismount;
      }, [chartData.data, config.LOCALE, config.MAX_HEIGHT, socket]);

    return (
        <div>
            {!props.showChart && renderHistoryEvents(history)}
            {props.showChart && chartData.label !== null && renderChart(chartData)}
            {props.showChart && chartData.label == null && 
                <div css={centered}>Loading history...</div>
            }
        </div>);
}

export default HistoryChart;