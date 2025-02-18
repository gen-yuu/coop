import { useEffect, useState } from 'react';
import ItemList from './ItemList';
import axios from "axios";



function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    axios.get("http://backend:5000/api/data")
      .then((response) => {
        setItems((prevItems) => [...prevItems, response.data]); // 配列に追加
      })
      .catch((error) => console.error(error));
  }, []);
  
  return (
    <>
      <ItemList items={items}/>
      <button id="confirm-purchase">購入確定</button>
      <div id="insertBarcodeError"></div>
      <div id="items"></div> 
    </>
  );
}

export default App;
