/** @jsx jsx */
import { jsx } from "@emotion/react";
import { FunctionalComponent } from "preact";
import { useContext, useEffect, useState } from "preact/hooks";
import {
  ConfigContext,
  SocketContext,
} from "../../components/context/global-context";
import HistoryChart from "../../components/history-chart";
import { toSeriesPoint, utcStringToLocalString } from "../../components/history-chart/model";
import {
  DepthMeasurement,
  MeasurementState,
  initialMeasurements
} from "../../model/depth-measurement";
import { home, title, currently, px1, warning } from "./style";

const Home: FunctionalComponent = () => {
  const socket = useContext(SocketContext);
  const config = useContext(ConfigContext);
  const [msrmt, setMsrmt] = useState(initialMeasurements);

  function getDiff(last: DepthMeasurement | null, current: DepthMeasurement | null) {
    if (!!last?.date && !!current?.date)
    {  
      const ld = Date.parse(last.date);
      const cd = Date.parse(current.date);
      return cd - ld;
    }
    return 0;
  }

  function isOutDated(m: MeasurementState) {
    return m.diff > config.OUTDATED_THRESHOLD;
  }

  function toTimeString(seconds: number) {
    const sec = Math.round(seconds % 60);
    const minutes = Math.floor(seconds / 60);
    const min = minutes % 60;
    const hours = Math.floor(minutes / 60);
    const h = hours % 24;
    const days = Math.floor(hours / 24);
    return `${days > 0 ? days+" d" : ''} ${h > 0 ? h+" h" : ''} ${min > 0 ? min+" min" : ''} ${sec > 0 ? sec+" sec" : ''}`;
  }

  useEffect(() => {
    function onDismount(): void {
      // before the component is destroyed
      // unbind all event handlers used in this component
      socket.off("depth", (measurement: DepthMeasurement) =>
        console.log(`OFF: ${measurement}`)
      );
    }

    // emit USER_ONLINE event
    //socket.emit("my_event", {data: 'test'});

    // subscribe to socket events
    socket.on("depth", (measurement: DepthMeasurement) => {
      setMsrmt({...msrmt,
        last: msrmt.current,
        current: measurement,
        diff: getDiff(msrmt.current, measurement) / 1000
      });
    });

    return onDismount;
  }, [socket, msrmt]);

  return (
    <div css={home}>
      <div css={currently}>
          {!!msrmt.current?.depth && (
              <div>
                {utcStringToLocalString(config.LOCALE, msrmt.current?.date) || "N/A"}
              </div>
          )}
          {renderDepth(msrmt)}
      </div>
      <div css={warning}>
        {signalMsg()}
      </div>
      <div css={title}>History</div>
      <HistoryChart showChart />
    </div>
  );

  function renderDepth(m: MeasurementState): JSX.Element {
    if(m.current?.depth) {
      var d = toSeriesPoint(m.current, config.LOCALE, config.MAX_HEIGHT)?.depth;
      var roundedD = Math.round((d + Number.EPSILON) * 100) / 100;
      return <div css={px1}>
        {roundedD} m
      </div>;
    }
    return <div css={px1}>no data</div>;
  }

  function signalMsg(): JSX.Element {
    if (isOutDated(msrmt)) {
        return <div>Last signal {toTimeString(msrmt.diff)} ago</div>;
    }
    return <div>LIVE</div>;
  }
};

export default Home;
