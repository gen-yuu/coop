import React from "react";

const Item = ({ item }) => {
  return (
    <div className="item">
      <span>商品ID: {item.id}</span> - <span>価格: {item.price}円</span>
    </div>
  );
};

export default Item;