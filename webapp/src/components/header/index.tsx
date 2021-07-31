import { FunctionalComponent, h } from 'preact';
import { Link } from 'preact-router/match';
import style from './style.css';

const Header: FunctionalComponent = () => {
    return (
        <header class={style.header}>
            <h1>Tank</h1>
            <nav>
                <Link activeClassName={style.active} href="/">
                    Measurements
                </Link>
            </nav>
        </header>
    );
};

/* <Link activeClassName={style.active} href="/profile">
Me
</Link>
<Link activeClassName={style.active} href="/profile/john">
    John
</Link>
*/
export default Header;
