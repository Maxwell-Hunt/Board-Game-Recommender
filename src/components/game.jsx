import { useState, useEffect} from "react";

function Game({thumbnail, id, initialRating, handleRating}) {
    let [rating, setRating] = useState(initialRating);

    useEffect(() => {
        setRating(initialRating);
    }, [id])

    return (
        <div className="Game">
            <img src={thumbnail}/>
            <input type="range" min={0} max={10} step={0.5} value={rating} onChange={(e) => {
                setRating(e.target.value);
                handleRating(id, e.target.value);
            }}/>
            <p>{parseFloat(rating).toFixed(1)}</p>
        </div>
    );
}

export default Game;