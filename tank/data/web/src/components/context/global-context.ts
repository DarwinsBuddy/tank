import { createContext } from "preact";
import { io, Socket } from "socket.io-client";

export type Config = {
    backend: () => string,
    production: boolean,
    HISTORY_LIMIT: number;
    NAMESPACE: string;
    MAX_HEIGHT: number;
    MIN_HEIGHT: number;
    LOCALE: string;
}

export const config: Config = {
    backend: () => {
        if(!!import.meta.env.VITE_BACKEND && !import.meta.env.PROD) {
            return import.meta.env.VITE_BACKEND;
        } else {
            return `${window.location.protocol}//${window.location.hostname}:8080`;
        }
    },
    production: import.meta.env.PROD,
    HISTORY_LIMIT: 100,
    NAMESPACE: 'data',
    MAX_HEIGHT: 1.8,
    MIN_HEIGHT: 0.3,
    LOCALE: 'de-AT'
};

const socketConfig = {
    reconnectionDelayMax: 10000,
    /*auth: {
        token: "123"
    },
    query: {
        "my-key": "my-value"
    }*/
};

//export const socket = io(`ws://localhost:8080/${NAMESPACE}`, config);
//export const socket = io(`/${NAMESPACE}`, config);
export const socket = io(`${config.backend()}/${config.NAMESPACE}`, socketConfig);

export const ConfigContext = createContext<Config>(config);
export const SocketContext = createContext<Socket>(socket);
