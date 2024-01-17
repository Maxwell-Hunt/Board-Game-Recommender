import {useState} from 'react';
import {Link} from 'react-router-dom';

function SearchBar() {
    let [text, setText] = useState('');
    let searchParams = new URLSearchParams();
    searchParams.append("query", text);
    
    const to = {pathname: "/results", search: searchParams.toString()};

    return (
        <div className="search_bar">
            <input type="text" value={text} onChange={(e) => setText(e.target.value)}></input>
            <Link to={to}><button onClick={() => setText("")}>Search</button></Link>
        </div>
    );
}

export default SearchBar;