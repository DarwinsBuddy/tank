/** @jsx jsx */
import { css, jsx } from '@emotion/react'
import { g } from '../../style/global'

export const header = css`
	position: fixed;
	left: 0;
	top: 0;
	width: 100%;
	height: ${g.header.height};
	padding: 0;
	background: #673AB7;
	box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
	z-index: 50;
	
	h1 {
		float: left;
		margin: 0;
		padding: 0 15px;
		font-size: ${g.header.font};
		line-height: ${g.header.height};
		font-weight: 400;
		color: #FFF;
	}

	nav {
		float: right;
		font-size: 100%;
	}

	nav a {
		display: inline-block;
		height: ${g.header.height};
		line-height: ${g.header.height};
		padding: 0 15px;
		min-width: 50px;
		text-align: center;
		background: rgba(255,255,255,0);
		text-decoration: none;
		color: #FFF;
		will-change: background-color;
	}

	nav a:hover,
	nav a:active {
		background: rgba(0,0,0,0.2);
	}

	nav a.active {
		background: rgba(0,0,0,0.4);
	}`