import { useEffect, useState } from 'react';
import ItemList from './ItemList';

function App() {
  const [items,setItems] = useState([{id:1,price:150}])
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
