import React, {useState, useEffect} from 'react';
import SearchBar from './components/searchbar';
import './css/App.css';

function App() {
  let [images, setImages] = useState([]);
  let [loadingRecommendations, setLoadingRecommendations] = useState(true);

  useEffect(() => {
    fetch("/getrecommendations").then(res => res.json()).then(res => {
      setLoadingRecommendations(false);
      setImages(res.thumbnail);
    });
  }, []);

  return (
    <div>
      <SearchBar/>
      {loadingRecommendations && <h1>Loading Recommendations...</h1>}
      <ul className="recommendation_list">{images.map(image => <li><img src={image}/></li>)}</ul>
    </div>
  );
}

export default App;
