import {useState, useEffect} from 'react';
import {Link, useSearchParams} from 'react-router-dom';
import SearchBar from './components/searchbar';
import Game from './components/game';
import './css/Results.css'

function Results() {
    let [images, setImages] = useState([]);
    let [ids, setIds] = useState([]);
    let [ratings, setRatings] = useState([]);
    let [query, setQuery] = useSearchParams();

    useEffect(() => {
        fetch("/getresults", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({"query": query.get("query")})
        }).then(res => res.json()).then(response => {
            setImages(response.thumbnail);
            setIds(response.id);
            setRatings(response.rating);
        });

    }, [query]);

    async function handleRatingChange(id, rating) {
        try {
            const response = await fetch("/updaterating", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"id": id, "rating": rating})
            });
            await response.json();
        } catch(e) {
            console.error("FAILURE TO UPDATE RATING");
        }
    }

    return (
        <div>
            <Link to="/">Go Back</Link>
            <SearchBar/>
            <h1>These are the results</h1>
            <h3>The games are</h3>
            <ul>{images.map((image, index) => 
                <li><Game thumbnail={image}
                        id={ids[index]}
                        initialRating={ratings[index]}
                        handleRating={handleRatingChange}/>
                </li>)}
            </ul>
        </div>
    );
}

export default Results;