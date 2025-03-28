import React, { useEffect, useState } from 'react';
import io from "socket.io-client";

const socket = io("http://localhost:8000"); // FlaskのWebSocketサーバーに接続

function App() {
  const [items, setItems] = useState([]);
  const [user, setUser] = useState(null);  // ユーザー情報
  const [isUserSet, setIsUserSet] = useState(false);  // ユーザーがセットされているか

  useEffect(() => {
    // WebSocketで商品情報を受信
    socket.on("item_registered", (data) => {
      setItems((prevItems) => [...prevItems, data]); // リストに追加
      console.log(data)
    });
    // ユーザー情報が送られてきた場合の処理
    socket.on("user_registered", (data) => {
      if (!isUserSet) {
        setUser(data);  // ユーザー情報をセット
        setIsUserSet(data);  // ユーザーがセットされた状態にする
        // console.log(data);
        console.log(isUserSet);
      }
    });
    // ユーザーが見つからない場合の処理
    socket.on("user_not_found", (data) => {
      alert(data.error);
    });
    return () => {
      socket.off("item_registered");
      socket.off("user_registered");
      socket.off("user_not_found");
    };
  }, []);  // isUserSetが変わる度に再実行

  // ユーザー情報をクリアする
  const clearUser = () => {
    setUser(null);
    setIsUserSet(false);  // ユーザーがクリアされた状態
  };

  return (
    <div>
      <h2>User Information</h2>
      {user ? (
        <div>
          <p>購入者: {user.name}</p>
          <p>残高: {user.balance}</p>
          <button onClick={clearUser}>Clear User</button>
        </div>
      ) : (
        <p>NFCをかざしてください</p>
      )}
      <h2>購入リスト</h2>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            {item.name} - {item.price}円 (購入数: {item.stock_num})
          </li>
        ))}
      </ul>
      <button id="confirm-purchase">購入確定</button>
      <div id="insertBarcodeError"></div>
      <div id="items"></div> 
    </div>
  );
}

export default App;
