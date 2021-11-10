import { css } from '@emotion/react';
import { g } from '../../style/global';

export const info = css`
    display: flex;
    width: 100%
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
`;

export const warning = css`
    color: #993800;
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: start;
    font-size: normal;
    font-weight: 600;
`;

export const ws = {
    nowrap: css`white-space: nowrap`
};

export const flex = {
    nowrap: css`flex-wrap: nowrap`,
    wrap: css`wrap`
}

export const home = css`
    padding-left: 2px;
    padding-right: 2px;
    padding-top: ${g.header.height};
    height: calc(100vh - 0.25rem);
	width: 100%;
    display: flex;
    flex-direction: column;
`;

export const currently = css`
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: start;
	font-size: normal;
	font-weight: 800;
	padding-top: 0.25rem;
	padding-bottom: 0.25rem;
`;

export const px1 = css`
    padding-left: 1rem;
    padding-right: 1rem;
`;

export const title = css`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
	font-size: larger;
	font-weight: 800;
	padding-top: 0.25rem;
	padding-bottom: 0.25rem;
`;

export const text = css`
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
	font-weight: 500;
	padding-top: 0.25rem;
	padding-bottom: 0.25rem;
`;