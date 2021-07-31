import { FunctionalComponent, h } from 'preact';
import { useEffect, useState, useContext } from 'preact/hooks';
import { ConfigContext, SocketContext } from '../../components/context/global-context';
import HistoryChart from '../../components/history-chart';
import { utcStringToLocalString } from '../../components/history-chart/model';

import { DepthMeasurement, initialDepthMeasurement } from '../../model/depth-measurement';
import style from './style.css';


const Home: FunctionalComponent = () => {
    const socket = useContext(SocketContext);
    const config = useContext(ConfigContext);
    const [measurement, setMeasurement] = useState(initialDepthMeasurement);

    useEffect(() => {

        function onDismount(): void {
            // before the component is destroyed
            // unbind all event handlers used in this component
            socket.off("depth", (measurement: DepthMeasurement) => console.log(`OFF: ${measurement}`));
        }

        // emit USER_ONLINE event
        //socket.emit("my_event", {data: 'test'}); 
    
        // subscribe to socket events
        socket.on("depth", (measurement: DepthMeasurement) => setMeasurement(measurement)); 
    
        return onDismount;
      }, [socket]);

    

    return (
        <div class={style.home}>
            <div class={style.title}>Currently</div>
            <div class={style.text}>{utcStringToLocalString(config.LOCALE, measurement.date)}</div>
            <div class={style.text}>{measurement.depth}m</div>
            <div class={style.title}>History</div>
            <HistoryChart showChart />
        </div>
    );
};

export default Home;

