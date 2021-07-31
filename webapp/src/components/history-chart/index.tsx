import { FunctionalComponent, h } from 'preact';
import { useContext, useEffect, useState } from 'preact/hooks';
import { CartesianGrid, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis, Text } from 'recharts';
import { DepthMeasurement, initialDepthMeasurement } from '../../model/depth-measurement';
import { ConfigContext, SocketContext } from '../context/global-context';
import { Series, toSeriesPoint } from './model';
import style from './style.css';

interface HistoryChartProperties {
    showChart?: boolean;
}

const DEPTH_SERIES_LABEL = 'Depth (m)';

const HistoryChart: FunctionalComponent<HistoryChartProperties> = (props: HistoryChartProperties) => {
    const socket = useContext(SocketContext);
    const config = useContext(ConfigContext);
    const [history, setHistory] = useState([initialDepthMeasurement]);    
    const [chartData, setChartData] = useState<Series>(
        {
            label: null,
            data: [toSeriesPoint(initialDepthMeasurement, config.LOCALE, config.MAX_HEIGHT)]
        }
    );

    function renderHistoryEvents(history: DepthMeasurement[]): h.JSX.Element[] {
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

    function renderChart(series: Series): h.JSX.Element {
   
        return (
            <div class={style.chartContainer}>
                <ResponsiveContainer width="80%" height="50%">
                    <LineChart data={series.data} margin={{ top: 5, right: 0, bottom: 150, left: 150 }}>
                        <Line type="monotone" dataKey="depth" stroke="#8884d8" dot={{r: 1}} animationDuration={50} />
                        <ReferenceLine y={config.MAX_HEIGHT} label="Full" stroke="red" strokeDasharray="4 3" />
                        <ReferenceLine y={config.MIN_HEIGHT} label="Empty" stroke="green" strokeDasharray="4 3" />
                        <CartesianGrid stroke="#ccc" strokeDasharray="1 1" />
                        <XAxis dataKey="date" textAnchor="end" angle={-45} />
                        <YAxis dataKey="depth" textAnchor="end" label={(<Text x={0} y={0} dx={180}dy={280} offset={0} angle={-90}>Water level (m)</Text>)} />
                        <Tooltip />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        );
    }

    useEffect(() => {
        fetch(`${config.backend}/history?limit=${config.HISTORY_LIMIT}`)
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
        socket.on("depth", (depth: DepthMeasurement) => {
            setChartData({
                label: DEPTH_SERIES_LABEL,
                data: [...chartData.data, toSeriesPoint(depth, config.LOCALE, config.MAX_HEIGHT)]
            })
        }); 
        return onDismount;
      }, [chartData.data, config.LOCALE, config.MAX_HEIGHT, socket]);

    return (
        <div>
            {!props.showChart && renderHistoryEvents(history)}
            {props.showChart && chartData.label !== null && renderChart(chartData)}
            {props.showChart && chartData.label == null && 
                <div class={style.centered}>Loading history...</div>
            }
        </div>);
}

export default HistoryChart;