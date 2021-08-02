/** @jsx jsx */

import { FunctionalComponent, h } from 'preact';
import { Link } from 'preact-router/match';
import { notfound } from './style';
import { jsx } from '@emotion/react';
const Notfound: FunctionalComponent = () => {
    return (
        <div css={notfound}>
            <h1>Error 404</h1>
            <p>That page doesn&apos;t exist.</p>
            <Link href="/">
                <h4>Back to Home</h4>
            </Link>
        </div>
    );
};

export default Notfound;
