/** @jsx jsx */
import { FunctionalComponent, h } from 'preact';
import { Link } from 'preact-router/match';
import { jsx } from '@emotion/react';
import { header } from './style';

const Header: FunctionalComponent = () => {
    return (
        <header css={header}>
            <h1>Tank</h1>
            <nav>
                <Link activeClassName="active" href="/">
                    Measurements
                </Link>
            </nav>
        </header>
    );
};
export default Header;
